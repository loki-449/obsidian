---
tags: [理论计算, EPW, 电声耦合]
created: 2026-05-23
---

# EPW 计算电声耦合

## EPW 是什么
> Electron-Phonon coupling using Wannier functions
> 基于 Wannier 函数插值计算精确电声耦合常数

## 完整计算流程
Step 1: QE 结构优化 (pw.x)
↓
Step 2: QE 自洽计算 (pw.x scf)
↓ 
Step 3: QE 非自洽计算 (pw.x nscf，粗网格) 
↓
Step 4: DFPT 声子计算 (ph.x) 
↓ 
Step 5: 提取电声矩阵元 (ph.x + q2r.x) 
↓ 
Step 6: Wannier 函数构造 (wannier90) 
↓
Step 7: EPW 精细插值计算 
↓ 
Step 8: 输出 α²F(ω)、λ、Tc
---

## 关键输入参数（EPW部分）

```fortran
&inputepw
  prefix      = 'h3s'
  amass(1)    = 32.06    ! S
  amass(2)    = 1.008    ! H

  ! Wannier参数
  nbndsub     = 16
  bands_skipped = 'exclude_bands = 1:4'

  ! 粗网格（与声子计算一致）
  nk1 = 8   nk2 = 8   nk3 = 8
  nq1 = 4   nq2 = 4   nq3 = 4

  ! 精细网格（越密越精确）
  nkf1 = 40  nkf2 = 40  nkf3 = 40
  nqf1 = 20  nqf2 = 20  nqf3 = 20

  ! 计算选项
  elph        = .true.
  epbwrite    = .true.
  epbread     = .false.

  ! Eliashberg计算
  eliashberg  = .true.
  muc         = 0.13     ! 库仑赝势μ*

  ! 输出
  a2f         = .true.
/
```

---

## 关键输出文件

| 文件 | 内容 |
|------|------|
| `prefix.a2f` | Eliashberg谱函数 α²F(ω) |
| `prefix.lambda` | 各q点的λ(q,ν) |
| `prefix.lambda_k_pairs` | k空间电声耦合分布 |

---

## 结果分析

### 从 α²F(ω) 提取参数
$$\lambda = 2\int_0^\infty \frac{\alpha^2F(\omega)}{\omega}d\omega$$

$$\omega_{log} = \exp\left(\frac{2}{\lambda}\int_0^\infty \frac{\alpha^2F(\omega)\ln\omega}{\omega}d\omega\right)$$

### 判断计算是否可靠
- λ 值与文献相符
- α²F(ω) 形状合理（无负值）
- Tc 与实验值接近

---

## 氢化物计算经验

- 精细k网格建议 40×40×40 以上
- H 的高频声子需要足够大的频率范围
- μ* 通常取 0.10~0.13
- 计算量大，建议在集群上运行

---

## 相关笔记
- [[PHONON计算流程]]
- [[声子机制]]
- [[Eliashberg方程]]
- [[λ与Tc计算]]
- [[理论计算MOC]]
