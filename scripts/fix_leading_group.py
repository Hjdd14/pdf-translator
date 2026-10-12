# -*- coding: utf-8 -*-
r"""fix_leading_group.py — Phase 4：修 beamer 吞掉前导 {\small X} 分组的问题
现象: frame 首行的 {\small [Palacios-Huerta, ...]} 引用行在编译产物中消失
     （beamer 对 frame 起始处的分组有吞料行为）。
用法:
    python fix_leading_group.py --chaps 'slides_build/chaps/part*.tex' [--apply]

把行首 `{\small X}` 改写为 `\small X\par`。
"""
import argparse, re, io, sys, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chaps', default='slides_build/chaps/part*.tex')
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    n = 0
    for f in sorted(glob.glob(args.chaps)):
        lines = open(f, encoding='utf-8').read().split('\n')
        out, changed = [], 0
        for ln in lines:
            m = re.match(r'^\{\\\small (.+)\}\s*$', ln)
            if m:
                out.append('\\small ' + m.group(1) + '\\par')
                changed += 1
            else:
                out.append(ln)
        if changed:
            if args.apply:
                open(f, 'w', encoding='utf-8').write('\n'.join(out))
            print(f, changed)
            n += changed
    print('total', n, '' if args.apply else '(演练模式：加 --apply 写入)')


if __name__ == '__main__':
    main()
