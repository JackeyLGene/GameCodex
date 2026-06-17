# Phase 1 — Go SHP Structure Scan

**日期:** 2026-06-14  
**状态:** Phase 1 初步结果。  
**结论:** Cross-harm 全局稳定；chroma 与 rhythm 两轴各自发生显著位移。AI 后围棋不是改变了色度-节奏耦合，而是在同一耦合结构下移动了操作点。

---

## 1. 编码

本轮沿用 SHP 的正交编码逻辑：

```text
每手棋 = (chroma, rhythm)
```

| 轴 | 含义 | 围棋解释 |
|----|------|----------|
| Chroma | 棋局生命周期位置 | 第几步、阶段、开局/中盘/收官等 |
| Rhythm | 与现存棋子的空间关系 | 是否开新话题、回应对手、贴身压迫、延续己方结构 |

关键思想：同一坐标落子在不同局面中不是同一个事件。`pd` 在空角第一手与在挂角后回应局部战斗，属于不同 rhythm 状态。

## 2. 主结果

整体 cross-harm：

| 指标 | 效应 |
|------|------|
| cross-harm | d = -0.029 |

解释：色度-节奏耦合无全局变化。AI 前后并未重写 chroma-rhythm 的耦合结构。

## 3. Rhythm 单轴位移

节奏维度出现显著单轴效应：

| rhythm feature | effect size | 方向解释 |
|----------------|-------------|----------|
| `dens_delta` | d = +3.30 | 最强信号；局部密度差/空间压力结构显著改变 |
| `is_corner_open` | d = -2.54 | AI 后更多空角落子 |
| `adj_opp` | d = -1.45 | AI 后更多贴对手 |
| `adj_own` | d = +0.97 | AI 后更少延己方 |
| `dist_near_opp` | d = +0.96 | AI 后离对手更近 |

工作解释：

> AI 后的空间节奏更偏向对手关联和可控压迫，而不是单纯延展己方结构。

这与围棋 AI 时代的体感一致：棋手不只是开局选择变新，而是更早、更主动地在空间关系上压近对手，追求可控的局面规划。

## 4. Chroma 单轴位移

色度维度也发生位移：

| chroma feature | effect size / value | 方向解释 |
|----------------|---------------------|----------|
| opening 阶段 | d = +1.51 | AI 后开局占比较低 |
| mid 阶段 | d = -2.07 | AI 后中盘占比增加 |
| 平均棋局长度 | 105.5 -> 106.7 | 稍长 |

工作解释：

> 棋局生命周期往外推了：开局相对压缩，中盘权重增加，棋局略长。

## 5. 为什么 cross-harm 不变

初始预期可能是 AI 会改变 cross-harm。但 Phase 1 显示更细的结构：

```text
chroma axis shifts outward   -> 更多中盘、更长生命周期
rhythm axis shifts inward    -> 更贴对手、更强对手关联
cross-harm global coupling   -> 近似抵消，d=-0.029
```

因此不是“cross-harm 变了”，而是：

> 耦合没变，但两个轴的分布各自位移，并在 cross-harm 标量上相互抵消。

这使结果比 entropy / novelty 更精确。Entropy 只能读出多样性变化；SHP 读出的是同一耦合场中的操作点迁移。

## 6. 当前解释

Phase 1 的最好表述：

> AI 没有改变围棋 chroma-rhythm 的耦合结构；它改变了棋手在该耦合结构中的操作点。

操作点变化表现为：

1. 棋局阶段更偏中盘。
2. 空间 rhythm 更贴近对手。
3. 己方延展倾向下降。
4. 局部密度/压力差成为最强信号。

这支持一个较窄、但有力的 AI-era 假说：AI 不是让棋谱“更乱”或“更多样”，而是把人类职业棋的空间节奏推向更强的对手关联与可控规划。

## 7. 下一步

Phase 2 不应再把主问题设为“cross-harm 是否变化”。更好的问题是：

> Phase 1 发现的 rhythm-axis shift，是否与 KataGo policy alignment 同向？

待检验：

| Phase 1 读数 | Phase 2 AI 对照 |
|--------------|-----------------|
| 更贴对手 | KataGo top-k 是否更偏好 opponent-proximal moves |
| 更少延己方 | KataGo policy 是否降低 self-extension 权重 |
| dens_delta 强位移 | KataGo policy mass 是否与 density-pressure feature 对齐 |
| 中盘占比增加 | AI alignment 是否在 move 20-80 最强 |

如果 Phase 2 显示 KataGo top-k move 与这些 rhythm 特征同向，则 Phase 1 可以解释为 AI 外部 Codex 正在重写人类棋手的空间操作点。

## 8. 边界

| 边界 | 处理 |
|------|------|
| Phase 1 尚无 KataGo 对照 | 不直接声称 AI 因果，只称 AI-era shift |
| Cross-harm 无效应 | 不作为失败；标量耦合稳定本身是结果 |
| 单轴效应需查方向定义 | 发表前必须确认每个 feature 的符号方向 |
| 数据源/样本需归档 | 必须记录年份切分、样本量、SGF 解析规则 |

## 9. 里程碑句

GoCodex Phase 1 的初步结论：

> AI 时代没有重写围棋的 chroma-rhythm 耦合；它在同一耦合结构下移动了操作点，使职业棋的空间节奏更贴近对手、更强调局部密度压力，并把棋局生命周期推向中盘。

