#!/usr/bin/env python3
import sys
import json
from pathlib import Path

def normalize(seed_path: Path):
    if not seed_path.exists():
        print(f"No seed file: {seed_path}")
        return 1
    data = json.loads(seed_path.read_text(encoding='utf-8'))
    if not isinstance(data, list):
        print("Unexpected seed format: expected JSON array")
        return 2
    seen = {}
    out = []
    for o in data:
        url = o.get('dataUrl','')
        url = url.replace('/.thumbs/.thumbs/','/.thumbs/')
        url = url.replace('/.thumbs/','/images/')
        o['dataUrl'] = url
        if url in seen:
            continue
        seen[url]=True
        out.append(o)
    seed_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Normalized {len(data)} → {len(out)} entries in {seed_path}")
    return 0

if __name__=='__main__':
    p = Path(sys.argv[1]) if len(sys.argv)>1 else Path('localstorage_seed.json')
    raise SystemExit(normalize(p))
