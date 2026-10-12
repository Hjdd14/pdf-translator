# -*- coding: utf-8 -*-
"""extract_pages.py — Phase 1 Step 2：逐页提取为 JSON（文本+环境标记+页幅）
用法:
    python extract_pages.py <source.pdf> --out-dir <dir>

产出 <out-dir>/pages.json : [{page, text, marks, width, height}]
  marks 例: ["definition:3", "theorem:5", "example:12", "recall:", ...]
  用于后续分片、编号重排（renumber2/3）与逐页校验（slides_gate2）。
"""
import argparse, json, io, re, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def _need_pdfplumber():
    """惰性导入：让 --help / 参数校验在未装 pdfplumber 时也能工作。"""
    try:
        import pdfplumber  # noqa: F401
        return pdfplumber
    except ImportError:
        sys.stderr.write(
            '错误: 需要 pdfplumber。安装: pip install pdfplumber\n')
        sys.exit(2)

PATTERNS = [
    (r'^Definition\s*(\d*)', 'definition'),
    (r'^Theorem\s*(\d*)', 'theorem'),
    (r'^Lemma\s*(\d*)', 'lemma'),
    (r'^Corollary\s*(\d*)', 'corollary'),
    (r'^Proposition\s*(\d*)', 'proposition'),
    (r'^Remark\s*(\d*)', 'remark'),
    (r'^Example\s*(\d*)', 'example'),
    (r'^Exercise\s*(\d*)', 'exercise'),
    (r'^Recall\s*(\d*)', 'recall'),
    (r'^Problem\s*(\d*)', 'problem'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf')
    ap.add_argument('--out-dir', required=True)
    args = ap.parse_args()

    data = []
    pdfplumber = _need_pdfplumber()
    with pdfplumber.open(args.pdf) as pdf:
        for i, p in enumerate(pdf.pages):
            t = p.extract_text() or ''
            marks = []
            for pat, name in PATTERNS:
                m = re.search(pat, t, re.M)
                if m:
                    marks.append(name + ':' + (m.group(1) or ''))
            data.append({'page': i + 1, 'text': t, 'marks': marks,
                         'width': p.width, 'height': p.height})
    out = os.path.join(args.out_dir, 'pages.json')
    os.makedirs(args.out_dir, exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f'wrote {out}  ({len(data)} pages)')


if __name__ == '__main__':
    main()
