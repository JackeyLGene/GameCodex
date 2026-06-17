# GameCodex — 棋类开局/定式作为 Codex 沉积实验域

**创建日期:** 2026-06-14  
**状态:** 新工作方向；synthetic pilot 已通过。用于重启 EE 的 Codex operation 主线。  
**核心问题:** 历史沉积的棋类开局/定式 Codex，是否能在有限记忆压力下提高对未来选择、采用和淘汰的预测？

---

## 1. 为什么是棋类

M32 关闭了生物线作为默认主战场后的一个方法论结论：EE 最适合符号基底清晰、执行轨迹可观测、选择压力明确的系统。

棋类满足这一组条件：

| EE 要求 | 棋类对应 |
|---------|----------|
| 符号基底清楚 | 棋步、局面、开局树、定式序列 |
| 规则封闭 | 合法性可验证，空间有限但复杂 |
| 代际继承 | 棋谱、定式书、AI 推荐、训练库 |
| 选择压力 | 胜负、采用率、顶尖棋手复用、淘汰 |
| 缓冲层稳定 | 棋盘状态就是执行缓冲层，不需要厚现实解释 |
| 可做 held-out | 用过去年份预测未来采用、存活和操作点位移 |

这条线不是再找一个“检测域”，而是寻找 EE 当前最缺的东西：**Codex operation 的自然实验域**。

### 2026-06-14 Synthetic Pilot

最小闭环已跑通：

```text
generate game-like move sequences
  -> build historical Codex
  -> predict held-out future moves
  -> compare against global frequency baseline
  -> test noise sensitivity
```

结果：

| 条件 | Codex vs Frequency |
|------|--------------------|
| Main synthetic pilot | Δ = +0.637 bits |
| Noise = 0.1 | Δ = +1.108 bits |
| Noise = 0.5 | Δ = +0.300 bits |

解释：低噪声时历史序列结构提供明显增量；高噪声时 Codex 退化接近 frequency。概念验证成立。详见 `results/PILOT_SYNTHETIC_2026-06-14.md`。

围棋主线计划：`docs/GO_TIMELINE_PLAN_2026-06-14.md`。

研究对话沉淀：`docs/RESEARCH_DIALOGUE_2026-06-14.md`。

Phase 1 围棋 SHP 初步结果：`results/PHASE1_SHP_GO_2026-06-14.md`。Cross-harm 全局稳定 (`d=-0.029`)，但 rhythm 轴显著位移：`dens_delta d=+3.30`，`is_corner_open d=-2.54`，`adj_opp d=-1.45`，提示 AI 时代改变的是同一 chroma-rhythm 耦合下的操作点，而非耦合结构本身。

Phase 2 KataGo alignment 初步结果：`results/PHASE2_KATAGO_ALIGNMENT_2026-06-14.md`。整体 rhythm gap 不变 (`d=-0.008`)，但 Phase 1 最强的三个 rhythm 位移与 KataGo 选择性对齐：`adj_opp -0.220 -> -0.016`，`adj_own -0.209 -> +0.007`，`dens_delta +0.216 -> -0.043`。结论：AI 后人类在贴身对抗/密度压力维度上向 KataGo policy 收敛，但在 `dist_last` 和 `is_corner_open` 上保留独立。

Phase 0.5 长历史基线结果：`results/PHASE0_5_LONG_HISTORY_2026-06-14.md`。AI-era drift (2010s→2020s) 为 `|drift|=0.0130`，位于 pre-2016 historical envelope 内 (`0.0146±0.0098`, `Z=-0.16`)；单个特征也未显著突破封套。最大历史漂移为 1910s→1920s (`|drift|=0.034`)，约为 AI-era 的 2.6x。结论：AI 不是断裂，而是世纪尺度 Codex 演化的连续阶段。

Phase 0.6 CWI archive composition audit：`results/PHASE0_6_CWI_ARCHIVE_COMPOSITION_2026-06-14.md`。区域距离长期收敛 (`slope=-0.0025/year`)，但 AI 后没有明显加速 (`2020s=0.0082` vs `2010s=0.0085`)。真正有信息量的是 CWI 数据自身从日本档案变成跨国棋谱流通网络：JPN/KOR/CHN 从 `58,371/0/0` (1950s) 变为 `426,114/57,453/7,245` (2020s)。结论：中韩棋谱从零到万，是 Codex 流通结构变迁的化石证据。

Phase 3 Codex operation 加强基线结果：`results/PHASE3_CODEX_OPERATION_2026-06-14.md`。Human Codex 在 22/22 个 held-out 年份上超过 frequency baseline (`Δ=+0.120 bits/move`, `p≈0`)；recency 也超过 frequency (`Δ=+0.094`)，但全史 Codex 在 19/22 年上超过 recency (`p=0.000428`)。Bootstrap CI 全部大于 0：E0 `[+0.082,+0.131]`，E1 `[+0.084,+0.231]`，E2 `[+0.059,+0.125]`，E3 `[+0.135,+0.197]`；E2→E3 recovery `+0.076 bits`。

