# -*- coding: utf-8 -*-
r"""renumber_envs.py — Phase 4：按源 PDF 权威重排定理类环境编号（slides 版）
前置: extract_pages.py 产出 pages.json；译文片段含 "% SRC p<n>" 锚点与
      \begin{definition}/.../ 等环境。
用法:
    python renumber_envs.py --pages-json <dir>/pages.json --chaps <glob>

原理: amsthm 环境开始时自增计数器 => 显示 n 需 \setcounter{env}{n-1}。
      删除译文里已有的 setcounter 行，按 pages.json 的全局出现序列重插。
      备注(Remark) 的「章.序号」小数编号跳过，由 renumber_remarks.py 处理。
r"""
import argparse, re, json, io, sys, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ENVS = ['definition', 'theorem', 'lemma', 'corollary', 'proposition',
        'example', 'exercise']
NAME = {'Definition': 'definition', 'Theorem': 'theorem', 'Lemma': 'lemma',
        'Corollary': 'corollary', 'Proposition': 'proposition',
        'Example': 'example', 'Exercise': 'exercise'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pages-json', required=True)
    ap.add_argument('--chaps', default='slides_build/chaps/part*.tex',
                   help='译文片段 glob（默认 slides_build/chaps/part*.tex）')
    args = ap.parse_args()

    data = json.load(open(args.pages_json, encoding='utf-8'))
    seq = {e: [] for e in ENVS}
    for d in data:
        for m in re.finditer(r'^(Definition|Theorem|Lemma|Corollary|Proposition|Example|Exercise)\\s+(\d+)\b',
                             d['text'], re.M):
            e = NAME[m.group(1)]
            seq[e].append(int(m.group(2)))
    for e in ENVS:
        s = seq[e]
        if not s:
            print(e, 'count 0 (source unused)')
            continue
        assert all(s[i] < s[i + 1] for i in range(len(s) - 1)), (e, s)
        print(e, 'count', len(s), 'range', s[0], '..', s[-1])

    pos = {e: 0 for e in ENVS}
    files = sorted(glob.glob(args.chaps))
    total = 0
    for f in files:
        lines = open(f, encoding='utf-8').read().split('\n')
        out = []
        for ln in lines:
            if re.match(r'\\setcounter\{(%s)\}\{' % '|'.join(ENVS), ln):
                continue
            mb = re.match(r'\s*\\begin\{(%s)\}' % '|'.join(ENVS), ln)
            if mb:
                e = mb.group(1)
                if seq[e]:
                    n = seq[e][pos[e]]
                    pos[e] += 1
                    out.append(f'\\setcounter{{{e}}}{{{n - 1}}}   % align src {e} {n}')
                    total += 1
            out.append(ln)
        open(f, 'w', encoding='utf-8').write('\n'.join(out))
    print('aligned', total, 'envs')


if __name__ == '__main__':
    main()
