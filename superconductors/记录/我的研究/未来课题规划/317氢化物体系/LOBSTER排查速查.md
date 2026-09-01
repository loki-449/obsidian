# 快速 POTCAR vs lobsterin 手工对照

## 方法: OUTCAR 中查什么

```bash
# 查看 POTCAR 实际携带的轨道
grep VRHFIN POTCAR
# 输出示例: VRHFIN =Ce: 4f 5d 5p 5s 6s

# 查看 OUTCAR 中赝势的轨道信息
grep -A 5 "VRHFIN" OUTCAR
# 或
grep -A 3 "onsite" OUTCAR | head -30
# 或看 OUTCAR 开头列的每个离子类型(带能标记的赝势轨道)
grep "VRHFIN\|TITEL\|ZVAL" OUTCAR
```

## 16 体系逐个检查

你要在集群上对每个体系跑:

```bash
cd $VASP_WORK_ROOT/<体系>/<压强>/scf_cohp/

echo "=== POTCAR VRHFIN ===" && grep VRHFIN POTCAR
echo "=== lobsterin basisfunctions ===" && grep basisfunctions lobsterin
echo "=== OUTCAR VRHFIN ===" && grep VRHFIN OUTCAR
```

三行输出逐元素比对。不一致的元素就是需要修 `lib/lobster_basis.py` 中 `DEFAULT_BASIS` 字典的。

## 已知问题

| 体系 | 问题 | 状态 |
|------|------|------|
| Ce3AgH7_8 | spilling 89%, Bunge→Koga 但缺 4f | 待修 DEFAULT_BASIS['Ce'] |
| Ba3AgH7_10 | spilling 31%, cohpGenerator 只找到 1.0-3.0Å 默认 (非 0.6-1.6) | lobsterin 缺参数 → 检查 POTCAR 是否正常解析 |
| 全部含 f 电子 | k 点全对称 warning | COHP_INCAR 加 ISYM=0 |
