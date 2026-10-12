<div align="center">

# 📄 PDF Translator

### 把英文 PDF 教材 / 幻灯片，完整翻译成中文 PDF

保持数学公式、表格、图片与版式 —— **逐页一一对应，零缺失**

<br>

<a href="#-快速开始"><img src="https://img.shields.io/badge/XeLaTeX-ctex-2c5282?style=flat-square" alt="XeLaTeX + ctex"></a>
<a href="#-智能体团队"><img src="https://img.shields.io/badge/智能体团队-并行翻译-c0392b?style=flat-square" alt="Agent Team"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-4a5568?style=flat-square" alt="MIT License"></a>
<img src="https://img.shields.io/badge/平台-Windows%20%2F%20macOS%20%2F%20Linux-1a2332?style=flat-square" alt="Platform">

<br><br>

**Beamer 幻灯片** · **A4 讲义** · **扫描件 OCR** · **263 页实测交付**

<br>

<a href="#-快速开始"><b>📥 立即安装 →</b></a> &nbsp;·&nbsp;
<a href="#-工作流程"><b>🔧 工作原理</b></a> &nbsp;·&nbsp;
<a href="#-工具集"><b>🧰 10 个工具</b></a>

</div>

---

## ✨ 这是什么

一个 **Agent Skill**：装进你的 AI 编程助手后，只要说一句

> 「完全翻译这个 PDF，这是 PPT 的 PDF 版，用 LaTeX 编译输出中文版，不可以缺失任何内容」

它就会自动跑完 **勘察 → 解析 → 分片 → 团队并行翻译 → XeLaTeX 编译 → 编号校正 → 门禁验收** 全流程，
交付一本**版式、公式、表格、编号全部对齐原文**的中文 PDF。

<table>
<tr>
<td width="50%" valign="top">

**✅ 它保证做到**

- 📑 逐页 / 逐 frame 一一对应，不丢一条 bullet
- 🧮 数学公式原样保留（`\sum`、矩阵、分段函数…）
- 📊 表格结构复刻，数字不译、文字翻译
- 🖼️ 位图用 `pdfimages` 抽取并挂回原位
- 🔢 「定义 25 / 定理 91」编号与源文件一致
- 🎨 页幅、字号、边距、定理样式按源复刻

</td>
<td width="50%" valign="top">

**⚡ 它怎么提速**

- 按内容主题分片（25–40 页/片）
- 多个子智能体**同时翻译**不同分片
- 写域互斥，零并发冲突
- 实测 263 页幻灯片：团队并行 ≈ 串行的 1/7 时间

**🛡️ 它怎么防错**

- 4 项自动门禁（单元数 / 数字 / 英文残留 / 编号）
- `(cid:xx)` 乱码速查表，公式重组不靠猜
- beamer 七大坑位预置解决方案

</td>
</tr>
</table>

---

## 🚀 快速开始

### 安装到 Claude Code / DeepSeek Harness

```bash
# 克隆到 skills 目录
git clone https://github.com/<your-name>/pdf-translator.git \
      ~/.claude/skills/pdf-translator

# 依赖
pip install pdfplumber          # 文本与表格提取
# poppler-utils（pdfimages / pdftoppm）
#   Windows : conda install poppler   或加入 PATH
#   macOS   : brew install poppler
#   Linux   : sudo apt-get install poppler-utils
# TeX Live / MiKTeX（xelatex + ctex 宏包）
```

装好后直接对 AI 说：

> 用 pdf-translator 翻译 `GameTheorySlidesV2.pdf`，可以用智能体团队加快速度

它会自动询问或判定版式（PPT → Beamer 16:9，讲义 → A4），然后开跑。

### 环境自检

```bash
python scripts/compile_latex.py --check    # xelatex / ctex / pdfplumber
python scripts/probe_pdf.py book.pdf       # 勘察：页幅 / 文本层 / 图片数
```

---

## 🔧 工作流程

<div class="flow">

1. **勘察** — `probe_pdf.py` 判定文本版/扫描版、页幅（幻灯片 or A4）、位图数量，据此选定 Beamer 或 ctexart 版式
2. **解析** — `extract_pages.py` 逐页提取为 `pages.json`，带上 `Definition 3`、`Theorem 5` 等环境标记
3. **分类** — 公式 / 图表 / 表格分区；`(cid:xx)` 乱码按速查表重组为 LaTeX
4. **分片 + 团队并行** — `make_digests.py` 按主题切片，多个子智能体同时翻译，写域互斥
5. **编译与校正** — XeLaTeX 编译 → 修错 → `renumber_envs.py` 对齐编号 → `fix_*.py` 修溢出 → 复编译至 0 error
6. **验收与交付** — `verify_translation.py` 四重门禁 + 逐页视觉抽查 → 交付 `<Name>_中文版.pdf`

</div>

---

## 🧰 工具集

所有脚本都是**通用 CLI 工具**，路径全部参数化，任何项目可直接复用。

