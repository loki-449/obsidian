---
tags:
  - pbs
  - hpc
  - 集群
  - 指令速查
created: 2026-06-14
---

# PBS 服务器常用指令速查

## 一、PBS 基本概念

PBS（Portable Batch System）是 HPC 集群最常用的作业调度系统之一。用户通过 PBS 提交计算任务（Job），由调度器根据资源情况分配给计算节点执行。

---

## 二、常用命令快速索引

| 命令 | 功能 | 常用场景 |
|------|------|----------|
| `qsub` | 提交作业 | 提交脚本或交互式任务 |
| `qstat` | 查看作业状态 | 检查排队/运行/完成情况 |
| `qdel` | 删除/取消作业 | 中止某个作业 |
| `qhold` | 挂起作业 | 暂不执行但保留排队位置 |
| `qrls` | 释放挂起作业 | 恢复被 hold 的作业 |
| `qalter` | 修改作业属性 | 修改已提交作业的参数 |
| `qrerun` | 重新运行作业 | 重跑已结束/异常退出作业 |
| `qmsg` | 向作业发送消息 | 向运行中作业写入日志 |
| `qselect` | 按条件筛选作业 | 批量查找和处理作业 |
| `qorder` | 调整作业顺序 | 改变作业在队列中的顺序 |
| `qmove` | 移动作业到其他队列 | 作业换队列 |
| `qsig` | 向作业发送信号 | 发送 SIGTERM 等 |
| `qinfo` | 查看队列信息 | 检查队列状态和资源配置 |

---

## 三、命令详解

### 1. qsub —— 提交作业

```bash
# 提交一个批处理脚本
qsub job.sh

# 指定队列和名称
qsub -q express -N my_job job.sh

# 交互式作业（申请节点后进入 shell）
qsub -I -l nodes=1:ppn=4,walltime=1:00:00

# 提交时直接指定资源
qsub -l nodes=2:ppn=8,walltime=12:00:00,mem=64gb job.sh

# 提交依赖作业（依赖 jobid 成功完成后才启动）
qsub -W depend=afterok:123456 job.sh
```

**交互式作业参数**：`-I` 申请一个交互式 shell，常用于调试和短时计算。

---

### 2. qstat —— 查看作业状态

```bash
# 查看所有作业
qstat

# 查看指定作业详情
qstat -f 123456

# 查看指定队列的作业
qstat -q express

# 只看某个用户的作业
qstat -u username

# 简洁模式（只显示 jobid、状态、队列）
qstat -s

# 查看已完成的作业（如果集群开启了历史记录）
qstat -x -u username
```

**状态码含义**：

| 状态 | 含义 |
|------|------|
| `Q` | 排队中（Queued） |
| `R` | 运行中（Running） |
| `H` | 被挂起（Held） |
| `E` | 正在结束（Exiting） |
| `C` | 已完成（Completed） |
| `S` | 挂起（Suspended） |

---

### 3. qdel —— 删除/取消作业

```bash
# 删除指定作业
qdel 123456

# 强制删除（发送 SIGKILL）
qdel -s 123456

# 批量删除（结合 qselect）
qdel $(qselect -u username -s Q)
```

---

### 4. qhold —— 挂起作业

```bash
# 挂起指定作业，保留排队位置不执行
qhold 123456

# 挂起一个范围内的作业
qhold 123456-123460

# 挂起所有排队中的作业
qhold $(qselect -s Q -u username)
```

**挂起类型**：
- 普通 hold：用户自行释放
- USER hold：用户级挂起
- OTHER hold：其他用户或管理员挂起
- SYSTEM hold：系统级挂起

---

### 5. qrls —— 释放挂起作业

```bash
# 释放被 hold 的作业
qrls 123456
```

---

### 6. qalter —— 修改作业属性

```bash
# 修改作业名称
qalter -N new_name 123456

# 修改资源需求
qalter -l walltime=24:00:00,mem=128gb 123456

# 修改输出文件路径
qalter -o /path/to/output.log 123456

# 修改邮件通知设置
qalter -M user@example.com -m bea 123456
```

> 注意：作业已开始运行后，部分属性无法修改。

