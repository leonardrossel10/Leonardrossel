#!/usr/bin/env python3
import sys
from pathlib import Path

def validate(seed_path: Path):
    if not seed_path.exists():
        print(f"No seed file: {seed_path}")
        return 1
    text = seed_path.read_text(encoding='utf-8')
    if '/.thumbs/' in text:
        print('ERROR: seed contains "/.thumbs/" entries')
        for line in text.splitlines():
            if '/.thumbs/' in line:
                print('  ', line.strip())
        return 2
    print('OK: no /.thumbs/ found in seed')
    return 0

if __name__=='__main__':
    p = Path(sys.argv[1]) if len(sys.argv)>1 else Path('localstorage_seed.json')
    raise SystemExit(validate(p))