Phase 0.5 + Phase 4 convergence：`results/PHASE05_PHASE4_CONVERGENCE_2026-06-14.md`。Phase 4A-E 已经把历史基线、档案解构、区域控制、1910s 拆解、pattern 传播和区域 rhythm 收束到同一条线：AI 没有重写棋步结构；它重写了 Codex 被发现、传播和锁定的速度。`Japan-only` 保留 Full CWI 的漂移信号，说明信号在棋步里，不在档案构成里；1910s→1920s 是 Oteai 制度革命，2010s→2020s 是 Oracle 速度革命；pattern 采纳从 6.3 年降至 1.5 年 (`4.2x`)，锁定率从 35% 升至 78%。

Phase 4E regional rhythm：`results/PHASE4E_REGIONAL_RHYTHM_ORACLE_CONVERGENCE_2026-06-14.md`。1990-2015 区域 rhythm 签名显示 JPN 厚实/地域型、KOR 战斗/灵活型、CHN 战斗+高机动型。区域距离呈现 AI 三阶段：1990s `0.0186` 分散，2016-17 `0.0070` shock 收敛，2018-21 `0.0121` 分化吸收，2022-25 `0.0065` oracle 稳定。韩国战斗指数在 AI diffusion 期达到历史最高 (`+0.038`)。结论：AI 没有简单抹平区域风格；它先制造共同震荡，再放大区域性吸收，最后让 Oracle Codex 稳定收敛。

Phase 4 CWI Codex Flow 计划：`docs/PHASE4_CWI_CODEX_FLOW_PLAN_2026-06-14.md`。计划文档现在作为后续路线图保留：player-level propagation network、4F KataGo historical replay，以及 Phase 5 论文骨架。

## 2. 核心假说

棋类开局/定式理论是一种可测量的 Codex 沉积。

在前 AI 时代，开局/定式主要由人类比赛胜负、棋手声望、流派和训练共同选择。AlphaGo、Leela、KataGo、Stockfish NNUE 等强 oracle 出现后，顶尖棋手的选择机制可能发生局部重排：AI 外部 Codex 被吸收到人类代际 Codex 中，尤其体现在可分解的 rhythm 维度上。

一句话：

> AI 之后，顶尖棋手不只是变强了；他们开始查询一个外部 Codex。

这正对应柯洁所说的“现在的围棋比赛已经变成了背 AI 谱子”的体感。该体感可以被操作化为：AI-policy alignment 上升、novelty burst、旧定式半衰期缩短、采用延迟下降，以及历史胜负/声望基线解释力下降。

## 3. 研究对象

优先级暂定：

| 优先级 | 对象 | 用途 |
|--------|------|------|
| 1 | 国际象棋开局 | 数据最公开，PGN/Stockfish/Lichess 可做快速 pilot |
| 2 | 围棋布局/定式 | 最符合“AI 谱系吸收”叙事，需先解决公开棋谱和 KataGo 复算 |
| 3 | 其他竞技策略谱系 | 作为扩展：speedrun 路线、卡牌 deck archetype、电竞 build order |

国际象棋适合作为工程试验场；围棋更可能成为叙事主场。

## 4. Codex 定义

在本方向中，Codex 不等于完整棋谱数据库。Codex 是经过有限记忆压力压缩后仍然存活的结构：

| 层级 | 可能编码 |
|------|----------|
| Opening path | 前 N 手序列、ECO code、局面 hash |
| Local pattern | 围棋局部定式 patch、棋形 hash、角部/边部/中央区域标签 |
| Transition | 从一个局面类型到下一步选择的边 |
| Survival | 后续年份是否继续被采用 |
| Selection | 胜率、采用率、顶尖棋手采用、AI top-k 推荐 |
| Operation | 历史 Codex 是否提高未来选择预测 |

EE 关心的不是“棋手为什么这么下”的语义解释，而是：哪些结构在历史压缩和选择中存活，并能否帮助后来的读者选择。

## 5. 第一批读数

| 读数 | 含义 |
|------|------|
| Opening entropy | 前 N 手/定式选择的多样性 |
| Novelty rate | 新变例或新局部型出现率 |
| Survival half-life | 新变例从出现到消失/稳定的半衰期 |
| Adoption lag | AI 推荐或顶尖局首用到群体采用的延迟 |
| Codex reuse | 历史高权重结构在未来被复用的比例 |
| AI-policy alignment | 实战选择落入 AI top-k 推荐的比例 |
| Prestige vs oracle | 棋手声望/胜负基线与 AI 推荐基线的解释力对比 |

## 6. 第一阶段实验

### Phase 0 — 文献与数据审计

目标：确认已有研究、数据许可、可复现路径和最小可跑数据集。

需要审计：

- 棋类文化传播与 move choice 文献
- 开局相似网络与未来采用预测文献
- 围棋 AI 前后布局/定式变化文献
- Lichess / master games / Stockfish eval 数据
- 围棋公开棋谱、KataGo 复算成本和许可