---

### 7. qrerun —— 重新运行作业

```bash
# 重跑一个作业（相当于删除后重新提交）
qrerun 123456
```

---

### 8. qmsg —— 向作业发送消息

```bash
# 向作业的标准输出写入消息
qmsg "Something went wrong, check logs" 123456
```

---

### 9. qselect —— 按条件筛选作业

```bash
# 筛选所有排队中的作业
qselect -s Q

# 筛选某个用户的作业
qselect -u username

# 筛选特定队列中的作业
qselect -q express

# 筛选特定名称的作业
qselect -N "my_job*"

# 组合筛选：express 队列中排队中的作业
qselect -q express -s Q -u username
```

---

### 10. qorder —— 调整作业顺序

```bash
# 将作业 123457 移到作业 123456 之前
qorder 123457 123456
```

> 需要管理员权限或队列策略允许。

---

### 11. qmove —— 移动作业到其他队列

```bash
# 将作业移动到另一个队列
qmove bigmem 123456

# 批量移动
qmove express $(qselect -N "test*" -s Q)
```

---

### 12. qsig —— 向作业发送信号

```bash
# 发送 SIGTERM（优雅终止）
qsig -s SIGTERM 123456

# 发送 SIGUSR1（自定义信号，需要作业内部处理）
qsig -s SIGUSR1 123456
```

---

### 13. qinfo —— 查看队列信息

```bash
# 查看所有队列情况
qinfo

# 查看某个队列详情
qinfo -q express
```

---

## 四、PBS 脚本指令（#PBS 参数）

提交的 Shell 脚本中可以通过 `#PBS` 注释行设置作业参数。

```bash
#!/bin/bash
#PBS -N my_job              # 作业名称
#PBS -q express              # 提交到哪个队列
#PBS -l nodes=2:ppn=8        # 申请 2 个节点，每节点 8 个核
#PBS -l walltime=12:00:00    # 最长运行时间（hh:mm:ss）
#PBS -l mem=64gb             # 内存需求
#PBS -l ncpus=16             # CPU 核数（新版 PBS 推荐）
#PBS -l ngpus=1              # GPU 数量
#PBS -l vmem=128gb           # 虚拟内存
#PBS -o /path/to/stdout.log  # 标准输出文件
#PBS -e /path/to/stderr.log  # 标准错误输出文件
#PBS -j oe                   # 合并标准输出和错误输出（oe/eo/n）
#PBS -M user@example.com     # 通知邮箱
#PBS -m bea                  # 何时发邮件：b=开始 e=结束 a=异常中止
#PBS -V                      # 继承所有环境变量
#PBS -d /path/to/workdir     # 工作目录
#PBS -S /bin/bash            # 指定脚本解释器
#PBS -t 1-10                 # 作业数组（10 个子任务）
#PBS -W group_list=mygroup   # 指定用户组
#PBS -A project_name         # 计费项目
#PBS -P project              # 项目名称
#PBS -k do                   # 保存输出到运行节点（d=删除 o=保留）
```

**`-j oe` 说明**：
- `oe` —— 将标准错误合并到标准输出
- `eo` —— 将标准输出合并到标准错误
- `n` —— 不合并（默认）

**`#PBS -l` 常用资源参数速查**：

| 参数 | 示例 | 说明 |
|------|------|------|
| `nodes` | `nodes=2:ppn=8` | 节点数和每节点 CPU 数（传统 PBS） |
| `ncpus` | `ncpus=16` | CPU 核数（新版 PBS 推荐方式） |
| `ngpus` | `ngpus=2` | GPU 数量 |
| `walltime` | `walltime=48:00:00` | 最大运行时间 |
| `mem` | `mem=64gb` | 物理内存 |
| `vmem` | `vmem=128gb` | 虚拟内存 |
| `mpiprocs` | `mpiprocs=8` | 每节点 MPI 进程数 |

---

## 五、PBS 环境变量

作业在节点上运行时会自动设置以下环境变量，可在脚本中直接使用：

