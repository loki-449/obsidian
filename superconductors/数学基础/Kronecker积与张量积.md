---
tags: [数学, 线性代数, 张量积, 希尔伯特空间]
created: 2026-07-26
---

# Kronecker 积与张量积

## 一句话定义

Kronecker 积（$\otimes$）是两个矩阵的"分块乘法"——把左边矩阵的每个元素乘以整个右边矩阵，结果维数是两个维数的乘积。物理上是把两个子系统的希尔伯特空间"拼"成复合系统空间的标准操作。

---

## 定义

$A$ ($m\times n$) $\otimes$ $B$ ($p\times q$) 得到 $mp \times nq$：

$$A \otimes B = \begin{pmatrix}
a_{11}B & a_{12}B & \cdots & a_{1n}B \\
a_{21}B & a_{22}B & \cdots & a_{2n}B \\
\vdots & \vdots & \ddots & \vdots \\
a_{m1}B & a_{m2}B & \cdots & a_{mn}B
\end{pmatrix}$$

**记忆方法**：每个元素 $a_{ij}$ 的位置放一个 $a_{ij} \cdot B$（整个矩阵 $B$ 缩放到 $a_{ij}$ 倍）。

---

## 物理含义：希尔伯特空间的直积

两个子系统的态 $\vert \psi_A \rangle \in \mathcal{H}_A$（$d_A$ 维）和 $\vert \psi_B \rangle \in \mathcal{H}_B$（$d_B$ 维）的复合态：

$$\vert \psi_A \rangle \otimes \vert \psi_B \rangle \in \mathcal{H}_A \otimes \mathcal{H}_B \quad (\text{维数 } d_A \cdot d_B)$$

在占据数基下，$M$ 个费米子轨道就是 $M$ 个 $2\times 2$ 空间的 Kronecker 积：

$$\mathcal{F} = \underbrace{\mathbb{C}^2 \otimes \mathbb{C}^2 \otimes \cdots \otimes \mathbb{C}^2}_{M \text{ 个}}$$

每个 $\mathbb{C}^2$ 代表一个轨道（占据态 $\vert 1\rangle$ 和空态 $\vert 0\rangle$）。

### 不纠缠的态（可分态）

$$\vert 0 \rangle \otimes \vert 1 \rangle \otimes \vert 0 \rangle = \vert 010 \rangle$$

这是 $\mathcal{F}$ 的一个基矢——恰好就是占据数表象里的一个态。

### 纠缠态

不能写成 Kronecker 积形式的态，例如 Bell 态：

$$\frac{1}{\sqrt{2}}(\vert 01\rangle + \vert 10\rangle) \neq \vert \psi_1 \rangle \otimes \vert \psi_2 \rangle$$

---

## 关键代数性质

这些性质在构造多轨道算符和验证对易关系时**每步都在用**：

| 性质 | 公式 | 用途 |
|------|------|------|
| 乘积拆分 | $(A \otimes B)(C \otimes D) = (AC) \otimes (BD)$ | 验证反对易关系 |
| 和分配 | $(A+B)\otimes C = A\otimes C + B\otimes C$ | 线性叠加 |
| Dagger 拆分 | $(A \otimes B)^\dagger = A^\dagger \otimes B^\dagger$ | 创造算符构造 |
| 迹乘积 | $\operatorname{Tr}(A \otimes B) = \operatorname{Tr}(A) \cdot \operatorname{Tr}(B)$ | 配分函数 |
| 行列式 | $\det(A \otimes B) = (\det A)^{p} (\det B)^{m}$ | — |
| 本征值 | $\lambda_i \mu_j$（$A$ 和 $B$ 本征值的全部配对） | 对角化 |

**乘积拆分**是最关键的性质。验证 $\{c_1, c_2\} = 0$ 时：

$$c_1 c_2 = (c \otimes I)(I \otimes c) = (cI) \otimes (Ic) = c \otimes c$$
$$c_2 c_1 = (I \otimes c)(c \otimes I) = (Ic) \otimes (cI) = c \otimes c$$

但这里需要 Jordan-Wigner 弦才能得到正确的 $-1$——**Kronecker 积本身无法区分玻色子和费米子符号，需要额外处理**（见 [[Jordan-Wigner变换]]）。

---

## 代码中的 Kronecker 积

```python
import numpy as np

# 两个 2x2 矩阵的 Kronecker 积 → 4x4
c = np.array([[0, 1], [0, 0]])
I = np.eye(2)

c1 = np.kron(c, I)   # 作用在第一个轨道
c2 = np.kron(I, c)   # 作用在第二个轨道
```

NumPy 的 `kron` 直接实现。

---

## 偏迹（Partial Trace）

Kronecker 积的逆操作——从复合系统约化出一个子系统的密度矩阵：

$$\rho_A = \operatorname{Tr}_B(\rho_{AB})$$

对于 $\rho_{AB} = A \otimes B$，$\rho_A = \operatorname{Tr}(B) \cdot A$。纠缠态不可做此拆分——这正是纠缠的定义。

在 DMRG 中，每一步截断都是通过约化密度矩阵的偏迹来实现的。

---

## 相关笔记

- [[创造湮灭算符的矩阵表示]]
- [[福克空间与占据数表象]]
- [[Jordan-Wigner变换]]
- [[奇异值分解SVD]]
