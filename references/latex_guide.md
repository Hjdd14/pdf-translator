# LaTeX公式编写指南

本指南用于确保PDF翻译过程中数学公式的LaTeX表示正确、规范。

## 基础语法

### 公式模式

| 类型 | 语法 | 示例 |
|------|------|------|
| 行内公式 | `$...$` | `$f(x) = x^2$` |
| 独立公式 | `$$...$$` | `$$\int_0^1 x^2 dx$$` |
| 编号公式 | `\begin{equation}...\end{equation}` | 自动编号 |
| 对齐公式 | `\begin{align}...\end{align}` | 多行对齐 |

### 上下标

| 操作 | 语法 | 渲染效果 |
|------|------|----------|
| 上标 | `x^2` | x的平方 |
| 下标 | `x_i` | x下标i |
| 复合上标 | `x^{n+1}` | x的n+1次方 |
| 复合下标 | `x_{i,j}` | x下标i,j |
| 上下标同时 | `x_i^2` | x下标i的平方 |

### 分式

| 语法 | 说明 |
|------|------|
| `\frac{a}{b}` | 标准分式 a/b |
| `\dfrac{a}{b}` | 显示模式分式（较大） |
| `\tfrac{a}{b}` | 文本模式分式（较小） |
| `a/b` | 行内斜杠分式 |

### 根式

| 语法 | 说明 |
|------|------|
| `\sqrt{x}` | 平方根 |
| `\sqrt[n]{x}` | n次方根 |

## 常用数学符号

### 希腊字母

| 名称 | 小写 | 大写 |
|------|------|------|
| alpha | `\alpha` | — |
| beta | `\beta` | — |
| gamma | `\gamma` | `\Gamma` |
| delta | `\delta` | `\Delta` |
| epsilon | `\epsilon` / `\varepsilon` | — |
| theta | `\theta` / `\vartheta` | `\Theta` |
| lambda | `\lambda` | `\Lambda` |
| mu | `\mu` | — |
| pi | `\pi` | `\Pi` |
| sigma | `\sigma` / `\varsigma` | `\Sigma` |
| phi | `\phi` / `\varphi` | `\Phi` |
| omega | `\omega` | `\Omega` |
| xi | `\xi` | `\Xi` |
| eta | `\eta` | — |
| rho | `\rho` / `\varrho` | — |
| tau | `\tau` | — |
| kappa | `\kappa` | — |
| zeta | `\zeta` | — |
| chi | `\chi` | — |
| psi | `\psi` | `\Psi` |
| nu | `\nu` | — |

### 运算符

| 符号 | 语法 | 说明 |
|------|------|------|
| ± | `\pm` | 正负号 |
| × | `\times` | 乘号 |
| ÷ | `\div` | 除号 |
| ≤ | `\leq` | 小于等于 |
| ≥ | `\geq` | 大于等于 |
| ≠ | `\neq` | 不等于 |
| ≈ | `\approx` | 约等于 |
| ∼ | `\sim` | 相似 |
| ≡ | `\equiv` | 恒等于 |
| ∝ | `\propto` | 正比于 |
| ≪ | `\ll` | 远小于 |
| ≫ | `\gg` | 远大于 |
| ∈ | `\in` | 属于 |
| ∉ | `\notin` | 不属于 |
| ⊂ | `\subset` | 真子集 |
| ⊆ | `\subseteq` | 子集 |
| ∪ | `\cup` | 并集 |
| ∩ | `\cap` | 交集 |
| ∀ | `\forall` | 任意 |
| ∃ | `\exists` | 存在 |
| ¬ | `\neg` | 非 |
| ∧ | `\land` | 与 |
| ∨ | `\lor` | 或 |
| → | `\rightarrow` | 箭头 |
| ⇒ | `\Rightarrow` | 蕴含 |
| ↔ | `\leftrightarrow` | 双向箭头 |
| ⇔ | `\Leftrightarrow` | 等价 |
| ↦ | `\mapsto` | 映射 |
| ∞ | `\infty` | 无穷 |
| ∅ | `\emptyset` | 空集 |
| ∇ | `\nabla` | 纳布拉算子 |
| ∂ | `\partial` | 偏导 |

### 大型运算符

| 符号 | 语法 | 说明 |
|------|------|------|
| ∑ | `\sum` | 求和 |
| ∏ | `\prod` | 求积 |
| ∫ | `\int` | 积分 |
| ∬ | `\iint` | 二重积分 |
| ∭ | `\iiint` | 三重积分 |
| ∮ | `\oint` | 围道积分 |
| lim | `\lim` | 极限 |
| max | `\max` | 最大值 |
| min | `\min` | 最小值 |
| sup | `\sup` | 上确界 |
| inf | `\inf` | 下确界 |

### 函数名（正体）

| 函数 | 语法 | 说明 |
|------|------|------|
| sin | `\sin` | 正弦 |
| cos | `\cos` | 余弦 |
| tan | `\tan` | 正切 |
| log | `\log` | 对数 |
| ln | `\ln` | 自然对数 |
| exp | `\exp` | 指数 |
| det | `\det` | 行列式 |
| dim | `\dim` | 维数 |
| ker | `\ker` | 核 |
| deg | `\deg` | 次数 |
| gcd | `\gcd` | 最大公约数 |
| arg | `\arg` | 辐角 |
| mod | `\mod` | 模 |

## 矩阵与行列式

### 基本语法