| 变量名 | 含义 |
|--------|------|
| `$PBS_JOBID` | 作业 ID（如 `123456.pbs-server`） |
| `$PBS_JOBNAME` | 作业名称 |
| `$PBS_NODEFILE` | 分配到的节点列表文件路径 |
| `$PBS_NUM_NODES` | 分配的节点数量 |
| `$PBS_NUM_PPN` | 每节点核数 |
| `$PBS_O_WORKDIR` | 提交作业时的原始工作目录 |
| `$PBS_O_HOME` | 提交用户的 home 目录 |
| `$PBS_O_HOST` | 提交作业的机器名 |
| `$PBS_O_QUEUE` | 提交时所在的队列 |
| `$PBS_O_LOGNAME` | 提交作业的用户名 |
| `$PBS_QUEUE` | 作业实际运行的队列 |
| `$PBS_ARRAYID` | 作业数组中的子任务索引 |
| `$PBS_TASKNUM` | 任务编号 |
| `$PBS_ENVIRONMENT` | PBS 环境标识，值为 `PBS_BATCH` 或 `PBS_INTERACTIVE` |
| `$TMPDIR` | 节点的临时目录（计算结束后自动清理） |

```bash
# 典型用法 —— 在脚本中引用环境变量
cd $PBS_O_WORKDIR          # 回到提交目录
echo "Running on node: $(hostname)" > output_${PBS_JOBID}.log
cat $PBS_NODEFILE          # 查看分配的节点列表
```

---

## 六、实用示例

### 示例 1：串行作业脚本

```bash
#!/bin/bash
#PBS -N serial_job
#PBS -l nodes=1:ppn=1,walltime=1:00:00,mem=4gb
#PBS -j oe
#PBS -V

cd $PBS_O_WORKDIR
./my_program input.dat
```

### 示例 2：MPI 并行作业

```bash
#!/bin/bash
#PBS -N mpi_job
#PBS -l nodes=4:ppn=16,walltime=24:00:00
#PBS -j oe
#PBS -V

cd $PBS_O_WORKDIR
mpirun -np 64 -hostfile $PBS_NODEFILE ./mpi_program
```

### 示例 3：GPU 作业

```bash
#!/bin/bash
#PBS -N gpu_job
#PBS -l nodes=1:ppn=4:gpus=2,walltime=12:00:00
#PBS -j oe
#PBS -V

cd $PBS_O_WORKDIR
export CUDA_VISIBLE_DEVICES=0,1
./cuda_program
```

### 示例 4：作业数组

```bash
#!/bin/bash
#PBS -N array_job
#PBS -l nodes=1:ppn=1,walltime=2:00:00
#PBS -t 1-100
#PBS -j oe

cd $PBS_O_WORKDIR
./process_data.sh input_${PBS_ARRAYID}.txt
```

### 示例 5：依赖作业（串行流水线）

```bash
# 先提第一个作业
job1=$(qsub step1.sh)
echo "Step 1: $job1"

# 依赖 job1 成功后运行 job2
job2=$(qsub -W depend=afterok:$job1 step2.sh)
echo "Step 2: $job2"

# 依赖 job2 成功后运行 job3
job3=$(qsub -W depend=afterok:$job2 step3.sh)
echo "Step 3: $job3"
```

**依赖类型**：

| 依赖类型 | 含义 |
|----------|------|
| `afterok:ID` | 指定作业正常退出后执行 |
| `afternotok:ID` | 指定作业异常退出后执行 |
| `afterany:ID` | 指定作业任意方式结束后执行 |
| `after:ID` | 指定作业开始运行后执行 |
| `before:ID` | 在当前作业之前执行 |

---

## 七、完整工作流示例

```bash
# 1. 查看集群信息和可用队列
qinfo
qstat -q

# 2. 提交作业
qsub run_simulation.pbs

# 3. 监控作业状态
watch -n 5 qstat -u $USER

# 4. 作业排队太长，修改资源（如果允许）
qalter -l walltime=48:00:00 123456

# 5. 作业出现问题，先挂起
qhold 123456

# 6. 检查脚本后释放
qrls 123456

# 7. 作业异常需要重跑
qrerun 123456

# 8. 彻底取消
qdel 123456
```
