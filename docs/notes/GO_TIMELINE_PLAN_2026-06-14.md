# GoCodex Timeline Plan — 围棋 AI 谱系吸收与 Codex Operation

**日期:** 2026-06-14  
**状态:** 工作计划。围棋作为主叙事，国际象棋作为工程 fallback。  
**目标:** 将“顶尖棋手开始背 AI 谱”的体感转化为可检验的 Codex operation 实验。

---

## 1. 战略判断

GameCodex 的 synthetic pilot 已经证明最小闭环可跑：

```text
historical sequence -> Codex -> held-out prediction -> Codex > frequency
```

下一步不应只寻找更大的合成任务，而应进入一个自然符号生态。围棋优先于国际象棋，因为 AlphaGo / KataGo 带来的外部 oracle 介入时间清晰、公共话题度高，且“人类开局/定式谱系如何吸收 AI oracle”本身就是 EE 的天然问题。

国际象棋保留为 fallback：数据更公开，PGN/engine eval 更容易批量处理；若围棋数据许可或 KataGo 复算卡住，用国际象棋完成方法闭环。

## 2. 核心问题

围棋开局/定式如何把 **AI 外部 Codex** 吸收到既有的**人类代际 Codex** 中？

操作化表述：

> AI 出现后，职业棋手的前中盘选择在哪些可分解 rhythm 维度上表现出 oracle 吸收，又在哪些维度保留人类历史沉积？

## 3. 假说

| 编号 | 假说 | 可测读数 |
|------|------|----------|
| H1 | AlphaGo 后出现 opening/joseki novelty burst | 新局面 hash、新局部型、新边出现率 |
| H2 | 旧定式半衰期缩短 | survival half-life、dropout rate |
| H3 | AI-policy alignment 在 2016/2018 后局部上升或斜率改变 | top-k alignment、policy rank、policy mass |
| H4 | Human Codex 的边际预测力下降 | pre/post 年代分层的 held-out Δ bits |
| H5 | AI Codex 的边际预测力上升 | AI-only / Human+AI vs frequency/recency |

主结果不是“AI 让棋手变强”，而是：

> AI 改变了人类棋类文化中 Codex 的沉积与调用机制。

## 4. 年代切分

| Era | 年份 | 名称 | 解释 |
|-----|------|------|------|
| E0 | 2000-2015 | Human Codex | 前 AlphaGo，人类棋谱、流派、胜负和声望主导 |
| E1 | 2016-2017 | AlphaGo Shock | AlphaGo 公开冲击期，新变化和观念快速扩散 |
| E2 | 2018-2021 | AI Diffusion | Leela / KataGo / AI 训练工具扩散 |
| E3 | 2022+ | Oracle Regime | AI 谱常态化；若数据足够则单独分析 |

若数据只到 2021，则 E3 暂不进入主分析。

## 5. 数据源审计

优先顺序：

| 来源 | 用途 | 风险 |
|------|------|------|
| PAGE professional Go dataset | 首选。1950-2021 职业棋谱并可能带 KataGo 统计 | 需确认许可、字段完整性、是否可发表 |
| CWI Japanese pro SGF archive | 辅助历史职业棋谱 | 偏日本棋谱，时代/地域偏倚 |
| Go4Go | 新近职业棋谱补充 | 可能有订阅或许可限制 |
| JGDB | 大规模 SGF 辅助 | 职业标签和元数据需清洗 |
| KataGo analysis engine | 小样本 AI-policy alignment | 批量复算成本、硬件时间 |

第一阶段必须先写数据审计，不直接大跑。

## 6. 总时间线

### Phase 0 — 数据审计与最小样本

**预计:** 1-2 天  
**目标:** 确认可发表数据源，拿到最小可跑 SGF 样本。

任务：

1. 审计 PAGE、CWI、Go4Go、JGDB 的许可和字段。
2. 统一解析字段：date、players、rank、result、komi、rules、moves。
3. 建立 `raw -> parsed -> yearly split` 的数据目录约定。
4. 输出 `docs/DATA_AUDIT.md`。

