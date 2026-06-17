# Phase 2 — KataGo Rhythm Alignment

**日期:** 2026-06-14  
**状态:** Phase 2 初步结果。  
**结论:** 整体 rhythm gap 不变，但 Phase 1 最强的三个空间节奏位移恰好向 KataGo policy 收敛。AI 后人类不是全面模仿 KataGo，而是在贴身对抗/密度压力维度上选择性收敛。

---

## 1. 问题

Phase 1 发现：

```text
cross-harm global coupling ~ unchanged
rhythm axis shifts strongly
```

Phase 2 的目标是检验这些 rhythm-axis shift 是否与 KataGo policy 同向。

核心问题：

> AI 后职业棋手的空间操作点，是否向 KataGo policy 收敛？

## 2. 聚合结果

整体 rhythm gap：

| 指标 | 结果 |
|------|------|
| d(E0 vs E3) | -0.008 |

聚合层面近似不变。若只看整体 gap，会得到“人类并未更接近 KataGo”的结论。

但逐特征拆开后，信号更清楚：整体 gap 被不同维度的相反变化抵消。

## 3. 选择性收敛维度

三个关键 rhythm 维度向 KataGo policy 收敛：

| feature | E0 human-vs-KataGo gap | E3 human-vs-KataGo gap | 解释 |
|---------|-------------------------|-------------------------|------|
| `adj_opp` | d = -0.220 | d = -0.016 | E3 接近 KataGo |
| `adj_own` | d = -0.209 | d = +0.007 | E3 接近 KataGo |
| `dens_delta` | d = +0.216 | d = -0.043 | E3 接近 KataGo |

这三个维度也是 Phase 1 中最重要的 rhythm 位移方向：

| Phase 1 strongest shift | Phase 2 alignment |
|-------------------------|-------------------|
| `dens_delta` | 收敛 |
| `adj_opp` | 收敛 |
| `adj_own` | 收敛 |

解释：

> AI 后人类在贴身对抗、己方延展、局部密度压力这些空间操作维度上向 KataGo policy 收敛。

## 4. 非收敛 / 分化维度

两个维度没有向 KataGo 收敛，甚至更远：

| feature | E0 human-vs-KataGo gap | E3 human-vs-KataGo gap | 解释 |
|---------|-------------------------|-------------------------|------|
| `dist_last` | d = -0.240 | d = -0.444 | E3 更远 |
| `is_corner_open` | d = +0.061 | d = -0.337 | E3 更远 |

解释：

> AI 后人类在步伐节奏和角部策略上没有完全贴合 KataGo policy，保留了独立变化。

这使结果不是“全面 AI 化”，而是“选择性吸收”。

## 5. 为什么整体 gap 不变

整体 gap 不变并非 null，而是维度抵消：

```text
converging dimensions:
  adj_opp, adj_own, dens_delta

diverging dimensions:
  dist_last, is_corner_open

aggregate rhythm gap:
  d(E0 vs E3) = -0.008
```

如果把 rhythm 压成单一标量，AI 信号会被抵消。SHP 的价值在于保留正交维度，读出选择性收敛。

## 6. 当前解释

Phase 2 的最好表述：

> AI 后人类职业棋在贴身对抗维度上向 KataGo policy 收敛，但在步伐节奏和角部策略上保持独立。AI 外部 Codex 没有整体替代人类棋风，而是选择性重写了部分空间操作点。

这比“人类开始背 AI 谱”更精确：

1. 背的不是完整谱。
2. 收敛的不是所有维度。
3. 最先被吸收的是局部对抗/密度压力的 rhythm 结构。
4. 人类仍在节奏距离和角部选择上保留差异。

## 7. 对 Phase 3 的影响

Phase 3 的 Codex operation 不能再用单一 aggregate gap 做主读数。必须分维度评估：

| Phase 3 读数 | 预期 |
|--------------|------|
| `adj_opp` Codex gain | AI 后增强 |
| `adj_own` Codex gain | AI 后增强 |
| `dens_delta` Codex gain | AI 后增强 |
| `dist_last` Codex gain | 不一定增强，可能保持人类独立 |
| `is_corner_open` Codex gain | 不一定增强，需单独解释 |

核心检验应改为：

> AI Codex 是否只在选择性收敛的 rhythm 维度提供 held-out 增益？

## 8. 边界

| 边界 | 处理 |
|------|------|
| 初步结果 | 需记录样本量、年份切分、KataGo visits、抽样策略 |
| 聚合 gap 不变 | 不作为 null；必须报告逐特征分解 |
| KataGo 是当前 oracle | 不等同于 2016 年 AlphaGo，但可作为现代 AI policy proxy |
| 特征方向需复核 | 发表前检查 `adj_own`、`adj_opp`、`dens_delta` 的符号定义 |

## 9. 里程碑句

GoCodex Phase 2 的初步结论：

> AI 时代的职业围棋并未全面贴合 KataGo；它在局部对抗和密度压力维度上选择性收敛，在步伐节奏和角部策略上保留独立。这说明外部 AI Codex 的吸收是分维度的，而不是整盘棋风的全局替换。

