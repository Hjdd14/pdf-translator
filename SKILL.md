---
name: pdf-translator
description: 将英文PDF教材/幻灯片完整翻译为中文PDF，保持原有排版、数学公式和图表。支持 A4 讲义（ctexart）与 16:9 幻灯片（Beamer+ctex）两种版式，支持智能体团队并行分片翻译加速。执行完整的勘察→解析→分类→分片翻译→LaTeX编译→编号校正→验收流程；数学公式保持LaTeX格式不翻译，图表位置保留，表格结构保持但内容翻译，逐页一一对应不缺失。使用此skill当用户要求翻译PDF教材、将英文教材转为中文、翻译学术文档、把PPT的PDF版做成中文版，或提供需要翻译的数学/物理/工程类PDF文件。If the user mentions a PDF file that needs translation, or asks to convert an English textbook to Chinese, use this skill.
---

# PDF教材翻译Skill

将英文PDF教材/幻灯片完整翻译为中文PDF，保持原有排版、数学公式和图表。
**支持两种版式**：A4 讲义（ctexart）与 16:9 幻灯片（Beamer+ctex）。
**支持智能体团队并行翻译**（见 Phase 3），大幅缩短大部头材料的交付时间。

## 核心铁律

```
1. 数学公式保持LaTeX格式，不翻译
2. 图表位置保留，标题翻译
3. 表格结构保持，内容翻译
4. 使用标准学术术语翻译
5. 翻译后必须验证公式完整性和排版质量
6. 逐页/逐单元一一对应：不缺失任何文本、表格、图片
7. 环境编号（定义/定理/例/练习…）必须与源文件一致
8. Phase 3.3 智能体团队并行翻译、Step 5.1 自动门禁、Step 5.2 视觉抽查为**强制步骤**，不得跳过
```

**完成定义**：编译 0 error、门禁通过、视觉抽查确认，三者齐备才算完成；缺一项即未完成。

## 工具索引（scripts/，先调用再动手，不要现写脚本）

> 所有脚本用 `python <脚本> --help` 可看参数。路径一律传参数，不写死。

| 阶段 | 脚本 | 什么时候用 | 例子 |
|---|---|---|---|
| P0 勘察 | `scripts/probe_pdf.py` | 拿到 PDF 第一步 | `python scripts/probe_pdf.py book.pdf --out report.txt` |
| P1 提取 | `scripts/extract_pages.py` | 文本版 PDF，产出 pages.json | `python scripts/extract_pages.py book.pdf --out-dir build/extract` |
| P3 分片 | `scripts/make_digests.py` | 派发子智能体前生成 digest | `python scripts/make_digests.py --pages-json build/extract/pages.json --out-dir build/extract --parts 1-34,35-61` |
| P4 编译 | `scripts/compile_latex.py` | LaTeX → PDF（自带环境检查） | `python scripts/compile_latex.py main.tex --output-dir build --runs 2` |
| P4 编号 | `scripts/renumber_envs.py` | 定义/定理等编号与源对齐 | `python scripts/renumber_envs.py --pages-json build/extract/pages.json --chaps 'chapters/part*.tex'` |
| P4 备注 | `scripts/renumber_remarks.py` | Remark 的「章.序号」编号 | `python scripts/renumber_remarks.py --labels 1.1,2.1,5.8 --chaps 'chapters/part*.tex'` |
| P4 setcounter | `scripts/move_setcounter.py` | 译者把 setcounter 写进环境体内 | `python scripts/move_setcounter.py --chaps 'chapters/part*.tex' --apply` |
| P4 超高 | `scripts/fix_frame_overflow.py` | beamer frame 内容溢出 | `python scripts/fix_frame_overflow.py --log build/main.log --chaps 'chapters/part*.tex' --apply` |
| P4 前导组 | `scripts/fix_leading_group.py` | beamer 吞掉行首 `{\small X}` | `python scripts/fix_leading_group.py --chaps 'chapters/part*.tex' --apply` |
| P5 验收 | `scripts/verify_translation.py` | 最终门禁（一脚本四检查） | `python scripts/verify_translation.py --src book.pdf --out build/main.pdf --offset 1` |

