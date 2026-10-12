# -*- coding: utf-8 -*-
r"""renumber_remarks.py — Phase 4：备注(Remark)按源「章.序号」格式重排（slides 版）
用法:
    python renumber_remarks.py --labels 1.1,1.2,2.1,5.8 --chaps <glob>

    --labels: 源 PDF 中 remark 的编号序列（从 pages.json 的 marks 或源文本
               "Remark 1.1" 行读出，按出现顺序，逗号分隔）。
    对每个 \begin{remark} 依次贴上对应标签：\renewcommand{\theremark}{<标签>}，
    并用 \begingroup/\endgroup 局部化，避免污染其他片段。
r"""
import argparse, re, io, sys, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--labels', required=True, help='如 1.1,1.2,2.1,2.2,5.8')
    ap.add_argument('--chaps', default='slides_build/chaps/part*.tex')
    args = ap.parse_args()

    labels = [x for x in args.labels.split(',') if x]
    k = 0
    for f in sorted(glob.glob(args.chaps)):
        lines = open(f, encoding='utf-8').read().split('\n')
        out = []
        for ln in lines:
            if re.match(r'\\\setcounter\{remark\}', ln):
                continue
            m = re.match(r'(\s*)\\begin\{remark\}(\[[^\]]*\])?', ln)
            if m and k < len(labels):
                lab = labels[k]
                k += 1
                num = int(lab.split('.')[1])
                indent, opt = m.group(1), m.group(2) or ''
                out.append(f'{indent}\\begingroup')
                out.append(f'{indent}\\renewcommand{{\\theremark}}{{{lab}}}\\setcounter{{remark}}{{{num - 1}}}')
                out.append(f'{indent}\\begin{{remark}}{opt}')
            elif re.match(r'(\s*)\\end\{remark\}', ln):
                out.append(ln)
                out.append(re.match(r'(\s*)', ln).group(1) + '\\endgroup')
            else:
                out.append(ln)
        open(f, 'w', encoding='utf-8').write('\n'.join(out))
    print('remarks relabeled:', k, 'of', len(labels))


if __name__ == '__main__':
    main()
