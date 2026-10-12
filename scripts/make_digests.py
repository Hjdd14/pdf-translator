# -*- coding: utf-8 -*-
"""make_digests.py — Phase 3 Step 1：按分片生成逐页 digest（供子智能体翻译）
用法:
    python make_digests.py --pages-json <dir>/pages.json --out-dir <dir> --parts 1-34,35-61,62-99

    --parts 不指定时按 30 页/片自动等分（末片含余数）。
    输出 digest_part01.txt ...，每个文件含 "===== PAGE n =====" + 该页文本。
"""
import argparse, json, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def parse_parts(spec, n):
    if not spec:
        # auto: 30 pages per part
        step = 30
        out = []
        a = 1
        while a <= n:
            out.append((a, min(a + step - 1, n)))
            a += step
        return out
    out = []
    for seg in spec.split(','):
        a, b = seg.split('-')
        out.append((int(a), int(b)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pages-json', required=True)
    ap.add_argument('--out-dir', required=True)
    ap.add_argument('--parts', default='', help='形如 1-34,35-61,62-99')
    args = ap.parse_args()

    data = json.load(open(args.pages_json, encoding='utf-8'))
    n = len(data)
    os.makedirs(args.out_dir, exist_ok=True)
    parts = parse_parts(args.parts, n)
    for k, (a, b) in enumerate(parts, 1):
        path = os.path.join(args.out_dir, f'digest_part{k:02d}.txt')
        with open(path, 'w', encoding='utf-8') as f:
            for d in data[a - 1:b]:
                f.write(f"===== PAGE {d['page']} =====\n{d['text']}\n\n")
        print(f'{path}: pages {a}-{b}')


if __name__ == '__main__':
    main()