## 触发指令（标准请求 → 无条件全流程执行）

以下请求是本 skill 的**标准触发形态**。一旦出现（无论用户是否逐字说出每一条），**不要反问、不要裁剪流程**，直接按本 skill 全流程执行：

> 「完全翻译这个pdf，这是一个ppt的pdf版本，使用latex编译输出新的pdf，要求不可以缺失任何文本，表格，图片，尽可能完全还原教材，制作出一个中文版，对于无法使用python读取的内容，你可以使用视觉理解。给出一个完整计划，可以使用智能体团队加快速度」

### 强制动作清单（每一项都是必做，不是可选项）

| # | 动作（无条件执行） | 手段 / 工具 |
|---|---|---|
| 1 | **完全翻译**：Phase 0–5 全流程，逐页一一对应 | 本文件全流程 |
| 2 | **PPT 版式**：勘察判定为 slides → Beamer 16:9，**每源页一个 frame** | `scripts/probe_pdf.py` → Phase 3-S |
| 3 | **LaTeX 编译输出**：XeLaTeX + ctex 编译，交付 `<Name>_中文版.pdf` | `scripts/compile_latex.py` |
| 4 | **零缺失**：任何文本、表格、图片都不得丢失 | `scripts/verify_translation.py` 门禁 + 逐页核对 digest + 视觉抽查 |
| 5 | **完全还原**：页幅 / 字号 / 边距 / 环境样式 / 编号全部按源复刻 | Phase 4 + `renumber_envs.py` / `renumber_remarks.py` |
| 6 | **视觉理解兜底**：python 提取失败或乱码的页 → 转图后 Read 工具识别 | `pdftoppm -png -r 300` + Step 1.3 + Phase 2 `(cid:xx)` 重组表 |
| 7 | **先给完整计划**：动手翻译前先输出分片方案与验收标准 | 本文件 Phase 0–5 即是计划模板，先陈述再执行 |
| 8 | **智能体团队并行加速**：按内容主题分片、并行派发 subagent、写域互斥 | Phase 3.3 编排（`make_digests.py` + 并行 subagent） |

> **执行纪律**：第 1–8 项全部执行完毕才算完成；任一项跳过即视为未完成。用户明确要求「精简/只翻某几章」时方可裁剪，但需在交付说明中注明裁剪范围。

## 工作流总览

```
Phase 0: 勘察（probe_pdf.py）→ 判定 text/scanned、页幅、图片数
   ↓
Phase 1: 内容解析（extract_pages.py / pdfimages）
   ↓
Phase 2: 内容分类标记（结构化 JSON，公式/图表/表格分区）
   ↓
Phase 3: 分片 + 智能体团队并行翻译（make_digests.py + subagent 编排）
   ↓
Phase 4: LaTeX 编译与编号校正（compile_latex.py / renumber_* / fix_*）
   ↓
Phase 5: 验证与交付（verify_translation.py + 视觉抽查）
```

---

## Phase 0: 勘察（必做）

```bash
python scripts/probe_pdf.py <source.pdf> --out report.txt
```

据输出决定版式与策略：

| 勘察结果 | 版式 | 说明 |
|---|---|---|
| `slides(宽屏)`（页幅比 >1.5，如 453×255pt） | **Beamer**，每源页一个 `\begin{frame}` | 走 Phase 3-Slides |
| `A4 portrait(讲义)` | **ctexart** | 走 Phase 3-Book |
| `scanned/无文本层` | 任选，先转图（Step 1.3）再用视觉识别 | OCR 或直接 Read 页面图 |
| `embedded bitmaps > 0` | 用 `pdfimages` 抽图（Step 1.4） | 图片必须逐一挂回译文 |

---

## Phase 1: 内容解析

### Step 1.1: 判断PDF类型