| 阶段 | 脚本 | 用途 | 示例 |
|:---:|---|---|---|
| P0 | [`probe_pdf.py`](scripts/probe_pdf.py) | 勘察 PDF：页数/文本量/页幅/图片/表格 | `python scripts/probe_pdf.py book.pdf` |
| P1 | [`extract_pages.py`](scripts/extract_pages.py) | 逐页提取 + 环境标记 → `pages.json` | `python scripts/extract_pages.py book.pdf --out-dir build/extract` |
| P3 | [`make_digests.py`](scripts/make_digests.py) | 按分片生成翻译用 digest | `python scripts/make_digests.py --pages-json build/extract/pages.json --out-dir build/extract --parts 1-34,35-61` |
| P4 | [`compile_latex.py`](scripts/compile_latex.py) | LaTeX 编译 + 环境自检 + 错误提取 | `python scripts/compile_latex.py main.tex --output-dir build --runs 2` |
| P4 | [`renumber_envs.py`](scripts/renumber_envs.py) | 定义/定理/例/练习编号按源重排 | `python scripts/renumber_envs.py --pages-json build/extract/pages.json --chaps 'chapters/part*.tex'` |
| P4 | [`renumber_remarks.py`](scripts/renumber_remarks.py) | Remark「章.序号」编号 | `python scripts/renumber_remarks.py --labels 1.1,2.1,5.8 --chaps 'chapters/part*.tex'` |
| P4 | [`move_setcounter.py`](scripts/move_setcounter.py) | 修 beamer overlay 吞 `\setcounter` | `python scripts/move_setcounter.py --chaps 'chapters/part*.tex' --apply` |
| P4 | [`fix_frame_overflow.py`](scripts/fix_frame_overflow.py) | 按 log 归属自动加 `[shrink=n]` | `python scripts/fix_frame_overflow.py --log build/main.log --chaps 'chapters/part*.tex' --apply` |
| P4 | [`fix_leading_group.py`](scripts/fix_leading_group.py) | 修 beamer 吞行首 `{\small X}` | `python scripts/fix_leading_group.py --chaps 'chapters/part*.tex' --apply` |
| P5 | [`verify_translation.py`](scripts/verify_translation.py) | 四重门禁：单元数/数字/英文/编号 | `python scripts/verify_translation.py --src book.pdf --out build/main.pdf --offset 1` |

---

## 🎯 实测案例

| 指标 | 结果 |
|---|---|
| 源文件 | 263 页 Beamer 幻灯片（博弈论讲义，16:9） |
| 交付 | 264 页中文版（标题页 + 263 页正文） |
| 编译 | **0 error**，overfull > 15pt = **0** |
| 单元对应 | frame **263 / 263** |
| 环境编号 | 定义 1–102 / 定理 5–96 / 引理 35–97 / 推论 18·75 / 例 12–88 / 练习 1–22 全部对齐 |
| 视觉抽查 | 首页 / 表格页 / 矩阵页 / 证明页 / 末页全部通过 |

---

## 📚 仓库结构

```
pdf-translator/
├── SKILL.md                 # 技能主文件（AI 读这份）
├── README.md                # 本文件（人读这份）
├── LICENSE                  # MIT
├── references/              # 术语表与 LaTeX 指南
│   ├── math_terms.md        #   数学术语标准译名
│   ├── physics_terms.md     #   物理术语标准译名
│   └── latex_guide.md       #   LaTeX 公式编写指南
├── scripts/                 # 10 个通用 CLI 工具（见上表）
└── docs/                    # GitHub Pages 演示页
    ├── index.html
    ├── style.css
    └── script.js
```

---

## 🧯 已沉淀的坑位

| 症状 | 原因 | 解法 |
|---|---|---|
| `TeX capacity exceeded` + `\labelenumi` 递归 | `enumitem` 与 beamer 冲突 | preamble 不要加载 enumitem |
| 定理环境不显示编号 | 缺 `\setbeamertemplate{theorems}[numbered]` | 加上 |
| `\setcounter` 无效，编号全是 1 | beamer overlay 在环境开始时重置计数器 | 移到 `\begin{}` 之前 |
| frame 首行 `{\small …}` 引用消失 | beamer 吞掉前导分组 | 改 `\small …\par` |
| `Multiple \tag` 报错 | 一个显示公式写了两个 `\tag` | 拆成两个 `\[ \]` |
| `Option clash for hyperref` | beamer 已加载 hyperref | 删掉重复 `\usepackage` |
| 内容超高被裁 | frame 超出页高 | `[shrink=n]` 或拆帧 |

---

## 🤝 贡献

欢迎 PR：新的 `(cid:xx)` 映射、更多术语表、其他版式适配、bug 修复。

1. Fork 本仓库
2. 新建分支 `feat/xxx`
3. 提交 PR，描述改动动机与实测结果

## 📄 许可

[MIT](LICENSE) © 2026 pdf-translator contributors
