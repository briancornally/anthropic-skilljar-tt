#!/usr/bin/env python3
"""Rename files/folders replacing spaces with underscores, and update markdown references."""

import os
import re
import sys
from pathlib import Path


def collect_renames(root: Path) -> list[tuple[Path, Path]]:
    """Walk bottom-up so child paths are renamed before parents."""
    renames = []
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        for name in filenames + dirnames:
            if " " in name:
                old = Path(dirpath) / name
                new = Path(dirpath) / name.replace(" ", "_")
                renames.append((old, new))
    return renames


def apply_renames(renames: list[tuple[Path, Path]], dry_run: bool) -> dict[str, str]:
    """Rename paths and return mapping of old→new relative string for md fixup."""
    mapping = {}
    for old, new in renames:
        rel_old = str(old.name)
        rel_new = str(new.name)
        mapping[rel_old] = rel_new
        if dry_run:
            print(f"  RENAME  {old}  →  {new.name}")
        else:
            old.rename(new)
            print(f"  renamed {old}  →  {new.name}")
    return mapping


def fix_markdown_refs(root: Path, dry_run: bool) -> None:
    """Replace spaces-in-paths inside markdown link/image syntax."""
    md_files = list(root.rglob("*.md"))
    pattern = re.compile(r"(\[.*?\]\()([^)]+)(\))")

    for md in md_files:
        text = md.read_text(encoding="utf-8")
        changed = False

        def replace_link(m: re.Match) -> str:
            nonlocal changed
            prefix, href, suffix = m.group(1), m.group(2), m.group(3)
            # Only touch local (non-URL) references
            if href.startswith("http://") or href.startswith("https://"):
                return m.group(0)
            new_href = href.replace(" ", "_")
            if new_href != href:
                changed = True
            return f"{prefix}{new_href}{suffix}"

        new_text = pattern.sub(replace_link, text)
        if changed:
            if dry_run:
                print(f"  UPDATE  {md}")
            else:
                md.write_text(new_text, encoding="utf-8")
                print(f"  updated {md}")


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    root = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else Path(".")

    if not root.exists():
        print(f"Error: {root} does not exist", file=sys.stderr)
        sys.exit(1)

    print(f"{'DRY RUN — ' if dry_run else ''}Root: {root.resolve()}\n")

    print("=== Renaming files and folders ===")
    renames = collect_renames(root)
    if renames:
        apply_renames(renames, dry_run)
    else:
        print("  nothing to rename")

    print("\n=== Updating markdown references ===")
    fix_markdown_refs(root, dry_run)

    print("\nDone.")


if __name__ == "__main__":
    main()
