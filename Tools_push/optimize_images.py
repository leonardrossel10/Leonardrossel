#!/usr/bin/env python3
"""Optimize images: resize, recompress and optionally convert to WebP.

Usage:
  python3 MonSitePhotos_tools/optimize_images.py --root "/path/to/site/images" --max 50 --max-width 1600 --quality 80 --convert-webp --inplace

This script processes the newest images under `--root`, up to `--max`, and
overwrites them when `--inplace` is used (safe because we operate on a copy).
"""
from pathlib import Path
import argparse
from PIL import Image
import sys


def gather_images(root: Path):
    exts = ('.jpg', '.jpeg', '.png', '.webp')
    files = [p for p in root.rglob('*') if p.is_file() and p.suffix.lower() in exts]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files


def ensure_dir(p: Path):
    p.parent.mkdir(parents=True, exist_ok=True)


def optimize_image(src: Path, dest: Path, max_width: int, quality: int, convert_webp: bool):
    try:
        im = Image.open(src)
    except Exception as e:
        print(f"Skipping {src}: open error {e}")
        return False

    if im.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', im.size, (255,255,255))
        background.paste(im, mask=im.split()[-1])
        im = background
    elif im.mode != 'RGB':
        im = im.convert('RGB')

    if max_width and im.width > max_width:
        h = int(max_width * im.height / im.width)
        im = im.resize((max_width, h), Image.LANCZOS)

    # Save optimized JPEG
    dest_jpg = dest.with_suffix('.jpg')
    try:
        ensure_dir(dest_jpg)
        im.save(dest_jpg, 'JPEG', quality=quality, optimize=True, progressive=True)
    except Exception as e:
        print(f"Error saving {dest_jpg}: {e}")
        return False

    if convert_webp:
        dest_webp = dest.with_suffix('.webp')
        try:
            ensure_dir(dest_webp)
            im.save(dest_webp, 'WEBP', quality=quality)
        except Exception as e:
            print(f"Error saving {dest_webp}: {e}")

    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--max', type=int, default=50)
    p.add_argument('--max-width', type=int, default=1600)
    p.add_argument('--quality', type=int, default=80)
    p.add_argument('--out-dir', default=None)
    p.add_argument('--inplace', action='store_true')
    p.add_argument('--root', required=True, help='Images root folder')
    p.add_argument('--convert-webp', action='store_true')
    args = p.parse_args()

    root = Path(args.root)
    if not root.exists():
        print('Root images folder not found:', root)
        sys.exit(1)

    files = gather_images(root)[:args.max]
    if not files:
        print('No images to process in', root)
        return

    for src in files:
        if args.inplace:
            dest = src
        else:
            if args.out_dir:
                dest = Path(args.out_dir) / src.relative_to(root)
            else:
                dest = src.with_suffix('.opt')
        print('Processing', src)
        ok = optimize_image(src, dest, args.max_width, args.quality, args.convert_webp)
        if ok and args.inplace:
            # originals overwritten
            pass

    print('Done')


if __name__ == '__main__':
    main()
