---
tags: [强关联, 自旋涨落, NMR, 磁化率, 唯象模型]
created: 2026-07-26
---

# MMP 磁化率

## 背景：为什么需要 MMP 磁化率

铜氧化物正常态（$T > T_c$，尤其在最佳掺杂附近）的 NMR 实验给出了反常结果——自旋-晶格弛豫率 $1/T_1$ 和自旋-自旋弛豫率 $1/T_2$ 的温度依赖不能同时用简单的 BCS 型磁化率或自由电子泡利磁化率解释。常规金属中自旋涨落是宽频带、无特定波矢的，但铜氧化物的 NMR 数据表明自旋涨落集中在反铁磁波矢 $\mathbf{Q} = (\pi, \pi)$ 附近，且具有特定的频率依赖。

Millis、Monien 和 Pines 在 1990 年提出了一套唯象磁化率——不求解微观哈密顿量，而是直接构造一个满足 NMR 实验约束的解析函数形式。这就是 MMP 磁化率的由来。

---

## MMP 磁化率的函数形式

### 实频形式

$$\chi(\mathbf{q}, \omega) = \frac{\chi_Q}{1 + \xi^2(\mathbf{q} - \mathbf{Q})^2 - i\omega/\omega_{sf}}$$

### 虚频形式（Matsubara）

$$\chi(\mathbf{q}, i\omega_n) = \frac{\chi_Q}{1 + \xi^2(\mathbf{q} - \mathbf{Q})^2 + |\omega_n|/\omega_{sf}}$$

### 各参数物理含义

| 参数 | 物理含义 | 实验来源 |
|------|---------|---------|
| $\mathbf{Q}$ | 反铁磁特征波矢 $(\pi, \pi)$ | 中子散射：自旋涨落集中在 AFM 波矢 |
| $\chi_Q$ | $\mathbf{Q}$ 处的静态自旋磁化率 | NMR Knight 位移 + $T_1$ 测量 |
| $\xi$ | 反铁磁自旋关联长度 | 中子散射峰宽：$\Delta q \sim 1/\xi$ |
| $\omega_{sf}$ | 自旋涨落特征频率（弛豫速率） | NMR $T_1$ + 非弹性中子散射能量宽度 |

---

## 函数形式的物理来源

分母里的每一项都有明确的物理对应。

### 空间部分：$1 + \xi^2(\mathbf{q} - \mathbf{Q})^2$

这是 Ornstein-Zernike 形式——近临界体系（反铁磁 QCP 附近）的经典结果。当体系接近反铁磁量子临界点时，关联长度 $\xi$ 发散，磁化率在 $\mathbf{Q}$ 处形成一个尖锐的峰。$1 + \xi^2(\mathbf{q} - \mathbf{Q})^2$ 是 $\chi(\mathbf{q})$ 在 $\mathbf{q} = \mathbf{Q}$ 处的泰勒展开到二阶：

$$\chi^{-1}(\mathbf{q}) \approx \chi_Q^{-1}\left[1 + \xi^2(\mathbf{q} - \mathbf{Q})^2\right]$$

### 频率部分：$-i\omega/\omega_{sf}$

