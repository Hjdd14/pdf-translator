# -*- coding: utf-8 -*-
r"""move_setcounter.py — Phase 4：把环境体内的 \\\setcounter 移到 \begin 之前
用法:
    python move_setcounter.py --chaps 'slides_build/chaps/part*.tex' [--apply]

原因: beamer 的 overlay 机制在定理环境开始时会重置计数器，写在环境体
      （\begin{theorem}[...]\setcounter{theorem}{n}）里的 setcounter 会被覆盖，
      编号显示为 1。移到 \begin 之前即可生效。
注意: 一般无需单独运行——renumber_envs.py 会先删掉旧 setcounter 再重插到
      \begin 之前；此脚本用于处理译者手写在环境体内的情况。
r"""
import argparse, re, io, sys, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ENVS = 'definition|theorem|lemma|corollary|proposition|example|exercise|remark'
PAT = re.compile(
    r'\\begin\{(' + ENVS + r')\}'
    r'(\[[^\]]*\])?[ \t]*\r?\n?[ \t]*\\\setcounter\{\1\}\{(\d+)\}'
)


def rep(m):
    env, opt, n = m.group(1), m.group(2) or '', m.group(3)
    return f'\\setcounter{{{env}}}{{{n}}}\n\\begin{{{env}}}{opt}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chaps', default='slides_build/chaps/part*.tex')
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    tot = 0
    for f in glob.glob(args.chaps):
        t = open(f, encoding='utf-8').read()
        t2, nb = PAT.subn(rep, t)
        if nb:
            if args.apply:
                open(f, 'w', encoding='utf-8').write(t2)
            print(f, nb)
            tot += nb
    print('total', tot, '' if args.apply else '(演练模式：加 --apply 写入)')


if __name__ == '__main__':
    main()
