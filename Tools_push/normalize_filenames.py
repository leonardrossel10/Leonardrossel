#!/usr/bin/env python3
"""Normalize image filenames: lowercase, replace spaces with underscores, normalize extensions.
Runs in project root; operates on the `images/` tree and on `images/.thumbs/` if present.
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMGROOT = ROOT / 'images'
VALID_EXT = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.mov', '.mp4', '.webm'}

def norm_name(name: str) -> str:
    name = name.replace(' ', '_')
    # collapse multiple underscores
    while '__' in name:
        name = name.replace('__', '_')
    return name.lower()

renames = []

for dirpath, dirnames, filenames in os.walk(IMGROOT, topdown=False):
    pdir = Path(dirpath)
    # rename files
    for f in filenames:
        old = pdir / f
        ext = old.suffix.lower()
        if ext and ext[1:] in {e.strip('.') for e in VALID_EXT}:
            new_name = norm_name(old.stem) + ext
        else:
            # still normalize name but keep extension as-is lowercased
            new_name = norm_name(old.stem) + ext
        new = pdir / new_name
        if old == new:
            continue
        # avoid clobber
        if new.exists():
            # if identical file, remove old
            try:
                if old.stat().st_size == new.stat().st_size:
                    old.unlink()
                    print(f"Removed duplicate {old} -> kept {new}")
                    continue
            except Exception:
                pass
            # otherwise append counter
            base = new.stem
            i = 1
            candidate = pdir / f"{base}_{i}{new.suffix}"
            while candidate.exists():
                i += 1
                candidate = pdir / f"{base}_{i}{new.suffix}"
            new = candidate
        try:
            old.rename(new)
            renames.append((old, new))
            print(f"Renamed: {old.relative_to(ROOT)} -> {new.relative_to(ROOT)}")
        except Exception as e:
            print(f"Failed to rename {old}: {e}")

# Also normalize directory names (lowercase, underscores) from bottom-up
for dirpath, dirnames, filenames in os.walk(IMGROOT, topdown=False):
    pdir = Path(dirpath)
    for d in dirnames:
        oldd = pdir / d
        newd = pdir / norm_name(d)
        if oldd == newd:
            continue
        if newd.exists():
            # merge: move contents of oldd into newd
            try:
                for item in oldd.iterdir():
                    target = newd / item.name
                    if target.exists():
                        # skip or rename
                        print(f"Skipping {item} since {target} exists")
                        continue
                    item.rename(target)
                oldd.rmdir()
                print(f"Merged directory {oldd.relative_to(ROOT)} -> {newd.relative_to(ROOT)}")
            except Exception as e:
                print(f"Failed to merge {oldd}: {e}")
        else:
            try:
                oldd.rename(newd)
                print(f"Renamed dir: {oldd.relative_to(ROOT)} -> {newd.relative_to(ROOT)}")
            except Exception as e:
                print(f"Failed to rename dir {oldd}: {e}")

print('\nNormalization complete.')
