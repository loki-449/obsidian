---
tags: [数学, 二次量子化, 费米子, 自旋映射]
created: 2026-07-26
---

# Jordan-Wigner 变换

## 一句话定义

Jordan-Wigner 变换把一维费米子算符**精确地**映射为自旋-1/2 算符（Pauli 矩阵），用一串 $\sigma^z$（JW 弦）来编码费米子符号——把反对易关系的非定域性转化为自旋语言的定域结构。

---

## 动机：为什么需要它

Kronecker 积构造的多轨道算符在**基矢按特定顺序排列时**自动满足反对易关系。但如果基序混乱，或者你想把费米子问题映射到自旋链上做 DMRG / QMC，就需要显式地处理不同位置算符之间的符号。

JW 变换给出了这个映射的标准形式。

---

## 变换公式

### 从费米子到自旋

$$c_j = \left(\prod_{l=1}^{j-1} \sigma_l^z\right) \sigma_j^-$$

$$c_j^\dagger = \left(\prod_{l=1}^{j-1} \sigma_l^z\right) \sigma_j^+$$

其中：
- $\sigma_j^- = \begin{pmatrix}0&0\\1&0\end{pmatrix}$ — 在位置 $j$ 的自旋降算符（湮灭一个自旋向上）
- $\sigma_j^+ = (\sigma_j^-)^\dagger = \begin{pmatrix}0&1\\0&0\end{pmatrix}$ — 自旋升算符（创造）
- $\sigma_j^z = \begin{pmatrix}1&0\\0&-1\end{pmatrix}$ — Pauli-Z 矩阵
- 弦 $S_j = \prod_{l=1}^{j-1} \sigma_l^z$ — **JW 弦**，给前面所有轨道"签名"

### 逆变换

$$ \sigma_j^z = 2c_j^\dagger c_j - 1 = 2\hat{n}_j - 1 $$

$$ \sigma_j^- = c_j \prod_{l=1}^{j-1} (1 - 2\hat{n}_l) $$

粒子数算符对应于自旋投影：占据 $\vert 1\rangle \to \sigma^z$ 本征值 $+1$，空态 $\vert 0\rangle \to \sigma^z$ 本征值 $-1$。

---

## JW 弦如何产生费米子符号

### 核心机制

弦 $S_j = \prod_{l=1}^{j-1} \sigma_l^z$ 的作用是"记住前面有多少个费米子"：
- $\sigma_l^z$ 作用于占据态 $\vert 1\rangle$ 给出 $+1$
- $\sigma_l^z$ 作用于空态 $\vert 0\rangle$ 给出 $-1$
- 两个占据态之间越过对方时，弦贡献 $-1$ 因子 → 反对易

### M=2 的显式矩阵验证

$$c_1 = \sigma_1^- \otimes I_2$$

$$c_2 = \sigma_1^z \otimes \sigma_2^-$$

计算乘积 $c_1 c_2$ 和 $c_2 c_1$：

$$c_1 c_2 = (\sigma_1^- \sigma_1^z) \otimes \sigma_2^-$$

$$\sigma_1^- \sigma_1^z = \begin{pmatrix}0&0\\1&0\end{pmatrix}\begin{pmatrix}1&0\\0&-1\end{pmatrix} = \begin{pmatrix}0&0\\1&0\end{pmatrix} = \sigma_1^-$$

$$c_2 c_1 = (\sigma_1^z \sigma_1^-) \otimes \sigma_2^-$$

$$\sigma_1^z \sigma_1^- = \begin{pmatrix}1&0\\0&-1\end{pmatrix}\begin{pmatrix}0&0\\1&0\end{pmatrix} = \begin{pmatrix}0&0\\-1&0\end{pmatrix} = -\sigma_1^-$$

因此 $c_1 c_2 = \sigma_1^- \otimes \sigma_2^-$，$c_2 c_1 = -\sigma_1^- \otimes \sigma_2^-$，求和为零：
$$\{c_1, c_2\} = 0 \; \checkmark$$

**关键点**：$\sigma_1^z$ 和 $\sigma_1^-$ 对易关系在不同顺序下差了一个负号——这个 $-1$ 就是 JW 弦产生的费米子符号。

---

## 一维横场 Ising 模型 → 自由费米子（经典应用）

$$H_{\text{TFI}} = -J\sum_{j} \sigma_j^x \sigma_{j+1}^x - h\sum_j \sigma_j^z$$

经 JW 变换后：

$$H_{\text{TFI}} = -J\sum_j (c_j^\dagger - c_j)(c_{j+1}^\dagger + c_{j+1}) - h\sum_j (2c_j^\dagger c_j - 1)$$

再经 Bogoliubov 变换对角化。这是精确可解模型的经典例子。

---

## 适用范围与局限

**适用**：一维或准一维系。JW 变换严格保持反对易关系，无近似。

**不适用**：二维及以上。JW 弦在二维晶格上会产生非定域的弦（"弦需要一条贯穿晶格的路径"），得到的自旋哈密顿量包含长程多体相互作用，失去了映射的实用性。

二维费米子体系通常直接保留费米子语言，不做 JW 映射。

---

## 相关笔记

- [[创造湮灭算符的矩阵表示]]
- [[福克空间与占据数表象]]
- [[哈密顿量中的dagger与厄米性]]
