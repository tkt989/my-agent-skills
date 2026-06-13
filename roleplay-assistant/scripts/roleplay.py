#!/usr/bin/env python3
"""State manager for the roleplay-assistant Codex skill."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
CHARACTERS_DIR = SKILL_DIR / "characters"
STATE_FILE = SKILL_DIR / "state" / "current_character.json"
ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


def emit(payload: dict[str, Any], exit_code: int = 0) -> int:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return exit_code


def read_state() -> dict[str, Any]:
    if not STATE_FILE.exists():
        return {"active_character": None}

    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"active_character": None}

    active = data.get("active_character")
    if isinstance(active, str) or active is None:
        return {"active_character": active}
    return {"active_character": None}


def write_state(active_character: str | None) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps({"active_character": active_character}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def character_path(character_id: str) -> Path:
    if not ID_PATTERN.fullmatch(character_id):
        raise ValueError("character_id may contain only letters, digits, underscores, and hyphens")
    return CHARACTERS_DIR / f"{character_id}.md"


def relative_character_file(path: Path) -> str:
    return path.relative_to(SKILL_DIR).as_posix()


def command_status() -> int:
    active = read_state()["active_character"]
    if active is None:
        return emit({"active_character": None})

    try:
        path = character_path(active)
    except ValueError:
        return emit({"active_character": None})

    if not path.is_file():
        return emit(
            {
                "active_character": active,
                "error": "active_character_file_not_found",
                "character_file": relative_character_file(path),
            },
            1,
        )

    return emit(
        {
            "active_character": active,
            "character_file": relative_character_file(path),
            "content": path.read_text(encoding="utf-8"),
        }
    )


def command_list() -> int:
    characters = [
        {"id": path.stem, "display_name": path.stem}
        for path in sorted(CHARACTERS_DIR.glob("*.md"))
        if path.is_file()
    ]
    return emit({"characters": characters})


def command_set(character_id: str) -> int:
    try:
        path = character_path(character_id)
    except ValueError as exc:
        return emit({"error": "invalid_character_id", "message": str(exc)}, 2)

    if not path.is_file():
        return emit(
            {
                "error": "character_not_found",
                "active_character": read_state()["active_character"],
                "character_id": character_id,
            },
            1,
        )

    write_state(character_id)
    return emit(
        {
            "active_character": character_id,
            "character_file": relative_character_file(path),
            "content": path.read_text(encoding="utf-8"),
        }
    )


def command_reset() -> int:
    write_state(None)
    return emit({"active_character": None})


def usage() -> int:
    return emit(
        {
            "error": "usage",
            "message": "Usage: roleplay.py status | list | set <character_id> | reset",
        },
        2,
    )


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        return usage()

    command = argv[1]
    if command == "status" and len(argv) == 2:
        return command_status()
    if command == "list" and len(argv) == 2:
        return command_list()
    if command == "set" and len(argv) == 3:
        return command_set(argv[2])
    if command == "reset" and len(argv) == 2:
        return command_reset()

    return usage()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