验收：

- 至少一个数据源可用于公开结果。
- 至少 10,000 局职业棋可解析。
- 年份字段可用，能分 era。

停止条件：

- 若围棋职业棋谱许可不可发表，转国际象棋 pilot。

### Phase 0.5 — Long-History Baseline

**预计:** 2-4 天  
**目标:** 给 AI 时代建立几百年尺度的历史零点，判断 2016 后变化是断点、加速，还是长期趋势延续。

Phase 0.5 初步结果已闭合：AI-era drift (`2010s -> 2020s`, `|drift|=0.0130`) 位于 pre-2016 historical envelope 内 (`0.0146 ± 0.0098`, `Z=-0.16`)。最大历史漂移为 `1910s -> 1920s` (`|drift|=0.034`)，约为 AI-era 的 2.6x。AI 不是断裂；它是长期 Codex 外置化过程中的连续阶段。

Phase 0.6 数据媒介层结果也已闭合：区域距离长期收敛 (`slope=-0.0025/year`)，但 AI 后没有明显加速 (`2020s=0.0082` vs `2010s=0.0085`)。更关键的是 CWI 数据库自身从日本档案扩展为跨国棋谱流通网络，JPN/KOR/CHN 计数从 1950s 的 `58,371/0/0` 变为 2020s 的 `426,114/57,453/7,245`。这不是单纯风格趋同，而是 Codex 流通结构变迁的化石证据。

核心转向：

> 不只问 AlphaGo 后有没有变化，而是问：在围棋 Codex 几百年沉积史中，AI 是否创造了一个超出历史漂移范围的 feature-wise 位移？

长历史 era 切分：

| Era | 年份 | 名称 | 机制 |
|-----|------|------|------|
| L0 | 1600-1850 | Classical Codex | 师承、棋书、局部流派 |
| L1 | 1850-1945 | Modern Institutional | 报刊、头衔战、职业制度 |
| L2 | 1945-1995 | Database Prehistory | 战后职业化、国际交流、现代定式整理 |
| L3 | 1995-2015 | Internet Codex | 棋谱库、在线对弈、搜索式学习 |
| L4 | 2016-2021 | AI Shock / Diffusion | AlphaGo、Leela、KataGo 扩散 |
| L5 | 2022+ | Oracle Regime | AI 谱常态化；若数据足够则单独分析 |

长历史读数：

| 读数 | 长历史意义 |
|------|------------|
| decade cross-harm | 棋局生命周期与空间节奏耦合是否长期稳定 |
| rhythm centroid | 空间操作点的长期漂移 |
| opening entropy | 定式谱多样性是否随媒介变化扩大 |
| novelty rate | 新变化出现速度 |
| survival half-life | 新变化淘汰/稳定速度 |
| feature-wise drift envelope | AI 后位移是否超出历史漂移带 |
| archive composition | CWI 本身是否从局部档案变成跨国流通网络 |

三种可接受结果：

| 结果 | 解释 |
|------|------|
| 长期稳定 + AI 局部位移 | 耦合场稳定，外部 AI Codex 改变局部操作点 |
| 互联网先加速，AI 改方向 | 互联网改变传播速度，AI 改变选择准则 |
| AI 在历史 envelope 内 | 当前结果。AI 不是断裂；改写为长期外置化史中的连续阶段与选择性吸收 |

验收：

- 至少按 decade 输出 `cross-harm`、rhythm centroid、feature-wise drift。
- 给 Phase 1/2 的 AI-era 结果提供历史漂移 envelope。
- 明确报告数据源地域偏倚，不把日本/韩国/中国局部棋谱误称为全球围棋。
- 将 CWI 全库结果称为 CWI-network result，并在可能时做 Japan-only 或 region-balanced 复核。

### Phase 1 — 无 AI 的棋谱结构漂移扫描

**预计:** 3-5 天  
**目标:** 不依赖 KataGo，先看棋谱自身是否在 AlphaGo 前后有结构断层。

编码：

