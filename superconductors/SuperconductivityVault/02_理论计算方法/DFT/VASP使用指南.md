---
tags: [理论计算, VASP, DFT]
created: 2026-05-23
---

# VASP 使用指南

## 四个核心输入文件

### 1. INCAR — 计算参数
## 基础设置

SYSTEM = H3S at 155GPa
ISTART = 0 # 从头开始 
ICHARG = 2 # 初始电荷密度 
ENCUT = 800 # 截断能(eV) 
PREC = Accurate # 精度

## 电子步

EDIFF = 1E-8 # 能量收敛标准
NELM = 200 # 最大电子步数 
ALGO = Fast # 算法

## 离子步（结构优化）

IBRION = 2 # 共轭梯度 
NSIM = 4 ISIF = 3 # 优化晶胞+原子 
NSW = 200 # 最大离子步 
EDIFFG = -0.001 # 力收敛标准

## K点采样

ISMEAR = 1 # Methfessel-Paxton 
SIGMA = 0.2 # 展宽

## 磁性

ISPIN = 1 # 非磁性

## 输出

LWAVE = .FALSE. 
LCHARG = .FALSE.
### 2. POSCAR — 晶体结构
H3S Im-3m 155GPa 
1.0 
3.0200 0.0000 0.0000 
0.0000 3.0200 0.0000 
0.0000 0.0000 3.0200 
S H 1 3 
Direct 
0.0000 0.0000 0.0000 
0.5000 0.0000 0.5000 
0.5000 0.5000 0.0000 
0.0000 0.5000 0.5000
### 3. KPOINTS — K点设置
Automatic 
0 
Gamma 
8 8 8 
0 0 0
### 4. POTCAR — 赝势文件
```bash
# 拼接赝势（注意元素顺序与POSCAR一致）
cat ~/POTCAR_PBE/S/POTCAR ~/POTCAR_PBE/H/POTCAR > POTCAR
```

---

## 计算任务类型

### 结构优化
IBRION = 2 
ISIF = 3 # 同时优化晶胞和原子位置 
NSW = 200
### 静态计算
IBRION = -1 
NSW = 0 
ICHARG = 2
### 态密度计算
IBRION = -1 
NSW = 0 
ICHARG = 11 # 读取CHGCAR 
LORBIT = 11 # 分波态密度 
NEDOS = 3000 
EMIN = -15 
EMAX = 15
### 能带计算
IBRION = -1 
NSW = 0 
ICHARG = 11 
LORBIT = 11

KPOINTS需要设置高对称路径
---

## 常见错误处理

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| ZBRENT: fatal error | 电子步不收敛 | 降低SIGMA或换ALGO |
| EDDDAV: call to ZHEGV failed | 内存不足 | 增加核数或NPAR |
| WARNING: Sub-Space-Matrix is not hermitian | k点太少 | 增加KPOINTS密度 |
| Inconsistent Bravais lattice | 对称性问题 | 检查POSCAR结构 |

---

## 高压计算特别注意

- PSTRESS 设置外部压力（kBar）：`PSTRESS = 1550`（155GPa）
- 高压下需要更高 ENCUT
- 注意检查优化后的压力是否收敛到目标值

---

## 提交任务脚本（PBS/Slurm）

```bash
#!/bin/bash
#SBATCH --job-name=H3S
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=32
#SBATCH --time=48:00:00

module load vasp/6.3.0
mpirun -np 64 vasp_std > vasp.log
```

---

## 相关笔记
- [[DFT基础]]
- [[赝势选择]]
- [[PHONON计算流程]]
- [[理论计算MOC]]