```latex
% pmatrix - 圆括号矩阵
\begin{pmatrix}
a_{11} & a_{12} \\
a_{21} & a_{22}
\end{pmatrix}

% bmatrix - 方括号矩阵
\begin{bmatrix}
a_{11} & a_{12} \\
a_{21} & a_{22}
\end{bmatrix}

% vmatrix - 竖线（行列式）
\begin{vmatrix}
a_{11} & a_{12} \\
a_{21} & a_{22}
\end{vmatrix}

% Bmatrix - 花括号矩阵
\begin{Bmatrix}
a_{11} & a_{12} \\
a_{21} & a_{22}
\end{Bmatrix}
```

### 省略号

| 语法 | 效果 | 说明 |
|------|------|------|
| `\cdots` | ⋯ | 水平居中省略号 |
| `\vdots` | ⋮ | 垂直省略号 |
| `\ddots` | ⋱ | 对角省略号 |

### 示例

```latex
$$
A = \begin{pmatrix}
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{n1} & a_{n2} & \cdots & a_{nn}
\end{pmatrix}
$$
```

## 分段函数

```latex
$$
f(x) = \begin{cases}
x^2, & x \geq 0 \\
-x^2, & x < 0
\end{cases}
$$
```

## 对齐公式

```latex
\begin{align}
f(x) &= (x+1)^2 \\
     &= x^2 + 2x + 1 \\
     &= (x^2 + 1) + 2x
\end{align}
```

**带编号的对齐**：每行自动编号，使用 `\notag` 取消编号。

```latex
\begin{align}
a &= b + c \notag \\
  &= d + e
\end{align}
```

## 括号与定界符

| 语法 | 说明 |
|------|------|
| `\left( ... \right)` | 自适应大小的圆括号 |
| `\left[ ... \right]` | 方括号 |
| `\left\{ ... \right\}` | 花括号 |
| `\left\langle ... \right\rangle` | 角括号 |
| `\left\| ... \right\|` | 双竖线（范数） |
| `\left\vert ... \right\vert` | 竖线 |
| `\left. ... \right)` | 单侧括号（`.`表示无） |

## 间距控制

| 语法 | 间距 | 说明 |
|------|------|------|
| `\,` | 3/18 em | 小间距 |
| `\:` | 4/18 em | 中等间距 |
| `\;` | 5/18 em | 大间距 |
| `\quad` | 1 em | 一个字符宽 |
| `\qquad` | 2 em | 两个字符宽 |
| `\!` | -3/18 em | 负间距 |

**积分中的间距**：

```latex
$$\int_0^1 f(x) \, dx$$
```

## 字体样式

| 语法 | 效果 | 说明 |
|------|------|------|
| `\mathbf{x}` | **x** | 粗体 |
| `\mathit{x}` | *x* | 斜体 |
| `\mathrm{x}` | x | 罗马体 |
| `\mathsf{x}` | x | 无衬线体 |
| `\mathtt{x}` | x | 等宽体 |
| `\mathbb{R}` | ℝ | 黑板粗体（数集） |
| `\mathcal{F}` | ℱ | 花体 |
| `\mathfrak{g}` | 𝔤 | 哥特体 |
| `\vec{x}` | x⃗ | 向量箭头 |
| `\hat{x}` | x̂ | 帽号 |
| `\bar{x}` | x̄ | 上划线 |
| `\tilde{x}` | x̃ | 波浪号 |
| `\dot{x}` | ẋ | 一点（时间导数） |
| `\ddot{x}` | ẍ | 两点 |
| `\overline{AB}` | AB̅ | 上划线（长） |
| `\overrightarrow{AB}` | AB→ | 上箭头（长） |

## 常见公式模板

### 二次方程求根公式

```latex
$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$
```

### 泰勒展开

```latex
$$f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!} (x-a)^n$$
```

### 高斯积分

```latex
$$\int_{-\infty}^{\infty} e^{-x^2} \, dx = \sqrt{\pi}$$
```

### 欧拉公式

```latex
$$e^{i\theta} = \cos\theta + i\sin\theta$$
```

### 傅里叶变换

```latex
$$\hat{f}(\xi) = \int_{-\infty}^{\infty} f(x) e^{-2\pi i x \xi} \, dx$$
```

### 麦克斯韦方程组

```latex
\begin{align}
\nabla \cdot \mathbf{E} &= \frac{\rho}{\varepsilon_0} \\
\nabla \cdot \mathbf{B} &= 0 \\
\nabla \times \mathbf{E} &= -\frac{\partial \mathbf{B}}{\partial t} \\
\nabla \times \mathbf{B} &= \mu_0 \mathbf{J} + \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}
\end{align}
```

### 薛定谔方程

```latex
$$i\hbar \frac{\partial}{\partial t} \Psi(\mathbf{r}, t) = \hat{H} \Psi(\mathbf{r}, t)$$
```

## 注意事项

1. **公式中的文本**：使用 `\text{中文}` 包裹，如 `\text{其中 } x \text{ 表示变量}`
2. **空格**：LaTeX公式中的普通空格会被忽略，使用 `\,` `\quad` 等控制间距
3. **特殊字符**：`#` `$` `%` `&` `_` `{` `}` `^` `~` `\` 需要转义（加 `\`）
4. **公式编号**：使用 `\tag{1.1}` 自定义编号
5. **跨页公式**：使用 `\begin{align}` 而非 `$$...$$` 以便跨页
6. **中文环境**：使用ctex宏包时，`\text{}` 中可直接写中文
