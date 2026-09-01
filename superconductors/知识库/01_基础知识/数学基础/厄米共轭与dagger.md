---
tags: [数学, 线性代数, 二次量子化]
created: 2026-07-26
---

# 厄米共轭与 dagger (†)

## 一句话定义

dagger (†) 就是**厄米共轭**——对矩阵或向量先转置、再取复共轭：$A^\dagger \equiv (A^*)^T = (A^T)^*$。两种操作顺序不重要，结果相同。

---

## 基础定义

### 复共轭 $z^*$

对复数 $z = a + bi$（$a, b \in \mathbb{R}$），$z^* = a - bi$。几何上是在复平面做关于实轴的反射。

### 转置 $A^T$

对矩阵 $A$，$(A^T)_{ij} = A_{ji}$——行列互换。

### 厄米共轭 $A^\dagger$

两步操作合在一起：$A^\dagger = (A^*)^T$。

对向量 $\mathbf{v}$，$\mathbf{v}^\dagger$ 得到一个行向量，每个分量取了复共轭。

---

## 关键代数性质

| 性质 | 公式 | 物理对应 |
|------|------|----------|
| 对合 | $(A^\dagger)^\dagger = A$ | dagger 两次回到原算符 |
| 乘积反转 | $(AB)^\dagger = B^\dagger A^\dagger$ | $(c_1 c_2)^\dagger = c_2^\dagger c_1^\dagger$ |
| 线性叠加 | $(\alpha A + \beta B)^\dagger = \alpha^* A^\dagger + \beta^* B^\dagger$ | 组合算符的 dagger |
| Kronecker 积 | $(A \otimes B)^\dagger = A^\dagger \otimes B^\dagger$ | 多轨道构造 |
| 内积 | $\langle u \vert v \rangle = u^\dagger v$ | bra = ket 的 dagger |

**乘积反转性质**是计算中最常用的。比如跳跃项 $c_i^\dagger c_j$ 的 dagger：
$$(c_i^\dagger c_j)^\dagger = c_j^\dagger (c_i^\dagger)^\dagger = c_j^\dagger c_i$$
这就是 $(c_i^\dagger c_j + h.c.)$ 里 $h.c.$ 的含义。

---

## 厄米矩阵（自伴矩阵）

满足 $H^\dagger = H$ 的矩阵称为厄米矩阵。这在物理中是**最核心的要求**，因为：

1. **本征值全为实数** — 物理可观测量必须这样
2. **不同本征值对应的本征矢量正交**
3. **本征矢量构成完备基**（谱定理）

任何物理上合理的哈密顿量都是厄米的。构造时加 $+h.c.$ 的目的就是保证这一点。

### 最简单的例子

$$H = \begin{pmatrix} a & c \\ c^* & b \end{pmatrix}, \quad a,b \in \mathbb{R}$$

对角元必为实数，非对角元互为复共轭。

---

## Bra-Ket 符号中的 dagger

- $\vert \psi \rangle$ 是一个列向量（ket）
- $\langle \psi \vert$ 是它的厄米共轭（bra）：$\langle \psi \vert = \vert \psi \rangle^\dagger$

对算符 $O$ 的期望值：
$$\langle O \rangle = \langle \psi \vert O \vert \psi \rangle = \psi^\dagger O \psi$$

这自动保证期望值是实数当 $O$ 是厄米的：
$$\langle O \rangle^* = (\psi^\dagger O \psi)^\dagger = \psi^\dagger O^\dagger \psi = \psi^\dagger O \psi = \langle O \rangle$$

---

## 代码中的对应

| 操作 | NumPy/SciPy | 说明 |
|------|------------|------|
| 复共轭 | `np.conj(A)` | 每个元素取共轭 |
| 转置 | `A.T` | 行列互换 |
| 厄米共轭 | `A.conj().T` 或 `scipy.linalg.A.H` | 两步合并 |
| 厄米矩阵对角化 | `scipy.linalg.eigh(H)` | **必须用 eigh 而不是 eig**——利用厄米性，更快且保证实本征值 |

---

## 相关笔记

- [[福克空间与占据数表象]]
- [[创造湮灭算符的矩阵表示]]
- [[哈密顿量中的dagger与厄米性]]
