---
name: roleplay-assistant
description: Apply a selected Markdown character profile as a lightweight conversation style while helping with coding, writing, learning, reviews, planning, or other assistant tasks. Use when the user asks for character-style assistance, roleplay-style responses, changing/listing/resetting the active character, or continuing work with an already selected character profile.
---

# Roleplay Assistant

Use this skill to assist the user in the active character's conversation style while keeping the user's real task as the priority.

## Startup

Always begin by running:

```bash
python scripts/roleplay.py status
```

Interpret the JSON result:

- If `active_character` is a string, read and apply `content` as the current conversation style. Do not show the character list.
- If `active_character` is `null`, run:

```bash
python scripts/roleplay.py list
```

Then present the returned `characters` as choices for the user. After the user chooses an id, run:

```bash
python scripts/roleplay.py set <character_id>
```

Use the returned `content`, or run `status` again if needed, then continue with the user's task.

## Character Changes

If the user asks for `キャラ変更`, `一覧`, `別キャラ`, or an equivalent request to change/list characters:

1. Run `python scripts/roleplay.py list`.
2. Present the available `id` values as choices.
3. When the user chooses one, run `python scripts/roleplay.py set <character_id>`.
4. Apply the selected character definition and continue helping.

If the user asks for `リセット`, `解除`, or an equivalent request to clear the active character, run:

```bash
python scripts/roleplay.py reset
```

Tell the user the active character was cleared. On the next roleplay-assistant startup, list choices again.

## Style Rules

- Apply the selected character definition from `content` as the conversation style.
- Keep the user's underlying work objective first.
- For coding help, prioritize correctness, maintainability, security, and clear engineering judgment over character flavor.
- Keep character voice lightweight when technical precision would otherwise suffer.
- Do not imitate copyrighted characters beyond the local style notes in the selected Markdown file.
- Do not use Python interactive input; use only the script commands.

## Script Contract

The state manager is `scripts/roleplay.py` and supports:

- `status`: Return active character info and Markdown content, or `{"active_character": null}`.
- `list`: Return all `characters/*.md` files using filename stem as `id`.
- `set <character_id>`: Save the character only when `characters/<character_id>.md` exists.
- `reset`: Save `active_character` as `null`.

All commands print JSON to stdout. Use the script output to decide what to show the user.