```python
import pdfplumber
with pdfplumber.open("textbook.pdf") as pdf:
    text = pdf.pages[0].extract_text()
    pdf_type = "scanned" if len(text.strip()) < 50 else "text"
```

### Step 1.2: 文本PDF解析（用工具）

```bash
python scripts/extract_pages.py textbook.pdf --out-dir build/extract
# 产出 build/extract/pages.json: [{page, text, marks, width, height}]
# marks 例: ["definition:3", "theorem:5", "example:12", "recall:"]
```

`marks` 是后续**编号权威重排**的依据（renumber_envs.py 依赖它），务必先跑。

### Step 1.3: 扫描版PDF解析

```python
from pdf2image import convert_from_path
images = convert_from_path('scanned.pdf', dpi=300)
for i, image in enumerate(images):
    image.save(f'page_{i+1:03d}.png', 'PNG')
```

之后用 Read 工具逐页读取图片，视觉识别文字与公式并转 LaTeX。

### Step 1.4: 提取图表

```bash
mkdir -p figures
pdfimages -png source.pdf figures/prefix
# 输出: figures/prefix-000.png ... 跳号正常；smask 蒙版图可忽略
```

- 提取后用 Read 工具查看每张图，确认对应哪个 Figure 编号
- Windows: `conda install poppler` 或下载 poppler for Windows 加入 PATH

### Step 1.5: 进度记录

记录：PDF类型、总页数、每页文本长度、表格数量、图表数量（写入 report.txt）。

---

## Phase 2: 内容分类标记

### Step 2.1: 识别数学公式

常见模式：
- 独立成行的公式（居中、缩进）
- 行内公式（含 =, +, ∑, ∫, ∂ 等）
- PDF 文本层碎裂：上下标分行、`(cid:xx)` 乱码 —— **必须按数学常识重组**

```python
import re
formula_patterns = [
    r'^\s*[A-Za-z]\s*=\s*',
    r'^\s*\\[A-Za-z]',
    r'^\s*[∑∏∫∮∂∇]',
]
```

### Step 2.2: (cid:xx) 乱码速查（pdfTeX 源常见）

| 乱码 | 含义 |
|---|---|
| `(cid:80)` `(cid:88)` | `\sum` |
| `(cid:82)` `(cid:90)` | `\int` |
| `(cid:18)(cid:19)` | 圆括号向量 `pmatrix` |
| `(cid:16)(cid:17)` | `\binom` |
| `(cid:40)(cid:41)` | `\begin{cases}` |
| `(cid:110)(cid:111)` | `\{ \}` |
| `(cid:2)` | `\times` |
| `(cid:20)` `(cid:21)` | `\leq` `\geq` |
| `(cid:24)` | `\sim`（等价关系） |
| `(cid:0)` `(cid:1)` | `-`（减号/负号） |
| `ˆ` `¯` | `\hat{}` `\bar{}` |
| `∥` | `\Vert`（偏离记号 s∥s′_i） |
| `̸=` | `\neq` |
| `T` 上标 | `^{\mathsf T}` 转置 |

### Step 2.3: 结构化表示

```json
{
  "page": 5,
  "blocks": [
    {"type": "heading", "content": "Equilibrium", "translate": true},
    {"type": "formula", "latex": "H_i(s\\Vert s'_i) \\le H_i(s)", "translate": false},
    {"type": "figure", "image_path": "figures/prefix-000.png", "caption_translate": true},
    {"type": "table", "headers": ["x", "f(x)"], "rows": [["0", "1"]], "content_translate": true}
  ]
}
```

### Step 2.4: 公式LaTeX化

- 行内 `$...$`；独立 `\[...\]` 或 `equation`
- 编号公式用 `\tag{}`；对齐用 `aligned`
- **每个显示公式只能有一个 `\tag{}`**（amsmath "Multiple \tag" 错误）；两个编号公式拆成两个 `\[ \]`

---

## Phase 3: 学术翻译处理