| 编码 | 说明 |
|------|------|
| Opening prefix | 前 30 / 50 手序列 |
| Board hash | 前 N 手局面 hash，按对称性 canonicalize |
| Local corner patch | 四角局部 9x9 / 11x11 pattern hash |
| Move transition | position_hash -> next_move |

指标：

| 指标 | 解释 |
|------|------|
| opening entropy | 年度前 N 手多样性 |
| novelty rate | 年度新 hash / 新 transition 出现率 |
| reuse rate | 历史高权重 hash 在未来复用比例 |
| survival half-life | 新变化从出现到稳定/消失的时间 |
| era classifier | 仅用开局结构能否区分 pre/post AlphaGo |

验收：

- 至少一个指标在 E0 -> E1/E2 出现可定位变化。
- 变化不只是样本量变化；需要按 yearly game count 做下采样或 bootstrap。

停止条件：

- 若所有无 AI 指标均为连续漂移，不能声称断点；仍可进入 Phase 2 检查 AI alignment。

### Phase 2 — 小样本 KataGo Alignment

**预计:** 5-10 天  
**目标:** 用 KataGo 小样本复算，检测 Phase 1 的 rhythm-axis shift 是否与 AI policy 同向。

Phase 1 已显示：cross-harm 全局稳定 (`d=-0.029`)，但 rhythm 轴显著位移。下一步主问题因此从“AI 是否改变 chroma-rhythm 耦合”转为：

> AI policy 是否偏好 Phase 1 观察到的空间操作点：更强对手关联、更高局部密度压力、更少单纯延展己方结构？

Phase 2 初步结果显示：整体 rhythm gap 不变 (`d=-0.008`)，但 `adj_opp`、`adj_own`、`dens_delta` 三个 Phase 1 关键位移向 KataGo 收敛，而 `dist_last`、`is_corner_open` 未收敛。这意味着后续 Codex operation 必须分维度评估，不能使用单一 aggregate gap。

抽样策略：

| 层 | 建议 |
|----|------|
| 年份 | 2000-2021，每年固定样本数 |
| 棋局 | 每年 500-2000 局，按数据量调整 |
| 局面 | 每局前 50 手，每 5 手取一个局面 |
| 分层 | 顶尖棋手 vs 普通职业棋手；若 rank 可用 |

KataGo 输出：

| 读数 | 说明 |
|------|------|
| top-1 / top-3 / top-5 alignment | 实战手是否在 AI 推荐集合中 |
| policy rank | 实战手在 AI policy 中排名 |
| policy mass | 实战手的 policy probability |
| winrate loss | 实战手相对 top move 的胜率损失 |

主检验：

```text
alignment(year) ~ era + move_number + player_strength + color + rules/komi
```

验收：

- 2016/2018 后 AI-policy alignment 出现局部上升或斜率改变。
- 顶尖棋手层的变化强于普通职业棋手。

停止条件：

- 若 KataGo alignment 无可定位变化，只报告 null 或连续漂移，不声称 oracle regime。

### Phase 3 — Codex Operation Held-out

**预计:** 1-2 周  
**目标:** 证明 Codex 不是历史描述，而是提高未来预测的 operation；并检验 AI Codex 的增益是否集中在 Phase 2 发现的选择性收敛维度。

Phase 3+ 加强基线已闭合：Human Codex 在 22/22 个 held-out 年份上超过 frequency baseline (`Δ=+0.120 bits/move`, `p≈0`)；recency 也超过 frequency (`Δ=+0.094`)，但全史 Codex 在 19/22 年上超过 recency (`p=0.000428`)。Era bootstrap CI 全部大于 0，E2→E3 recovery 为 `+0.076 bits`。下一步重点不是追求更大的 Δ，而是归档脚本、复核 split，并加入 win-rate/player-strength/AI-policy baselines。

最小闭环：

```text
games <= year t
  -> build Human Codex
  -> optionally build AI Codex from KataGo policy
  -> predict choices/adoptions in year t+1
  -> compare baselines
```

模型对照：

