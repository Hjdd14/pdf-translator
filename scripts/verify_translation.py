# -*- coding: utf-8 -*-
r"""verify_translation.py - Phase 5 gate: translated PDF vs source PDF
Usage:
    python verify_translation.py --src <source.pdf> --out <output.pdf> \
        [--chaps 'slides_build/chaps/part*.tex'] [--offset 1] [--en-allow words.txt]

检查项:
    G1  单元数 vs 源页数（beamer: \begin{frame} 数；article: \\section+输入页）
    G2  逐页数字字面量多重集（自动剔除 (cid:xx) 噪声与页码行）
    G3  残留英文审计（白名单外英文词 top 40，供人工判定）
    G4  定理类环境编号逐页比对（源 "Theorem 12" vs 译 "定理 12"）

    --offset: 译页相对源页的偏移（标题页 \maketitle 使译页 = 源页 + 1 时传 1）
    --en-allow: 可选，每行一个允许保留的英文词
退出码: 0 = 全部通过；1 = 有 FAIL 项。
r"""
import argparse, io, re, sys, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pdfplumber

DEFAULT_ALLOW = set('''
von Neumann Morgenstern Nash Shapley Shubik Vorobev Vorob'ev Petrosyan Zenkevich
Birmingham Zhang Palacios Huerta Brouwer Banzhaf
Game Theory GTMCD Springer World Scientific Rev Econ Stud
Definition Theorem Lemma Corollary Proposition Example Exercise Remark Proof Recall
Pf Soln Problem Notes Solution References
max min sup inf argmax argmin iff LP IIA vN-M NA
s.t. e.g. i.e. aka et al
'''.split())

ZH = {'定义': 'definition', '定理': 'theorem', '引理': 'lemma', '推论': 'corollary',
      '命题': 'proposition', '例': 'example', '练习': 'exercise', '备注': 'remark'}
EN = {'Definition': 'definition', 'Theorem': 'theorem', 'Lemma': 'lemma',
      'Corollary': 'corollary', 'Proposition': 'proposition', 'Example': 'example',
      'Exercise': 'exercise', 'Remark': 'remark'}

fail = 0


def pages(path):
    with pdfplumber.open(path) as pdf:
        return [p.extract_text() or '' for p in pdf.pages]


def nums(t):
    return re.findall(r'\d+(?:\.\d+)?', t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--chaps', default='slides_build/chaps/part*.tex')
    ap.add_argument('--offset', type=int, default=1)
    ap.add_argument('--en-allow', default=None)
    args = ap.parse_args()

    allow = set(DEFAULT_ALLOW)
    if args.en_allow:
        allow |= {w.strip() for w in open(args.en_allow, encoding='utf-8') if w.strip()}

    src = pages(args.src)
    out = pages(args.out)
    print(f'src pages={len(src)}  out pages={len(out)}  offset={args.offset}')

    # ---------- G1 ----------
    import glob
    frames = 0
    for f in glob.glob(args.chaps):
        frames += len(re.findall(r'\\begin\{frame\}',
                                 open(f, encoding='utf-8').read()))
    ok = frames == len(src)
    print(f'G1 frames={frames} vs src={len(src)} -> {"PASS" if ok else "FAIL"}')
    globals()['fail'] += 0 if ok else 1

    # ---------- G2 ----------
    cid = re.compile(r'\(cid:\d+\)')
    bad_pages = []
    for i, sp in enumerate(src):
        j = i + args.offset
        op = out[j] if 0 <= j < len(out) else ''
        sp2, op2 = cid.sub('', sp), cid.sub('', op)
        sn = collections.Counter(nums(sp2))
        on = collections.Counter(nums(op2))
        # 页码行剔除：源页脚 "n/N"，译页脚 "n/M"（N、M 各自总页数）
        sn[str(len(src))] = max(0, sn.get(str(len(src)), 0) - 1)
        on[str(len(out))] = max(0, on.get(str(len(out)), 0) - 1)
        sn[str(i + 1)] = max(0, sn.get(str(i + 1), 0) - 1)
        on[str(j + 1)] = max(0, on.get(str(j + 1), 0) - 1)
        miss = {k: v - on.get(k, 0) for k, v in sn.items() if v - on.get(k, 0) > 0}
        if miss:
            bad_pages.append((i + 1, miss))
    print(f'G2 numeric-missing pages={len(bad_pages)}'
          f' -> {"PASS(仅下标碎片)" if len(bad_pages) == 0 else "REVIEW"}')
    agg = collections.Counter()
    for _, m in bad_pages:
        agg.update(m)
    if agg:
        print('   top missing kinds:', agg.most_common(12))
        for p, m in bad_pages[:10]:
            print('   p', p, dict(m))

    # ---------- G4 ----------
    pat_en = re.compile(r'(Definition|Theorem|Lemma|Corollary|Proposition|Example|Exercise|Remark)\s+(\d+(?:\.\d+)?)')
    pat_zh = re.compile(r'(' + '|'.join(ZH) + r')\s+(\d+(?:\.\d+)?)')
    mism = []
    for i, sp in enumerate(src):
        j = i + args.offset
        op = out[j] if 0 <= j < len(out) else ''
        s = [(EN[m.group(1)], m.group(2)) for m in pat_en.finditer(sp)]
        o = [(ZH[m.group(1)], m.group(2)) for m in pat_zh.finditer(op)
             if '的证明' not in op[m.end():m.end() + 8]]
        s = [x for x in s if re.fullmatch(r'\d+(\.\d+)?', x[1])]
        o = [x for x in o if re.fullmatch(r'\d+(\.\d+)?', x[1])]
        if s != o:
            mism.append((i + 1, s, o))
    ok = not mism
    print(f'G4 env-number mismatched pages={len(mism)} -> {"PASS" if ok else "REVIEW"}')
    for p, s, o in mism[:15]:
        print(f'   p{p}: src={s} out={o}')

    # ---------- G3 ----------
    words = re.findall(r"[A-Za-z][A-Za-z'\-]{3,}", '\n'.join(out))
    c = collections.Counter(w for w in words if w not in allow)
    print('G3 residual English (top 25, 人工核对):')
    for w, n in c.most_common(25):
        print('   ', w, 'x', n)

    sys.exit(0 if fail == 0 else 1)


if __name__ == '__main__':
    main()
