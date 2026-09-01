---
tags: [基础理论, Tc计算, 强耦合]
created: 2026-05-23
---

# Eliashberg 方程

## 地位
> BCS理论的强耦合推广，是计算氢化物Tc最精确的理论框架

## 方程形式（Matsubara频率空间）

$$Z(i\omega_n) = 1 + \frac{\pi T}{\omega_n}\sum_m \frac{\omega_m}{\sqrt{\omega_m^2 + \Delta^2(i\omega_m)}}\lambda(i\omega_n - i\omega_m)$$

$$Z(i\omega_n)\Delta(i\omega_n) = \pi T \sum_m \frac{\Delta(i\omega_m)}{\sqrt{\omega_m^2+\Delta^2(i\omega_m)}}[\lambda(i\omega_n-i\omega_m)-\mu^*]$$

## 核心物理量

| 量 | 含义 |
|------|------|
| $Z(i\omega_n)$ | 质量重整化函数 |
| $\Delta(i\omega_n)$ | 超导能隙函数 |
| $\lambda(i\omega_n)$ | 频率依赖的电声耦合 |
| $\mu^*$ | 库仑赝势 |

## 与麦克米兰公式的关系
- 麦克米兰公式是 Eliashberg 方程的近似解析解
- Eliashberg 方程需要数值求解
- 对强耦合体系（λ > 1.5）Eliashberg 更准确

## 实际计算中的使用
- 通过 EPW 代码数值求解
- 输入：α²F(ω) 和 μ*
- 输出：Tc 和能隙 Δ

## 相关笔记
- [[BCS理论]]
- [[麦克米兰方程]]
- [[EPW计算]]
- [[声子机制]]