| 模型 | 说明 |
|------|------|
| Frequency | 全局热门下一手 |
| Recency | 最近窗口热门下一手 |
| Win-rate | 历史胜率加权 |
| Player-strength | 顶尖棋手采用加权 |
| Human Codex | 历史路径/局面 transition 压缩 |
| AI Codex | KataGo top-k / policy mass |
| Human + AI | 两种 Codex 联合 |

主读数：

| 读数 | 解释 |
|------|------|
| Δ bits vs frequency | Codex 增量信息 |
| Δ bits vs recency | 是否超过近期流行 |
| pre/post Δ | AI 后增益是否转移 |
| adoption AUC | 预测某 transition 是否未来被采用 |
| survival log loss | 预测新变化是否存活 |
| feature-wise Δ | `adj_opp`、`adj_own`、`dens_delta` 是否比 `dist_last`、`is_corner_open` 更受 AI Codex 增益影响 |

当前 Phase 3 边界：

| 边界 | 下一步 |
|------|--------|
| frequency + recency 已闭合 | 继续加入 win-rate、player-strength、AI-policy |
| 效应小但稳定 | 对 22/22 与 19/22 做 split 稳健性检验 |
| Era 波动 | E2 低谷与 E3 恢复已见；继续做长历史 envelope |
| AI alignment 相关弱 | 不声称单变量解释；改做 feature-wise Δ |

理想结果：

| Era | 预期 |
|-----|------|
| E0 Human Codex | Human Codex > AI Codex |
| E1 Shock | Novelty 高，旧 Human Codex 退化 |
| E2 Diffusion | AI Codex 边际贡献上升 |
| E3 Oracle | Human+AI 最强，AI-only 接近或超过 Human-only |

### Phase 4 — CWI Codex Flow & Archive Network

**预计:** Phase 0.5 / 0.6 / 3 之后  
**目标:** 将 CWI 从透明数据源改写为 Codex 外部记忆网络，区分棋步选择变化与档案构成变化。

Phase 4 详细计划见 `docs/PHASE4_CWI_CODEX_FLOW_PLAN_2026-06-14.md`。

Phase 4A-E convergence 结果见 `results/PHASE05_PHASE4_CONVERGENCE_2026-06-14.md`。当前核心结论：

> AI 没有重写围棋的棋步结构——它重写了围棋 Codex 被发现、传播和锁定的速度。

关键读数：

| 读数 | 结果 | 解释 |
|------|------|------|
| Historical envelope | AI-era `|drift|=0.0130`, pre-2016 `0.0146±0.0098` | AI 在历史封套内 |
| Region control | Full CWI `0.0160`, Japan-only `0.0159`, balanced `0.0277` | 信号在棋步里，不在构成里 |
| 1910s->1920s | overlap players 保留 85% drift | Oteai 制度革命是真实棋步重组 |
| Pattern adoption | 6.3 年 -> 1.5 年 (`4.2x`) | AI 改变 Codex 传播速度 |
| Reuse rate | 35% -> 78% (`2.2x`) | AI 提高 pattern 锁定率 |
| Regional rhythm | `0.0186 -> 0.0070 -> 0.0121 -> 0.0065` | shock 收敛、分化吸收、oracle 稳定 |

Phase 4E regional rhythm 结果见 `results/PHASE4E_REGIONAL_RHYTHM_ORACLE_CONVERGENCE_2026-06-14.md`。它从区域视角独立复现 Phase 3 的 `E1 peak -> E2 trough -> E3 recovery`：AlphaGo shock 造成共同收敛，AI diffusion 期各区域以自身风格吸收 AI，Oracle 时代再次稳定收敛。

核心任务：

| 任务 | 目的 |
|------|------|
| Archive composition matrix | 已完成：建立 `decade × region × player × event × source` 构成矩阵 |
| Region-controlled replication | 已完成：Full / Japan-only / balanced 复核 |
| 1910s->1920s decomposition | 已完成：最大历史漂移以真实棋步变化为主 |
| Pattern adoption / survival | 已完成：采纳 4.2x 加速，锁定率 2.2x 提高 |
| Regional rhythm & oracle convergence | 已完成：区域三阶段独立验证 Phase 3 |
| Player-level propagation network | 待做：区分区域风格与顶尖棋手影响 |
| KataGo historical replay | 待做：给选择性 AI 吸收加历史坐标 |

