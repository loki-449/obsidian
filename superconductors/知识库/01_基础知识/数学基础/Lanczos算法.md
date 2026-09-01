---
tags: [数学, 数值方法, 对角化, 迭代算法]
created: 2026-07-26
---

# Lanczos 算法

## 一句话定义

Lanczos 是求大型稀疏厄米矩阵**极端本征值**（最大/最小几个）的迭代算法。它把 $N\times N$ 矩阵投影到低维 Krylov 子空间，在这个子空间里对角化——$O(N\cdot m)$ 而不是 $O(N^3)$。

---

## 为什么需要它

精确对角化 $O(N^3)$，$N=2^M$ 指数增长。$M=20$ 时 $N\approx 10^6$，直接对角化根本不可能。

但物理上通常只需要基态 $\vert\psi_0\rangle$ 和低能激发态——不是整个谱。Lanczos 就是为这个需求设计的。

---

## Krylov 子空间

从一个试探向量 $\vert\phi_0\rangle$ 出发，反复用 $H$ 作用：

$$\mathcal{K}_m = \operatorname{span}\{\vert\phi_0\rangle, H\vert\phi_0\rangle, H^2\vert\phi_0\rangle, \ldots, H^{m-1}\vert\phi_0\rangle\}$$

$m \ll N$（通常 $m \sim 100\text{-}200$）。

**关键直觉**：$H^m\vert\phi_0\rangle$ 里极端本征矢量的分量指数性放大。基底 $\{\vert\phi_0\rangle, H\vert\phi_0\rangle, H^2\vert\phi_0\rangle, \ldots\}$ 天然富含极端本征矢量的信息。

但 $\{H^k\vert\phi_0\rangle\}$ 直接做基不好——它们的 Gram 矩阵接近奇异（数值不稳定）。Lanczos 用 Gram-Schmidt 正交化来稳定。

---

## Lanczos 迭代

### 递推公式

$$\beta_{n+1}\vert\phi_{n+1}\rangle = H\vert\phi_n\rangle - \alpha_n\vert\phi_n\rangle - \beta_n\vert\phi_{n-1}\rangle$$

其中：
$$\alpha_n = \langle\phi_n\vert H\vert\phi_n\rangle, \quad \beta_{n+1} = \|H\vert\phi_n\rangle - \alpha_n\vert\phi_n\rangle - \beta_n\vert\phi_{n-1}\rangle\|$$

初始条件：$\beta_0 = 0$，$\vert\phi_{-1}\rangle = 0$。

### 三对角化

在 Lanczos 基下，$H$ 变成三对角矩阵：

$$T_m = \begin{pmatrix}
\alpha_0 & \beta_1 & 0 & \cdots & 0 \\
\beta_1 & \alpha_1 & \beta_2 & \cdots & 0 \\
0 & \beta_2 & \alpha_2 & \ddots & \vdots \\
\vdots & \vdots & \ddots & \ddots & \beta_{m-1} \\
0 & 0 & \cdots & \beta_{m-1} & \alpha_{m-1}
\end{pmatrix}$$

$T_m$ 是 $m\times m$ 小矩阵，直接调用 `eigh` 对角化。$T_m$ 的极端本征值就是 $H$ 极端本征值的近似。

---

## 收敛性质

- 基态能量从**上方**逼近（变分原理保证 $E_0^{(m)} \geq E_0$）
- 极端本征值收敛最快——因为它们对应 Krylov 子空间里指数放大的分量
- 能隙越大，收敛越快。能隙闭合（临界体系）时收敛变慢
- 一般 $m \sim 100$ 就足够得到基态能量的机器精度

---

## 代码实现

```python
import numpy as np
from scipy.linalg import eigh_tridiagonal

def lanczos(H_func, phi0, m=100):
    """
    H_func: 接受向量返回 H|ψ⟩ 的函数（不需要显式矩阵！）
    phi0: 初始试探向量
    m: Lanczos 迭代步数
    返回: (极端本征值, alphas, betas)
    """
    N = len(phi0)
    alphas = np.zeros(m)
    betas = np.zeros(m)
    
    phi_prev = np.zeros(N)
    phi = phi0 / np.linalg.norm(phi0)
    
    for j in range(m):
        # H|phi_j⟩
        Hphi = H_func(phi)
        
        # α_j = ⟨ϕ_j|H|ϕ_j⟩
        alphas[j] = np.real(np.dot(np.conj(phi), Hphi))
        
        # 新方向: |r⟩ = H|ϕ_j⟩ - α_j|ϕ_j⟩ - β_j|ϕ_{j-1}⟩
        r = Hphi - alphas[j] * phi - betas[j] * phi_prev
        
        if j < m - 1:
            betas[j + 1] = np.linalg.norm(r)
            phi_prev = phi
            phi = r / betas[j + 1]
    
    # 对角化三对角矩阵
    # betas[1:m] 对应 T 的次对角（去掉 betas[0]）
    E, _ = eigh_tridiagonal(alphas, betas[1:])
    
    return E, alphas, betas

# 使用示例
def H_func(psi):
    """稀疏矩阵-向量乘，不构造整个 H"""
    # 对 Hubbard/Heisenberg 等模型，按位操作计算 H|ψ⟩
    return H_sparse @ psi  # 或用按位操作代替显式乘法
```

---

## 幽灵本征值与重正交化

有限精度运算中，$\vert\phi_n\rangle$ 的正交性随 $n$ 增大而丢失（舍入误差累积）。
- **症状**：出现"幽灵本征值"——假的本征值，是不存在的。
- **解决方案1**：完全重正交化——每一步对所有前面的向量做 Gram-Schmidt。多了 $O(m^2 N)$ 开销。
- **解决方案2**：部分重正交化——只对最近几个向量做。
- **解决方案3**：隐式重启（ARPACK 的做法）——在 Krylov 子空间里"滤掉"不想要的本征矢量，重新开始。

SciPy 的 `eigsh` 底层是 ARPACK，已经内置了隐式重启 Lanczos。

---

## 与精确对角化的关系

| | 精确对角化 | Lanczos |
|---|---|---|
| 输出 | 完整谱 | 极端本征值 |
| 复杂度 | $O(N^3)$ | $O(m \cdot N_{\text{nz}})$ |
| 存储 | 整个矩阵 | 2-3 个向量 |
| M 上限 | ~14 | ~24-26 |

ED 是"小体系全谱"，Lanczos 是"大体系极端值"。两者互补。

---

## 相关笔记

- [[精确对角化的矩阵构造]]
- [[本征值问题与谱分解]]
- [[奇异值分解SVD]]