### Step 3.1: 翻译规则

**必须翻译**：章节标题、正文段落、公式描述文字（"where x represents…"→"其中 x 表示…"）、图表标题、表格文字、脚注注释。

**不翻译**：数学公式本身、变量名、数学常数（π, e）、函数名（sin, cos, log）、人名与文献条目（Nash、Shapley、[Palacios-Huerta (2003)…]）。

### Step 3.2: 学术翻译原则

术语标准化：严格使用 `references/math_terms.md` / `references/physics_terms.md`；未收录术语可自拟，但**必须登记**（在最终交付说明里列「自拟术语表」）。

风格：准确、严谨、一致、可读；被动语态转中文主动/无主语句（"It is shown that…"→"研究表明…"）。

### Step 3.3: 分片 + 智能体团队并行翻译（强制，加速关键）

**适用**：页数 ≥ 40 或明确要求「用智能体团队加快速度」。分片原则：**按内容主题切**，每片 25–40 页，片间**写域互不重叠**（各写一个文件），避免并发冲突。

```bash
# 1) 生成各片 digest（含 ===== PAGE n ===== 锚点）
python scripts/make_digests.py --pages-json build/extract/pages.json \
    --out-dir build/extract --parts 1-34,35-61,62-99
```

2) **同一消息内并行派发**若干 subagent（互不依赖才能并行），每个 subagent 的 prompt 必须包含：

- 输入 digest 文件绝对路径 + 术语表路径（`TERMS.md` 或 references/）
- **唯一输出文件**（写域互斥声明：「只准写这一个文件，不得改动其他任何文件」）
- 格式规范（见下方 Phase 3-S / 3-B 模板）
- `% SRC p<n>` 锚点要求（每单元前标注源页码，供逐页核对与编号重排）
- 完整性要求：逐页核对，不得跳页跳条目；frame/单元数 = 分片页数
- 回报格式：frame 数、编号校正情况、不确定术语

3) 派发前先写好 `preamble` 与主文件骨架（Lead 独占，translator 只读），保证术语宏、字体、定理环境一致。

#### Phase 3-Slides 模板（Beamer，每源页一 frame）

```latex
% SRC p<n>
\begin{frame}{<源页首行标题的中译>}
\begin{itemize}
  \item ...
\end{itemize}
\begin{definition}[<括注中译>]
  ...
\end{definition}
\end{frame}
```

要点：
- 无标题的延续页用 `\begin{frame}` 空标题，列表重开
- 页码行（`5/263`）不包含
- 定义/定理/引理/推论/例/练习/备注用环境；编号错位由 Lead 用 renumber_envs.py 统一修，译者只需按源写内容
- `Pf.` → `\begin{proof}`；`Soln.` → `{\bfseries 解}…\qed`（或自定义 solution 环境，自动补 QED）
- 表格用 `booktabs` 的 `tabular` 复刻，数字不译
- 跨页证明用 `\begin{proof}[证明（续）]` 承接

#### Phase 3-Book 模板（A4 讲义）

- `\section/\subsection/\subsubsection` 对应源层级
- 源文件各章不另起新页就不要强加 `\clearpage`
- 定理类环境：粗体标题 + 斜体正文（中文映射楷体）+ 标题后无句点
- 数学字体保持 Computer Modern（不得替换）

---

## Phase 4: LaTeX/XeLaTeX PDF生成

### Step 4.1: 生成LaTeX源文件

**讲义版**（ctexart）：

```latex
\documentclass[10pt,a4paper]{ctexart}
\usepackage[UTF8]{ctex}
\usepackage{amsmath,amssymb,amsfonts,mathtools}
\usepackage{booktabs,array,multirow,makecell,longtable}
\usepackage{geometry}
\geometry{left=2cm,right=2cm,top=3.2cm,bottom=2.95cm}
\setCJKmainfont{SimSun}
\setCJKsansfont{SimHei}
\usepackage[hidelinks,unicode]{hyperref}
\begin{document}
\section{引言}
...
\end{document}
```