这是因果律要求的最简形式。响应函数在时域满足 $\chi(t-t')=0$ 当 $t<t'$（因果性），傅里叶变换后分母必须有 $-i\omega$ 项。$\omega_{sf}$ 是自旋涨落的弛豫速率——它决定了耗散的强度。虚部：

$$\operatorname{Im}\chi(\mathbf{Q}, \omega) = \frac{\chi_Q \, \omega/\omega_{sf}}{1 + (\omega/\omega_{sf})^2}$$

这正是 Lorentz 型耗散谱——峰值在 $\omega = \omega_{sf}$，半高宽 $\sim \omega_{sf}$。

### 虚频形式中 $|\omega_n|$ 的来源

从实频解析延拓到虚频：$\omega \to i\omega_n$，$-i\omega \to -i(i\omega_n) = \omega_n$。取绝对值 $|\omega_n|$ 是为了保证响应函数在 Matsubara 轴上仍是实的（涨落-耗散定理要求）。

---

## 与 NMR 实验的联系

NMR 测的两个核心量都和 $\chi(\mathbf{q}, \omega)$ 直接相关。

### 自旋-晶格弛豫率 $1/T_1$

$$1/T_1 T \propto \sum_{\mathbf{q}} \frac{\operatorname{Im}\chi(\mathbf{q}, \omega_0)}{\omega_0} \approx \frac{\chi_Q}{\omega_{sf}} \int \frac{d^2q}{1 + \xi^2(\mathbf{q} - \mathbf{Q})^2}$$

NMR 频率 $\omega_0$（通常在 MHz 范围）远小于自旋涨落特征频率 $\omega_{sf}$（通常在 meV 范围）——$\omega_0 \ll \omega_{sf}$——所以 $\operatorname{Im}\chi \propto \omega_0/\omega_{sf}$，代入后 $\omega_0$ 消去，$1/T_1T$ 主要由静态磁化率 $\chi_Q$ 和自旋弛豫速率 $\omega_{sf}$ 决定。

### 自旋-自旋弛豫率 $1/T_2$（或 $1/T_{2G}$）

$$1/T_{2G} \propto \sqrt{\sum_{\mathbf{q}} |\chi(\mathbf{q}, 0)|^2} \approx \frac{\chi_Q}{\xi}$$

对 $\mathbf{q}$ 积分后的结果正比于 $\chi_Q/\xi$。和 $1/T_1T \propto \chi_Q/(\omega_{sf}\xi^2)$ 相比，这两个测量量提供了 $\chi_Q$、$\xi$、$\omega_{sf}$ 的独立约束。

### 实验上提取参数的方法

- **Knight 位移** $K \propto \chi_Q$：测量 $\mathbf{q}=0$ 附近的自旋磁化率响应，由传导电子和局域自旋的超精细耦合决定
- **$1/T_1T$** 给出 $\chi_Q/(\omega_{sf} \xi^2)$
- **$1/T_{2G}$** 给出 $\chi_Q/\xi$
- **中子散射** 直接测量 $\xi$（峰宽 $\Delta q$）和 $\omega_{sf}$（能量宽度）

四组独立数据放在一起，能同时定出 $\chi_Q$、$\xi$、$\omega_{sf}$ 的温度依赖。

---

## MMP 磁化率的成功与局限

### 成功之处

MMP 磁化率用一个简单的 Ornstein-Zernike 空间分布 + Lorentz 型耗散的形式，成功描述了铜氧化物正常态的 NMR 数据——特别是 $1/T_1T$ 和 $1/T_{2G}$ 在宽温度范围内的行为，以及它们对掺杂浓度的依赖。

更重要的是，它提供了自旋涨落的**唯象标度关系**：
- $\xi$ 随温度降低而增长（接近反铁磁 QCP）
- $\omega_{sf} \sim \xi^{-z}$（$z$ 是动力学临界指数，MMP 中 $z=2$）
- $1/T_1T$ 在低温下偏离 Korringa 关系（$\propto 1/T$），呈 $\propto T$ 或更复杂的幂律行为

这些标度关系后来被用于检验微观理论（如自旋费米子模型、规范场理论）的正确性。

### 局限之处

- MMP 是唯象模型——$\chi_Q$、$\xi$、$\omega_{sf}$ 是拟合参数，不是从哈密顿量推导出来的
- Ornstein-Zernike 形式在二维体系中本身有问题：二维反铁磁的关联长度 $\xi$ 是指数增长的（$\xi \sim e^{2\pi\rho_s/T}$），不是幂律
- 频率依赖的 $|\omega_n|$ 形式（在 Matsubara 表示中）虽然满足因果律，但过于简单——真实的量子临界磁化率可能涉及更复杂的 $|\omega_n|/T$ 标度依赖

尽管如此，MMP 磁化率至今仍然是分析铜氧化物 NMR 数据、中子散射数据的标准参照模型——因为它足够简单，物理图像足够清晰，抓住了自旋涨落"集中在 $\mathbf{Q}$ 附近 + 满足因果律"这两个核心特征。

---

## 相关笔记

- [[Kramers-Kronig与解析延拓]] — 实频 ↔ 虚频的解析延拓，$-i\omega$ 项的因果律来源
- [[奇异金属与Doniach相图]] — 奇异金属相、非费米液体正常态
- [[强关联体系通用相图]] — 反铁磁 QCP + 超导穹顶 + 自旋涨落配对
- [[超导能隙与热力学响应]] — $1/T_1$ 在超导态中幂律 vs 指数依赖
