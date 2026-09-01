---
tags:
  - Hubbard-model
  - multi-orbital
  - strong-correlation
  - nickelate
  - Hund-coupling
date: 2026-08-03
aliases:
  - 多轨道Hubbard模型
---

# 多轨道 Hubbard 模型

> 将 d_z²、d_x²−y²、t₂g 等多个轨道同时纳入强关联框架的理论工具。单轨道 Hubbard 只管"一个轨道上的电子要不要局域化"，多轨道版本管的是"几个轨道上的电子各自局域化到什么程度、互相之间怎么串通"。

---

## 一、从单轨道到多轨道

### 单轨道 Hubbard

$$
H = -t \sum_{\langle i,j \rangle, \sigma} (c_{i\sigma}^\dagger c_{j\sigma} + h.c.) + U \sum_i n_{i\uparrow} n_{i\downarrow}
$$

- 第一项：电子跳跃 t → 倾向巡游、倾向金属
- 第二项：同格点双占据排斥 U → 倾向局域、倾向绝缘
- **只有两个参数在拔河**：t 想把电子铺开，U 想把电子锁在位点上

### 多轨道推广

$$
H = H_{kin} + H_U + H_{Hund} + H_{ex}
$$

四个部分各自承担不同物理。

---

## 二、H_kin —— 轨道分辨的跳跃矩阵

$$
H_{kin} = -\sum_{\langle i,j \rangle} \sum_{\alpha,\beta} \sum_{\sigma} 
          t_{i\alpha, j\beta} \; (c_{i\alpha\sigma}^\dagger c_{j\beta\sigma} + h.c.)
$$

α, β 标记轨道（d_z², d_x²−y², d_xz, ...）。t_{iα, jβ} 不仅包含格点 i→j 的跳跃，还包含**轨道之间的杂化跳跃**（d_z² ↔ d_x²−y² 的直接耦合来源）。

**不同轨道的 t 可以差一个数量级**：

| 通路 | 主导轨道 | t 大小 | 原因 |
|:---|:---|:---:|:---|
| 层间 Ni–apical O–Ni | d_z² | **大** | σ 型 d_z²–p_z–d_z² 重叠 |
| 面内 Ni–O–Ni | d_x²−y² | 大 | σ 型 d_x²−y²–p_x/p_y |
| 面内 Ni–O–Ni | d_z² | 小 | π 型重叠（仅赤道分量） |

**结构写在 t 矩阵里——"结构是语法"就是体现在这里。**

---

## 三、H_U —— 轨道选择的库仑排斥

$$
H_U = \sum_{i,\alpha} U_\alpha \; n_{i\alpha\uparrow} n_{i\alpha\downarrow}
$$

每个轨道有自己专属的 U_α。d_z² 更局域 → U_z² 更大。d_x²−y² 更延展 → U_x²−y² 较小。

**轨道选择的 Mott 物理（OSMP）的根源**：U_z²/W_z² 越过 Mott 临界值，但 U_x²−y²/W_x²−y² 没到。一个轨道局域了，另一个还巡游。

---

## 四、H_Hund —— 轨道间耦合

$$
H_{Hund} = -J_H \sum_{i,\alpha \neq \beta} \mathbf{S}_{i\alpha} \cdot \mathbf{S}_{i\beta}
          + J_H' \sum_{i,\alpha \neq \beta} (c_{i\alpha\uparrow}^\dagger c_{i\alpha\downarrow}^\dagger c_{i\beta\downarrow} c_{i\beta\uparrow} + h.c.)
          + U' \sum_{i,\alpha < \beta} n_{i\alpha} n_{i\beta}
$$

三项各自的功能：

| 项 | 物理 | 能标 | 在 Ni327 中的角色 |
|:---|:---|:---:|:---|
| J_H（自旋-自旋） | 强制两轨道自旋平行 | ~0.7–0.9 eV | d_z² 自旋"绑架"d_x²−y² 自旋 |
| J_H'（对跳 pair-hopping） | 一个轨道配对整体跳到另一个轨道 | = J_H | **Camp B 的数学载体——d_z² 单态振幅泄漏到 d_x²−y²** |
| U'（轨道间库仑） | 两轨道电子密度互相排斥 | ~U − 2J_H | — |

三者满足 Kanamori 参数化：$U' = U - 2J_H$, $J_H = J_H'$。

---

## 五、H_ex —— 格点间的超交换

强耦合极限（U ≫ t）下做二阶微扰展开，H_kin + H_U 退化成**海森堡自旋模型**：

$$
H_{ex} = \sum_{\langle i,j \rangle} \sum_{\alpha,\beta} J_{ij}^{\alpha\beta} \; 
         \mathbf{S}_{i\alpha} \cdot \mathbf{S}_{j\beta}
$$

其中

$$
J_{ij}^{\alpha\beta} \propto \frac{t_{i\alpha,j\beta}^2}{U_{eff}}
$$

**J 的大小取决于两个竞争因素**：
- 分子 $t^2$：d_z² 沿 c 轴的 t 远大于面内任何方向 → J⊥ 天然比 J∥ 大
- 分母 $U_{eff}$：d_z² 更局域 → U 更大 → 这会减弱 J⊥

两者竞争后，$J_\perp / J_\parallel \sim 3-10$。

---

## 六、多轨道 vs 单轨道的核心区别

| | 单轨道 Hubbard | 多轨道 Hubbard |
|:---|:---|:---|
| **核心问题** | 巡游 vs 局域 | 谁局域、谁巡游 + 局域和巡游怎么串通 |
| **配对胶水** | J 来自同一轨道 | J 可以来自一个轨道，传递给另一个轨道 |
| **实验对应** | 铜氧化物近似适用 | Ni327（d_z² + d_x²−y² 共存）必须用 |
| **结构印记** | 仅键长 | 键长 + 键角 + 配位数 + orbital lobe 方向 |
| **相图复杂性** | 反铁磁 + d 波 | 反铁磁 + 向列 + 轨道序 + s± 或 d 波 |

---

## 七、对应关系：模型 → 物理

| 模型层次 | 物理 | 对应讨论内容 |
|:---|:---|:---|
| H_kin（t 矩阵） | 电子跳跃——结构决定 | "结构是语法" |
| H_U（U_α） | 谁局域 | d_z² 的 m*/m=5–8 vs d_x²−y² 的 2–3 |
| H_Hund（J_H + J_H'） | 轨道间耦合 | "d_z² 和 d_x²−y² 之间有耦合"的来源 |
| H_ex（J ∝ t²/U） | 格点间超交换 | J⊥ ≫ J∥，条纹磁序，(π,0) vs (π,π) |

---

## 相关笔记

- [[La3Ni2O7-层间层内电子对比分析]]
- [[J值与Tc关系跨体系调研]]
- [[s±波配对对称性]]

---

*创建时间：2026-08-03*
