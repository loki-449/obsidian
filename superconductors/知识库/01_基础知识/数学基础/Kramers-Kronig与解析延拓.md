---
tags: [数学, 响应函数, 因果律, 涨落耗散]
created: 2026-07-26
---

# Kramers-Kronig 关系与解析延拓

## 一句话定义

因果律要求响应不能超前于扰动——这个物理约束等价于响应函数 $\chi(\omega)$ 在上半复平面解析。解析性通过留数定理推出 KK 关系：实部和虚部互推。再通过谱表示把实频和虚频（Matsubara）统一为同一个谱函数的两种参数化。

---

## 因果律 → 解析性

响应函数在时域满足因果性：$\chi(t-t') = 0$ 当 $t < t'$。傅里叶变换到复频域：

$$\chi(z) = \int_{-\infty}^{\infty} \chi(t) e^{izt} dt, \quad z = \omega + i\eta$$

因果性保证当 $\operatorname{Im}(z) > 0$（上半平面）时积分收敛 → $\chi(z)$ 在上半平面解析（无极点）。

---

## Kramers-Kronig 关系

解析函数在实轴上的实部和虚部不是独立的。用留数定理积分：

$$\operatorname{Re}\chi(\omega) = \frac{1}{\pi}\mathcal{P}\int_{-\infty}^{\infty} \frac{\operatorname{Im}\chi(\omega')}{\omega' - \omega}d\omega'$$

$$\operatorname{Im}\chi(\omega) = -\frac{1}{\pi}\mathcal{P}\int_{-\infty}^{\infty} \frac{\operatorname{Re}\chi(\omega')}{\omega' - \omega}d\omega'$$

$\mathcal{P}$ 是柯西主值积分。**知道全频域的虚部，就能算出任意频率的实部；知道全频域的实部，就能算出任意频率的虚部。** 色散（实部）和吸收（虚部）被因果律锁死。

### 物理例子：阻尼谐振子

$$\chi(\omega) = \frac{1}{\omega_0^2 - \omega^2 - i\gamma\omega}$$

实部（色散）在 $\omega_0$ 处过零，虚部（吸收）在 $\omega_0$ 处取峰值——两者通过 KK 关系严格互推。$\gamma$ 是耗散系数，决定吸收峰的宽度。

---

## 涨落-耗散定理

平衡态的涨落（热驱动）和非平衡态的耗散（外场驱动）之间的严格关系：

$$\operatorname{Im}\chi(\omega) = \frac{\pi}{\hbar}(1 - e^{-\beta\hbar\omega}) S(\omega)$$

其中 $S(\omega) = \int dt\, e^{i\omega t} \langle A(t)A(0) \rangle$ 是动态结构因子（涨落的谱密度）。

经典极限（$\hbar\omega \ll k_B T$）：$\operatorname{Im}\chi(\omega) \propto \omega\, S(\omega)/k_B T$
量子极限（$\hbar\omega \gg k_B T$）：$\operatorname{Im}\chi(\omega) \propto S(\omega)$

NMR 实验中的 $1/T_1T \propto \sum_q \operatorname{Im}\chi(q,\omega_0)/\omega_0$ 就是涨落-耗散定理的直接应用——自旋-晶格弛豫率测的是局域自旋涨落的谱密度。

---

## 解析延拓：实频 ↔ 虚频

Matsubara（虚频）形式：$\chi(q, i\omega_n)$，$\omega_n = 2n\pi k_B T$（玻色）或 $(2n+1)\pi k_B T$（费米）。

推迟（实频）形式：$\chi^R(q, \omega) = \chi(q, \omega + i0^+)$。

两者通过**谱表示（Lehmann 表示）**统一：

$$\chi(q, i\omega_n) = \int_{-\infty}^{\infty} \frac{d\omega'}{\pi} \frac{\operatorname{Im}\chi^R(q, \omega')}{\omega' - i\omega_n}$$

从虚频到实频：把 $i\omega_n$ 解析延拓到 $\omega + i0^+$——这是整个量子多体理论的标准操作。

### MMP 磁化率的具体体现

实频形式：
$$\chi(q,\omega) = \frac{\chi_Q}{1 + \xi^2(q-Q)^2 - i\omega/\omega_{sf}}$$

虚部 $\operatorname{Im}\chi \propto \omega/\omega_{sf}$ 是自旋涨落的耗散通道（NMR $1/T_1$ 的来源）。

虚频形式：
$$\chi(q, i\omega_n) = \frac{\chi_Q}{1 + \xi^2(q-Q)^2 + |\omega_n|/\omega_{sf}}$$

$-i\omega/\omega_{sf} \to |\omega_n|/\omega_{sf}$——解析延拓时 $\omega$ 换成 $i\omega_n$，$i \cdot i = -1$ 的符号被绝对值吸收（保证虚频响应函数是实的，涨落-耗散定理的要求）。

---

## 总结：三条锁链

| 锁链 | 连接的内容 | 数学根源 |
|------|-----------|----------|
| KK 关系 | 实部 ↔ 虚部 | 因果律 → 上半平面解析 → 留数定理 |
| 涨落-耗散定理 | 热涨落 ↔ 外场耗散 | 平衡态统计算符 $e^{-\beta H}$ 的谱表示 |
| 解析延拓 | Matsubara ↔ 推迟 | 同一个谱函数 $A(\omega)$ 的参数化：$\int d\omega\, A(\omega)/(\omega - z)$ |

**三条锁链的共同根源：系统与热浴的耦合 + 因果律。** 无论测输运、NMR、中子散射还是光学电导率，只要涉及响应函数，这三条锁链就同时生效。

---

## 相关笔记

- [[厄米共轭与dagger]]
- [[本征值问题与谱分解]]
- [[知识库/01_基础知识/强关联/01_强关联基础/电阻率与比热公式集|电阻率与比热公式集]]
