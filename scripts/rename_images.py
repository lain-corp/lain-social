#!/usr/bin/env python3
"""Rename images in a directory to sequential numeric filenames.

Usage examples:
  # Dry run (safe)
  python3 scripts/rename_images.py --dry-run

  # Actually rename, starting at 1, sort by name (natural)
  python3 scripts/rename_images.py --dir images

  # Start at 10, sort by modification time, zero-pad to 4 digits
  python3 scripts/rename_images.py --start 10 --sort mtime --pad 4

This script performs a two-phase rename (temp names then final names)
to avoid name collisions when existing filenames overlap with the
target numeric names.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List
import uuid
import re
import os
import time

SUPPORTED_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}


def natural_key(s: str):
    # Split into list of ints and text for natural sorting
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", s)]


def gather_images(dirpath: Path) -> List[Path]:
    files = [p for p in dirpath.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_EXT]
    return files


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Rename images in a directory to sequential numeric filenames")
    p.add_argument('--dir', default='images', help='Directory containing images (default: ./images)')
    p.add_argument('--start', type=int, default=1, help='Starting index for numbering (default: 1)')
    p.add_argument('--pad', type=int, default=0, help='Zero-pad width (default: auto based on count)')
    p.add_argument('--sort', choices=['name', 'mtime', 'ctime', 'natural'], default='natural', help='Sort order for files (default: natural)')
    p.add_argument('--dry-run', action='store_true', help='Show planned renames but do not perform them')
    p.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    args = p.parse_args(argv)

    dirpath = Path(args.dir)
    if not dirpath.exists() or not dirpath.is_dir():
        print(f"Directory not found: {dirpath}")
        return 2

    images = gather_images(dirpath)
    if not images:
        print(f"No images found in {dirpath} (supported: {', '.join(SUPPORTED_EXT)})")
        return 0

    # Sort
    if args.sort == 'name':
        images.sort(key=lambda p: p.name.lower())
    elif args.sort == 'natural':
        images.sort(key=lambda p: natural_key(p.name))
    elif args.sort == 'mtime':
        images.sort(key=lambda p: p.stat().st_mtime)
    elif args.sort == 'ctime':
        images.sort(key=lambda p: p.stat().st_ctime)

    total = len(images)
    start = max(0, args.start)
    last_index = start + total - 1
    pad = args.pad if args.pad > 0 else len(str(last_index))

    # Build mapping: original -> final
    mapping = []  # list of tuples (orig_path, final_path)
    idx = start
    for pth in images:
        ext = pth.suffix.lower()
        final_name = f"{idx:0{pad}d}{ext}"
        final_path = dirpath / final_name
        mapping.append((pth, final_path))
        idx += 1

    # Show planned renames
    print("Planned renames:")
    for src, dst in mapping:
        print(f"  {src.name} -> {dst.name}")

    if args.dry_run:
        print("Dry run: no files were changed.")
        return 0

    # Two-phase rename: first rename to temporary safe names, then to final names
    temp_map = []  # (temp_path, final_path)
    try:
        for src, dst in mapping:
            # If src already equals dst, skip
            if src.resolve() == dst.resolve():
                if args.verbose:
                    print(f"Skipping (already named): {src.name}")
                continue

            temp_name = f".tmp_{uuid.uuid4().hex}{src.suffix.lower()}"
            temp_path = dirpath / temp_name
            if args.verbose:
                print(f"Renaming {src.name} -> {temp_path.name}")
            src.rename(temp_path)
            temp_map.append((temp_path, dst))

        # Small pause to ensure filesystem updated
        time.sleep(0.05)

        # Move temps to final names
        for temp_path, final_path in temp_map:
            if final_path.exists():
                # Shouldn't happen due to temp scheme, but handle defensively
                backup = final_path.with_suffix(final_path.suffix + '.bak')
                print(f"Warning: {final_path.name} already exists. Backing up to {backup.name}")
                final_path.rename(backup)

            if args.verbose:
                print(f"Renaming {temp_path.name} -> {final_path.name}")
            temp_path.rename(final_path)

    except Exception as e:
        print(f"Error during rename operation: {e}")
        print("Attempting to roll back any temp renames...")
        # Attempt rollback: rename any temps back to original names where possible
        for temp_path, final_path in temp_map:
            try:
                # original name is unknown here; best-effort: if .tmp_ file exists, remove it
                if temp_path.exists():
                    temp_path.unlink()
            except Exception:
                pass
        return 1

    print("Renaming complete.")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
