---
tags: [强关联, 配对机制, d波, MMP磁化率]
created: 2026-07-26
---

# MMP 磁化率 → d 波配对 → 穹顶 $T_c$

## d 波对称性是如何从 MMP 磁化率中出来的

配对相互作用取为 $V(\mathbf{q}) = g^2 \chi(\mathbf{q}, 0)$，$\chi(\mathbf{q})$ 的静态部分：
$$\chi(\mathbf{q}) = \frac{\chi_Q}{1 + \xi^2(\mathbf{q} - \mathbf{Q})^2}, \quad \mathbf{Q}=(\pi,\pi)$$

**关键几何事实**：铜氧化物空穴型费米面上 $(\pi,0)$ 和 $(0,\pi)$ 附近的动量差恰好是 $(\pi,\pi)$——落在 $\chi(\mathbf{q})$ 的峰值上。这两部分费米面之间的配对散射最强。

而同一个区域内部的散射（如 $(\pi,0)$ → $(\pi,0)$）对应的 $\mathbf{q} \approx 0$——MMP 磁化率在 $\mathbf{q}=0$ 处无峰值，耦合很弱。

### 能隙方程的形式

$$\Delta(\mathbf{k}) = -\sum_{\mathbf{k}'} V(\mathbf{k} - \mathbf{k}') \frac{\Delta(\mathbf{k}')}{2E(\mathbf{k}')} \tanh\frac{E(\mathbf{k}')}{2k_B T}$$

$V > 0$（排斥性自旋涨落配对）→ 能隙方程左边的负号要求 $\Delta(\mathbf{k})$ 和 $\Delta(\mathbf{k}')$ **反号** → $(\pi,0)$ 和 $(0,\pi)$ 处的 $\Delta$ 号相反。

这正好是 $d_{x^2-y^2}$ 的对称性：
$$\Delta(\mathbf{k}) \propto \cos k_x - \cos k_y$$

对角线上 $k_x = k_y$ → $\Delta = 0$ → 四个节点。对边中点号相反。

**s 波被禁止**：s 波要求 $\Delta(\mathbf{k})$ 在整个费米面上同号，但 $V > 0$（排斥配对）下能隙方程符号不匹配，无解。MMP 自旋涨落配对的排斥性天然选择了 d 波——这不是调参数挑出来的，是自洽解的必然结果。

---

## 穹顶 $T_c(x)$ 的来源：两个效应竞争

### 态密度效应

空穴掺杂增加 → 费米面从 $(\pi/2,\pi/2)$ 向 $(\pi,0)$ 移动 → $N(E_F)$ 起初增加（更多载流子），过最佳掺杂后进入平台/下降区。

### 自旋涨落衰减

掺杂破坏反铁磁关联 → $\xi$ 减小 → $\chi_Q$ 减小 → 配对相互作用 $V(\mathbf{Q}) \propto \chi_Q$ 减弱。

$$T_c \sim \omega_{sf} \exp\left(-\frac{1}{N(E_F) V}\right)$$

- **低掺杂**：$\chi_Q$ 大，但 $N(E_F)$ 太小 → $T_c$ 低
- **最佳掺杂**：$N(E_F) \times \chi_Q$ 达到最优乘积 → $T_c$ 最大
- **过掺杂**：$\chi_Q$ 持续下降，$N(E_F)$ 不再上升 → 配对胶水稀释 → $T_c$ 减小

**两个效应在自洽计算中自动叠加——穹顶形状不需要额外参数。** MMP 磁化率 + 真实费米面色散 + 粒子数守恒自洽条件，同时给出 d 波对称性和穹顶 $T_c(x)$。

---

## 相关笔记

- [[MMP磁化率]]
- [[电荷转移Mott绝缘体与掺杂]]
- [[Mott绝缘体与Hubbard模型]]
- [[强关联体系通用相图]]
- [[序参量与配对对称性]]
