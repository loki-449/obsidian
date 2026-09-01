---
tags: [数学, 线性代数, SVD, 矩阵分解, DMRG]
created: 2026-07-26
---

# 奇异值分解 (SVD)

## 一句话定义

任何一个 $m \times n$ 矩阵 $A$ 都可以分解为 $A = U \Sigma V^\dagger$——$U$ 和 $V$ 是幺正矩阵（列是左右奇异矢量），$\Sigma$ 是对角矩阵（对角元是奇异值 $\sigma_i \geq 0$）。**这是矩阵最重要的分解之一，没有厄米性要求。**

---

## 定义

$$A = U \Sigma V^\dagger$$

- $U$ ($m\times m$)：左奇异矢量，$U^\dagger U = I$
- $\Sigma$ ($m\times n$)：对角矩阵，$\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_r > 0 = \cdots = 0$
- $V$ ($n\times n$)：右奇异矢量，$V^\dagger V = I$
- $r = \operatorname{rank}(A)$：非零奇异值的个数

---

## 与本征值分解的关系

SVD 和 $A^\dagger A$ (或 $AA^\dagger$) 的本征值是一一对应的：

$$A^\dagger A = V \Sigma^2 V^\dagger, \quad AA^\dagger = U \Sigma^2 U^\dagger$$

- $V$ 的列是 $A^\dagger A$ 的本征矢量
- $U$ 的列是 $AA^\dagger$ 的本征矢量
- $\sigma_i = \sqrt{\lambda_i}$，其中 $\lambda_i$ 是 $A^\dagger A$ 的本征值

**注意**：$A^\dagger A$ 总是厄米且半正定的——所以 $\sigma_i$ 总是实数且 $\geq 0$。

---

## 低秩近似（Eckart-Young 定理）

保留前 $k$ 个奇异值，扔掉其余的：

$$A_k = \sum_{i=1}^{k} \sigma_i \mathbf{u}_i \mathbf{v}_i^\dagger$$

这是对 $A$ 的在 Frobenius 范数意义下**最优**的秩-$k$ 近似：
$$\|A - A_k\|_F = \sqrt{\sum_{i=k+1}^r \sigma_i^2}$$

---

## 在 DMRG 中的应用——这是大杀器

DMRG 每一步的核心操作就是 SVD 截断。

### 流程

1. 把系统+环境的联合波函数 $\vert\Psi\rangle$ 重塑为矩阵 $M$（行=系统自由度，列=环境自由度）
2. 对 $M$ 做 SVD：$M = U \Sigma V^\dagger$
3. 保留最大的 $m$ 个奇异值（$m$ 是 bond dimension）
4. 扔掉 $\sigma_{m+1}, \ldots$ → 截断误差 $\varepsilon = \sum_{i=m+1}^r \sigma_i^2$
5. 用截断后的 $U$ 重定义系统基

### 为什么 SVD 是最优的

Eckart-Young 定理保证——在 Frobenius 范数下，丢掉最小的奇异值带来的误差是所有同秩近似中最小的。**SVD 是信息损失最少的方式。**

### 纠缠熵

约化密度矩阵 $\rho_A = M M^\dagger$ 的本征值就是 $\sigma_i^2$。纠缠熵：
$$S = -\sum_i \sigma_i^2 \ln \sigma_i^2$$

奇异值衰减越快 → 纠缠越小 → DMRG 越高效（用很小的 $m$ 就能精确描述基态）。一维有能隙体系满足面积律 → 奇异值指数衰减 → DMRG 近似精确。

---

## 代码

```python
import numpy as np

U, S, Vh = np.linalg.svd(M, full_matrices=False)

# 截断到 m 个奇异值
U_trunc = U[:, :m]
S_trunc = S[:m]
Vh_trunc = Vh[:m, :]

# 截断误差
truncation_error = np.sum(S[m:]**2)
```

---

## 相关笔记

- [[本征值问题与谱分解]]
- [[Kronecker积与张量积]]
- [[DMRG中的MPO构造]]