### Phase 1 — Chess Pilot

目标：用国际象棋验证 Codex operation 的最小闭环。

基本设计：

1. 按年份切分 PGN 数据。
2. 以前 N 手或开局树边作为符号流。
3. 用历史窗口形成 opening Codex。
4. 在 held-out 年份预测哪些 opening path / edge 会被采用、扩散或死亡。
5. 对比 frequency、recency、win-rate、Elo、engine-eval 基线。

成功标准：Codex 模型在 held-out 年份上超过简单 frequency/recency 基线，并且增益不是由样本量或 Elo 混杂解释。

### Phase 2 — Go / AI Transition

目标：检测 AlphaGo/KataGo 前后，围棋布局/定式的 Codex 操作点位移与选择性吸收。

基本设计：

1. 将职业棋谱按时代切分：pre-AlphaGo、AlphaGo shock、KataGo diffusion。
2. 编码前 30-50 手布局和角部局部定式。
3. 测量 entropy、novelty、survival half-life。
4. 用 KataGo 复算关键局面，得到 AI top-k policy。
5. 检验 AI-policy alignment 是否在 2016 后出现局部上升或斜率改变。

成功标准：AI-policy alignment、novelty rate、定式半衰期或 adoption lag 出现时间上可定位的变化，并在顶尖棋手层更强。

### Phase 3 — Codex Operation

目标：证明不是“历史统计描述”，而是“外部 Codex 改变未来读取”。

核心检验：

```text
historical games <= year t
  -> finite-memory Codex
  -> predict choices/adoptions in year t+1
  -> compare with no-Codex, frequency-only, recency-only, win-rate, AI-only baselines
```

如果 AI Codex 在 2016 后显著提升预测，而人类历史 Codex 的边际贡献下降，则支持：

> 人类开局文化在胜负/声望选择的长历史中，吸收了 oracle recommendation。

## 7. 停止规则

这条线必须继承生物线后的纪律。

| 停止条件 | 处理 |
|----------|------|
| Codex 不超过 frequency/recency 基线 | 不声称 operation，只保留文化演化描述 |
| AI-policy alignment 无局部增益 | 不声称 AI 特异解释，只报告连续漂移或 null |
| 数据许可不可发表 | 不进入主线，改用公开数据集或降级为内部探索 |
| 指标依赖人工语义标注过强 | 降低解释强度，回到纯棋步/局面编码 |
| 围棋数据不足 | 用国际象棋完成方法闭环，围棋保留为叙事动机 |

## 8. 与 EE 主线的关系

GameCodex 不是新的横向应用，而是 EE 的核心缺口实验：

| EE 阶段 | 当前状态 | GameCodex 目标 |
|---------|----------|----------------|
| Formation | WTC 已证明 | 开局/定式结构从历史棋谱中沉积 |
| Selection | WTC 已证明 | 胜负、采用、AI 推荐筛选 Codex |
| Operation | 当前 scaffolded | 历史/AI Codex 提高 held-out 预测 |

如果闭合，GameCodex 将把 EE 从“结构可以外置化”推进到“外置化结构可以在自然符号生态中操作性地改变未来读取”。

## 9. 当前任务清单

- [x] 建立数据审计文档。
- [x] 跑通 synthetic Codex operation 最小闭环。
- [x] 写入围棋 AI 谱系外置化时间线计划。
- [x] 完成 Phase 1 围棋 SHP 结构扫描初步结果。
- [x] 完成 Phase 2 KataGo rhythm alignment 初步结果。
- [x] 将长历史基线与研究对话写入文档。
- [x] 完成 Phase 0.5 long-history baseline：AI-era drift 在历史 envelope 内。
- [x] 完成 Phase 0.6 CWI archive composition audit：数据库构成变化作为 Codex 流通化石。
- [x] 完成 Phase 3 Codex operation 加强基线闭合。
- [x] 写入 Phase 4 CWI Codex Flow 工作计划。
- [x] 完成 Phase 0.5 + Phase 4 convergence：AI 重写 Codex 流通速度，而非棋步结构。
- [x] 完成 Phase 4A-E：档案构成、区域控制、1910s 拆解、pattern adoption/survival、区域 rhythm。
- [x] 完成 Phase 4E：区域 rhythm 与 Oracle convergence。
- [ ] 完成 Phase 4E+：玩家级传播网络。
- [ ] 完成 Phase 4F：KataGo historical replay。
- [ ] 整理 Phase 5 论文骨架。
- [ ] 归档 synthetic pilot 脚本、seed、参数与输出。
- [ ] 选定 chess pilot 的最小公开数据集。
- [ ] 定义 opening path / edge / position hash 编码。
- [ ] 写 baseline：frequency、recency、win-rate、Elo。
- [ ] 写 Codex 压缩模型。
- [ ] 做第一个 yearly held-out 实验。
- [ ] 决定是否进入围棋 KataGo 复算阶段。
