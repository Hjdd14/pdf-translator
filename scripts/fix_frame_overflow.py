# -*- coding: utf-8 -*-
"""fix_frame_overflow.py — Phase 4：为内容超高的 beamer frame 自动加 [shrink=n]
用法:
    python fix_frame_overflow.py --log build/main_slides.log --chaps 'slides_build/chaps/part*.tex'

原理: 解析 LaTeX log 的 "Overfull \vbox (Xpt too high) detected at line N"，
      按 log 中 "(./path/partNN.tex" 打开文件标记把 N 归属到正确的片段文件，
      再向上找最近的 \begin{frame} 插入 [shrink=percent]。
      shrink ≈ ceil(X / frame高 × 100) + 2，夹在 [5,60]。
      先清除上一次插入的 shrink（可重复运行）。
"""
import argparse, re, io, sys, glob, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

OPEN_PAT = re.compile(r'\(\.?/?[\w/\\.-]*?(part\d+|chap\d+|ch\d+)[\w/\\.-]*?\.tex')
OVER_PAT = re.compile(r'Overfull \\vbox \((\d+(?:\.\d+)?)pt too high\) detected at line (\d+)')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--log', default='build/main_slides.log')
    ap.add_argument('--chaps', default='slides_build/chaps/part*.tex')
    ap.add_argument('--frame-height', type=float, default=204.0,
                    help='frame 正文高度(pt)，16:9@10pt ≈ 204')
    ap.add_argument('--apply', action='store_true', help='实际写入（否则只演练）')
    args = ap.parse_args()

    # 1) revert previous insertions
    for f in glob.glob(args.chaps):
        t = open(f, encoding='utf-8').read()
        t2 = re.sub(r'\\begin\{frame\}\[shrink=\d+\]', r'\\begin{frame}', t)
        if t2 != t:
            open(f, 'w', encoding='utf-8').write(t2)
    print('reverted previous shrink insertions')

    # 2) parse log with file attribution
    log = open(args.log, encoding='utf-8', errors='ignore').read()
    cur, hits = None, []
    for ln in log.split('\n'):
        m = OPEN_PAT.search(ln)
        if m:
            cur = m.group(1)
        m = OVER_PAT.search(ln)
        if m and cur:
            hits.append((cur, int(m.group(2)), float(m.group(1))))
    print('attributed overfull vboxes:', [(c, n) for c, n, _ in hits])

    # 3) locate frames
    fixes = []
    for stem, texln, pt in hits:
        for path in glob.glob(args.chaps):
            if stem not in path:
                continue
            lines = open(path, encoding='utf-8').read().split('\n')
            for i in range(texln - 1, max(-1, texln - 300), -1):
                if re.match(r'\s*\\begin\{frame\}(\{|\[|$)', lines[i]):
                    shrink = max(5, min(60, math.ceil(pt / args.frame_height * 100) + 2))
                    fixes.append((path, i, shrink, pt, texln))
                    break

    for path, i, shrink, pt, texln in sorted(fixes, key=lambda x: -x[1]):
        lines = open(path, encoding='utf-8').read().split('\n')
        if '[shrink' in lines[i]:
            continue
        rest = lines[i][len(r'\begin{frame}'):]
        lines[i] = f'\\begin{{frame}}[shrink={shrink}]' + rest
        if args.apply:
            open(path, 'w', encoding='utf-8').write('\n'.join(lines))
        print(f'{path}:{i + 1} shrink={shrink} ({pt}pt over, log line {texln})')
    if not args.apply:
        print('\n（演练模式：加 --apply 写入）')


if __name__ == '__main__':
    main()
