# 16 体系 COHP 部署检查表

> 状态标记: ✓=已部署可跑,  ⬦=输入就绪待部署,  ✗=缺失,  ?=待确认

## 部署前准备

每个体系需要在 `scf_cohp/opt/` 下完成结构优化：
- opt/CONTCAR → 收敛的最终结构
- opt/POTCAR  → 合并赝势文件

## 16 体系部署清单

```
□ Ba3AgH7/10  ─  opt/POTCAR 应从 ELFCAR_TOT.ELFCAR_Ba3AgH7_10 的元素: Ba, Ag, H
□ Ba3AuH7/0   ─  opt/POTCAR: Ba, Au, H
□ Ca3PdH7/15  ─  opt/POTCAR: Ca, Pd, H
□ Ca3PtH7/10  ─  opt/POTCAR: Ca, Pt, H
□ Ce3AgH7/8   ─  opt/POTCAR: Ce, Ag, H
□ Ce3AuH7/0   ─  opt/POTCAR: Ce, Au, H
□ Cs3AgH7/5   ─  opt/POTCAR: Cs, Ag, H
□ Cs3AuH7/55  ─  opt/POTCAR: Cs, Au, H
□ La3AgH7/0   ─  opt/POTCAR: La, Ag, H
□ La3AuH7/0   ─  opt/POTCAR: La, Au, H
□ Sr3AgH7/25  ─  opt/POTCAR: Sr, Ag, H
□ Sr3AuH7/19  ─  opt/POTCAR: Sr, Au, H
□ Sr3ZnH7/21  ─  opt/POTCAR: Sr, Zn, H
□ Y3CuH7/12   ─  opt/POTCAR: Y, Cu, H
□ Y3PdH7/8    ─  opt/POTCAR: Y, Pd, H
□ Y3PtH7/1    ─  opt/POTCAR: Y, Pt, H
```

## 部署命令

```bash
# 先确认 opt/ 收敛 + POTCAR 存在
ls /home/test1/hhy/calculation/vasp/Cs3AuH7/55/opt/CONTCAR
ls /home/test1/hhy/calculation/vasp/Cs3AuH7/55/opt/POTCAR

# 批量部署 (所有体系)
cd /home/test1/hhy/calculation/vasp
python /home/test1/hhy/tools/vasp/scripts/scf_cohp/deploy_scf_cohp.py --scan --write-pbs
```

## lobsterin 验证

部署后用 test 脚本检查生成的 lobsterin 是否正确：

```bash
python /home/test1/hhy/tools/vasp/scripts/scf_cohp/make_lobsterin.py \
  /home/test1/hhy/calculation/vasp/Cs3AuH7/55/scf_cohp/POTCAR
# 应输出 basisfunctions + cohpGenerator 行
```

## 提交计算

```bash
python /home/test1/hhy/tools/vasp/scripts/scf_cohp/submit_scf_cohp.py
```

## 运行后检查

```bash
# 确认 LOBSTER 正常完成
tail /home/test1/hhy/calculation/vasp/Cs3AuH7/55/scf_cohp/lobster.log
# 应输出 "finished" 或 "LOBSTER done"

# 确认输出文件存在
ls /home/test1/hhy/calculation/vasp/Cs3AuH7/55/scf_cohp/ICOHPLIST.lobster
ls /home/test1/hhy/calculation/vasp/Cs3AuH7/55/scf_cohp/COHPCAR.lobster
```

## 后处理 (跑完后)

```bash
# 使用 cursor 实现的 extract_cohp.py
python /home/test1/hhy/tools/vasp/scripts/scf_cohp/extract_cohp.py \
  --work-root /home/test1/hhy/calculation/vasp \
  --output cohp_summary.csv
```