Phase 4 成功标准不是证明 AI 断裂，而是明确：

> CWI-network 中哪些信号属于 move-choice effect，哪些属于 archive-composition effect。

### Phase 5 — 论文骨架与外部叙事

**预计:** Phase 4 之后  
**目标:** 把结果整理为 EE 的 Codex operation 论文或章节。

候选标题：

- *When Players Began to Query the Oracle: AI and the Rewriting of Go Opening Codex*
- *Externalized Codex Operation in Professional Go after AlphaGo*
- *From Human Joseki to Oracle Conformity: A Codex View of Go's AI Transition*

主图草案：

| 图 | 内容 |
|----|------|
| Fig 1 | CWI region composition timeline |
| Fig 2 | Full vs Japan-only vs region-balanced drift envelope |
| Fig 3 | pattern adoption / survival |
| Fig 4 | KataGo historical replay by feature axis |
| Fig 5 | held-out Codex operation Δ bits |

## 7. 最小实现顺序

1. `scripts/phase4a_archive_composition.py`：已完成，输出 `decade × region × player × event × source` 构成矩阵。
2. `scripts/phase4b_region_controlled.py`：已完成，复核 `Full CWI / Japan-only / region-balanced`。
3. `scripts/phase4c_1910s_decompose.py`：已完成，拆解最大历史漂移。
4. `scripts/phase4d_pattern_adoption.py`：已完成，first_seen、adoption_lag、survival_half_life。
5. `scripts/phase4e_regional_rhythm.py`：已完成，区域 rhythm 与 oracle convergence。
6. `scripts/propagation_network.py`：待做，玩家级 pattern 流通网络。
7. `scripts/katago_historical_replay.py`：待做，小样本 KataGo historical replay。
8. `scripts/evaluate_heldout.py`：待扩展，baseline 与 Codex operation 对照。

## 8. 文件组织

```text
game_codex/
  data/
    raw/               # 不提交大型原始数据
    parsed/            # 标准化小样本/索引
    samples/           # 可复现实验子集
  docs/
    DATA_AUDIT.md
    GO_TIMELINE_PLAN_2026-06-14.md
    PHASE4_CWI_CODEX_FLOW_PLAN_2026-06-14.md
  scripts/
    parse_sgf.py
    extract_opening_features.py
    phase1_structure_scan.py
    build_codex.py
    evaluate_heldout.py
  results/
    PILOT_SYNTHETIC_2026-06-14.md
    phase1/
    phase2/
    phase3/
```

## 9. 风险与停止规则

| 风险 | 处理 |
|------|------|
| SGF 许可不清 | 不进入主线；改用可公开数据或国际象棋 |
| 数据地域偏倚 | 按数据源分层报告，不合并成全球职业棋 |
| KataGo 成本过高 | 先做小样本；只分析关键局面 |
| AI alignment 无可定位增益 | 不声称 AI 特异解释，只报告连续漂移或 null |
| Codex 不超过 frequency/recency | 不声称 operation，只保留结构描述 |
| 人工定式标签污染 | 优先使用棋盘 hash / transition，不依赖人工 joseki 名称 |

## 10. 第一周目标

| 天 | 目标 |
|----|------|
| Day 1 | 数据源审计，选定主数据源 |
| Day 2 | SGF parser + 年份/棋步字段验证 |
| Day 3 | 前 50 手 hash / opening prefix + SHP chroma/rhythm 抽取 |
| Day 4 | decade-level long-history baseline 初跑 |
| Day 5 | AI-era Phase 1 scan + 下采样控制 |
| Day 6-7 | Phase 1/0.5 结果文档；决定是否扩大 KataGo 小样本 |

第一周的成功标准不是证明 AI 断裂，而是回答：

> 围棋职业棋谱自身是否足够干净，能不能承载 Codex operation 主线？
