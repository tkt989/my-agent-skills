---
name: obsidian-root-organizer
description: Organize loose Markdown files at the root of an Obsidian vault into appropriate existing folders. Use this skill whenever the user asks to tidy, organize, classify, move, or clean up root-level .md files in a notes vault, especially when they want confirmation before file operations, want only root Markdown files touched, or need duplicate or related notes merged rather than overwritten.
---

# Obsidian Root Markdown Organizer

Use this skill to safely organize Markdown notes that are sitting in the root of an Obsidian vault.

The core behavior is conservative: inspect first, propose a plan, ask for confirmation, then move only the files that the user approved. Preserve unrelated files and avoid overwriting existing notes.

## Workflow

1. Identify the vault root.
   - Use the current working directory unless the user names another vault path.
   - List root-level Markdown files with `find . -maxdepth 1 -type f -name '*.md' -print`.
   - Do not include `.DS_Store`, images, PDFs, attachments, or nested Markdown files unless the user explicitly expands scope.

2. Inspect the existing folder structure.
   - List root-level directories with `find . -maxdepth 1 -type d -print`.
   - If needed, list one or two levels of subfolders to understand local conventions.
   - Prefer existing folders over creating new ones.

3. Read enough of each root Markdown file to classify it.
   - Use `sed -n '1,80p' '<file>'` or a similarly small preview.
   - Infer category from title, content, date format, and nearby folder naming conventions.
   - Examples:
     - Language-learning notes belong in the vault's language-learning folder if one exists.
     - Daily notes belong in the vault's daily-note folder only if content and filename match the vault's daily-note convention.
     - Book notes belong in the vault's book-note folder if one exists.
     - Interview, work, and presentation notes belong in a work-related folder if one exists.

4. Propose moves before changing anything.
   - Show a concise mapping: `source` -> `destination`.
   - Include files intentionally left untouched.
   - Ask for explicit confirmation before running `mv`, unless the user has already confirmed the exact plan.

5. Move only approved root-level Markdown files.
   - Use `mv` for each approved file.
   - Do not delete or move non-Markdown files unless the user explicitly says to.
   - Avoid broad shell globs that could catch nested files or unintended extensions.

6. Handle conflicts conservatively.
   - If the destination path already exists, do not overwrite it.
   - Compare the existing note and the loose note by reading both.
   - If they are related, ask whether to merge or keep both.
   - When merging, append the loose note under a clear section such as `## LT Notes`, `## Additional Notes`, or another context-specific heading.
   - After a successful merge, delete the duplicate loose file only when its content is preserved in the destination.

7. Verify the result.
   - Confirm the remaining root-level Markdown files with `find . -maxdepth 1 -type f -name '*.md' -print`.
   - Confirm expected destination files exist.
   - Report what moved, what was merged, and what was left untouched.

## Confirmation Rules

Always ask before the first file operation when the user's request says "操作する前に確認", "確認してから", "check before operating", or similar.

If the user narrows scope after a proposal, follow the narrower scope. For example, if they say to move only root-level `*.md` files, then touch only root-level Markdown files and leave `.DS_Store` alone.

If the user corrects a classification, accept the correction and adjust the destination. Example: if a file was placed in a work folder but the user says it is a book impression note, move or merge it into the book-note folder.

## Shell Practices

Use `rg` for text searches when needed. Use `find`, `sed`, and `ls` for simple filesystem inspection.

Quote paths because Obsidian vaults often contain spaces, Japanese filenames, and iCloud paths.

Prefer separate explicit `mv` commands for each file. This makes review and recovery easier than a broad bulk command.

## Reporting Format

Before changes:

```text
Move plan:
- `source.md` -> `folder/source.md`
- `another.md` -> `other-folder/another.md`

Please confirm before I run these moves.
```

After changes:

```text
Done.

- `source.md` -> `folder/source.md`
- `duplicate.md` was merged into `folder/existing.md`, then the duplicate file was removed

There are now 0 root-level `*.md` files.
```