**幻灯片版**（Beamer，16:9）：

```latex
\documentclass[aspectratio=169,10pt]{beamer}
\usepackage[UTF8,fontset=windows]{ctex}
\usepackage{amsmath,amssymb,amsfonts,mathtools,amsthm}
\usepackage{booktabs,array,multirow,makecell}
\usetheme{default}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}[frame number]
\usefonttheme{professionalfonts}
\setCJKmainfont{SimSun}
\setCJKsansfont{SimHei}
\setbeamertemplate{theorems}[numbered]   % ← 关键：否则定理不显示编号
% 定理环境（beamer 已预定义同名宏，先清除再建，计数器名=环境名）
\makeatletter
\let\theorem\@undefined \let\endtheorem\@undefined
\expandafter\let\csname c@theorem\endcsname\@undefined
\expandafter\let\csname p@theorem\endcsname\@undefined
\expandafter\let\csname thetheorem\endcsname\@undefined
\makeatother
\newtheorem{theorem}{定理}
% definition/lemma/corollary/proposition/example/exercise/remark 同理
\renewcommand{\proofname}{证明}
\begin{document}
\input{preamble_slides}   % 或直接内联
\input{chapters/part01}
...
\end{document}
```

> **beamer 坑位速查**（实测）：
> 1. **不要加载 `enumitem`** —— 与 beamer 冲突导致 `\labelenumi` 递归、TeX capacity exceeded
> 2. `\setbeamertemplate{theorems}[numbered]` 不加则定理环境**不显示编号**
> 3. `\setcounter` 写在定理环境**体内**会被 overlay 机制覆盖 → 用 move_setcounter.py 修
> 4. frame 首行的 `{\small X}` 分组会被吞 → 用 fix_leading_group.py 修
> 5. 一个显示公式只能一个 `\tag{}`
> 6. beamer 已加载 hyperref，重复 `\usepackage{hyperref}` 报 Option clash
> 7. 内容超高的 frame 用 `[shrink=n]`（fix_frame_overflow.py 自动加）

### Step 4.2: 内容转换

标题层级、公式、图片（`\includegraphics`）、表格（`booktabs`）按 Phase 3 模板处理；图片引用 `figures/` 目录，编号与源 Figure 对应。

### Step 4.3: 编译PDF

```bash
# 方式一：工具（自带 xelatex/ctex 环境检查）
python scripts/compile_latex.py main.tex --output-dir build --runs 2 --check

# 方式二：直接编译（编译两遍）
xelatex -interaction=nonstopmode -output-directory=build main.tex
xelatex -interaction=nonstopmode -output-directory=build main.tex
```

**编译前检查**：`figures/` 与 .tex 同目录；所有 `\includegraphics` 文件存在；中文字体已装（Windows: SimSun/SimHei；Linux: `fonts-noto-cjk`）。

**编译后修复顺序**：
1. `!` 错误 → 修到 0（语法/字体/路径/宏冲突，见 Step 4.5 表）
2. `Overfull \vbox` → `python scripts/fix_frame_overflow.py --log build/main.log --chaps '...' --apply`
3. 编号错位 → `python scripts/renumber_envs.py --pages-json ... --chaps '...'`
4. Remark「章.序号」→ `python scripts/renumber_remarks.py --labels <源序列> --chaps '...'`
5. 复编译，重复 1–4 直到 0 error、无大溢出

### Step 4.4: 字体配置

| 字体 | 用途 | 文件 |
|---|---|---|
| 宋体 SimSun | 正文 | simsun.ttc |
| 黑体 SimHei | 标题/加粗 | simhei.ttf |
| 仿宋 FangSong | 等宽 | simfang.ttf |
| 楷体 KaiTi | 定理斜体映射 | simkai.ttf |

