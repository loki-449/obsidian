---
tags: [数学, 线性代数, 哈密顿量, 厄米性]
created: 2026-07-26
---

# 哈密顿量中的 dagger 与厄米性

## 核心结论

物理的哈密顿量 $H$ 必须是厄米的（$H = H^\dagger$），因为它的本征值是能量——必须是实数。构造 $H$ 时加 $+h.c.$ 就是加前一项的 dagger，这就是为了保证厄米性。

---

## 跳跃项（Hopping）的 dagger 结构

### 标准形式

$$H_{\text{hop}} = -t\sum_{\langle i,j\rangle} (c_i^\dagger c_j + h.c.)$$

其中 $h.c. = (c_i^\dagger c_j)^\dagger = c_j^\dagger c_i$（用了乘积反转性质）。

完整写成：
$$H_{\text{hop}} = -t\sum_{\langle i,j\rangle} (c_i^\dagger c_j + c_j^\dagger c_i)$$

### 为什么加 h.c. 就够了

把 hopping 写成矩阵形式：$H_{\text{hop}} = \sum_{ij} T_{ij} c_i^\dagger c_j$

要求 $T_{ij} = T_{ji}^*$（即 $T$ 是厄米矩阵）。这时：
$$H_{\text{hop}}^\dagger = \sum_{ij} T_{ij}^* c_j^\dagger c_i = \sum_{ij} T_{ji} c_i^\dagger c_j = H_{\text{hop}}$$

**条件**：$T$ 厄米 $\Longleftrightarrow$ $H$ 厄米。所以紧束缚代码里构造好 $T$ 矩阵、检查 $T = T^\dagger$，哈密顿量就自动自洽。

### 代码中的处理

```python
# 构造厄米的 hopping 矩阵
T = np.zeros((M, M), dtype=complex)
for i, j in neighbor_pairs:
    T[i, j] = -t
    T[j, i] = -np.conj(t)  # h.c.

# 验证厄米性
assert np.allclose(T, T.conj().T)
```

---

## 配对项（Pairing）的 dagger

BCS 哈密顿量里：
$$\Delta c_{i\uparrow}^\dagger c_{i\downarrow}^\dagger + h.c. = \Delta c_{i\uparrow}^\dagger c_{i\downarrow}^\dagger + \Delta^* c_{i\downarrow} c_{i\uparrow}$$

$h.c.$ 对创造算符对的作用是反转成湮灭对：
$$(\Delta c_{i\uparrow}^\dagger c_{i\downarrow}^\dagger)^\dagger = \Delta^* c_{i\downarrow} c_{i\uparrow}$$

---

## 电声耦合中的 dagger

$$H_{\text{eph}} = g\sum_{i} (a_i + a_i^\dagger)(c_i^\dagger c_i - \langle n \rangle)$$

$a_i$ 和 $a_i^\dagger$ 是声子算符（玻色子），$c_i^\dagger c_i$ 是电子密度。每一项都自带 dagger 结构——$a_i + a_i^\dagger$ 是厄米的（$(a_i + a_i^\dagger)^\dagger = a_i^\dagger + a_i = a_i + a_i^\dagger$），电子密度 $c_i^\dagger c_i$ 也是厄米的，乘积 $(a_i + a_i^\dagger)(c_i^\dagger c_i - \langle n \rangle)$ 自动厄米。

---

## 自旋算符中的 dagger

$$\mathbf{S}_i = \frac{1}{2}\sum_{\alpha\beta} c_{i\alpha}^\dagger \boldsymbol{\sigma}_{\alpha\beta} c_{i\beta}$$

$S_i^x, S_i^y, S_i^z$ 每个分量都是厄米的（$\sigma$ 矩阵是厄米的）：
$$(S_i^\alpha)^\dagger = \frac{1}{2}\sum_{\alpha\beta} c_{i\beta}^\dagger (\sigma^\alpha_{\beta\alpha})^* c_{i\alpha} = \frac{1}{2}\sum_{\alpha\beta} c_{i\alpha}^\dagger \sigma^\alpha_{\alpha\beta} c_{i\beta} = S_i^\alpha$$

---

## 总结：三层检查

| 检查层次 | 方法 |
|----------|------|
| 符号上 | 每个创造算符配湮灭算符，或显式加 $+h.c.$ |
| 矩阵上 | 确认 hopping/pairing 系数矩阵是厄米的 |
| 代码上 | `assert np.allclose(H, H.conj().T)` |

三层都通过，$H$ 的本征值就一定是实数。

---

## 相关笔记

- [[厄米共轭与dagger]]
- [[创造湮灭算符的矩阵表示]]
- [[本征值问题与谱分解]]
