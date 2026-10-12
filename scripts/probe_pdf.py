# -*- coding: utf-8 -*-
"""probe_pdf.py — Phase 1 Step 1：PDF 勘察（页数/文本量/图片/表格/页幅）
用法:
    python probe_pdf.py <source.pdf> [--out report.txt]

输出: 控制台 + 可选报告文件。用于判定：
  - text vs scanned（每页提取字符数）
  - 页幅（判断 slides 16:9 / A4 / letter，决定 LaTeX 版式）
  - 位图数量（决定是否需要 pdfimages 抽图）
  - 表格数量、低文本页清单
"""
import argparse, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pdfplumber


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf')
    ap.add_argument('--out', default=None)
    args = ap.parse_args()

    lines = []
    def say(s=''):
        print(s)
        lines.append(s)

    with pdfplumber.open(args.pdf) as pdf:
        n = len(pdf.pages)
        sizes = {}
        total = 0
        imgs = 0
        tabs = 0
        low = []
        for i, p in enumerate(pdf.pages):
            t = p.extract_text() or ''
            total += len(t)
            imgs += len(p.images)
            tabs += len(p.extract_tables())
            key = (round(p.width, 1), round(p.height, 1))
            sizes[key] = sizes.get(key, 0) + 1
            if len(t.strip()) < 50:
                low.append(i + 1)
        say(f'pages            : {n}')
        say(f'total chars      : {total}')
        say(f'page sizes (pt)  : {sizes}')
        say(f'embedded bitmaps : {imgs}')
        say(f'tables detected  : {tabs}')
        say(f'low-text pages   : {low[:30]}{" ..." if len(low) > 30 else ""}')
        verdict = 'scanned/无文本层' if total / max(1, n) < 50 else 'text(可提取)'
        ratio = (sizes and max(sizes, key=sizes.get)[0] / max(sizes, key=sizes.get)[1]) or 0
        if max(sizes.values()) == n and ratio > 1.5:
            kind = 'slides(宽屏)'
        elif max(sizes.values()) == n and abs(ratio - 0.707) < 0.05:
            kind = 'A4 portrait(讲义)'
        else:
            kind = 'mixed'
        say(f'verdict          : {verdict} / {kind}')

    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print(f'\n报告已写入 {args.out}')


if __name__ == '__main__':
    main()