位于 `C:\Windows\Fonts\`。Linux 装 `fonts-noto-cjk`。

### Step 4.5: 处理编译错误

| 错误 | 原因 | 解决方案 |
|---|---|---|
| `Undefined control sequence` | 宏未定义/包缺失 | 补 `\usepackage` 或改用 `\operatorname{}` |
| `Font ... not found` | 字体缺失 | 装字体或改 `\setCJKmainfont` |
| `Overfull \hbox` | 行宽溢出 | 调整公式换行或 `\emergencystretch` |
| `Missing $ inserted` | 公式标记缺失 | 检查 `$`/`\[`配对 |
| `File ... not found` | 图片路径错 | 检查 figures/ 路径 |
| `Command \X already defined` | 与 beamer 预定义宏重名 | `\let\X\@undefined` 后重建 |
| `TeX capacity exceeded` + `\labelenumi` | enumitem 与 beamer 冲突 | 移除 enumitem |
| `Multiple \tag` | 一个公式两个 tag | 拆成两个显示公式 |
| `Option clash for hyperref` | beamer 已加载 | 删掉重复 usepackage |

---

## Phase 5: 验证与交付

### Step 5.1: 自动门禁（强制，用工具）

```bash
python scripts/verify_translation.py --src <source.pdf> --out build/main.pdf \
    --chaps 'chapters/part*.tex' --offset 1
```

- `--offset`：译页相对源页偏移（标题页 `\maketitle` 占 1 页时传 1；讲义逐章对应时传 0）
- 检查 G1 单元数 / G2 数字多重集 / G3 残留英文 / G4 环境编号
- **G2/G4 的已知可容忍项**：小整数下标碎片（`H_i` 的 i 等在文本层脱离）、证明标题与交叉引用（「定理 26 的证明」「由定理 32」）——人工抽查确认后放行

### Step 5.2: 视觉抽查（强制）

```bash
pdftoppm -png -r 110 -f <源页> -l <源页> source.pdf qa/src
pdftoppm -png -r 110 -f <译页> -l <译页> build/main.pdf qa/out
```

用 Read 工具对照源页/译页截图，至少覆盖：首页、含表格页、含矩阵页、证明页、末页。

### Step 5.3: 翻译质量检查

- [ ] 术语一致（自拟术语已登记）
- [ ] 公式描述文字准确
- [ ] 无未译段落（G3 白名单外英文词已逐个人工核对）
- [ ] 中文表达流畅、学术语气

### Step 5.4: 最终交付

| 文件 | 说明 |
|---|---|
| `<Name>_中文版.pdf` | 最终中文PDF |
| `main.tex` / `preamble*.tex` | LaTeX 源文件 |
| `chapters/part*.tex` | 分片译文（带 `% SRC p<n>` 锚点） |
| `build/extract/pages.json` + `digest_part*.txt` | 提取与分片中间产物 |
| `TERMS.md` | 术语对照总表（权威） |
| `qa/` | 验收截图与报告 |

---

## 智能体团队编排速查（Phase 3）

```
Lead:
  1. probe_pdf.py 勘察 → extract_pages.py 提取
  2. 写 preamble + main 骨架（术语宏/字体/定理环境，独占写域）
  3. make_digests.py 分片
  4. 同一消息并行派发 N 个 subagent（每片一个，写域互斥）
  5. 收齐后：compile_latex.py → 修错 → renumber_envs/remarks → fix_* → 复编译
  6. verify_translation.py 门禁 + 视觉抽查 → 交付
subagent（每片）:
  输入: digest_partNN.txt + TERMS.md + 格式规范
  输出: chapters/partNN.tex（唯一写文件），每单元带 % SRC p<n>
  回报: 单元数 / 编号校正 / 不确定术语
```

## 参考文件

- `references/math_terms.md` — 数学术语标准译名对照表
- `references/physics_terms.md` — 物理术语标准译名对照表
- `references/latex_guide.md` — LaTeX公式编写指南

## 辅助脚本

- `scripts/compile_latex.py` — LaTeX编译辅助脚本（环境检查+编译+错误提取）
- 其余 9 个脚本见上方「工具索引」
