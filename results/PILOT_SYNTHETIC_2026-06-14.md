# Synthetic Pilot — Codex Operation Minimum Loop

**日期:** 2026-06-14  
**状态:** 最小闭环通过。  
**结论:** 历史棋步序列 Codex 在 held-out 预测上超过全局 frequency 基线；噪声敏感度符合预期。

---

## 1. 目标

验证 GameCodex 的最小闭环是否成立：

```text
generate game-like move sequences
  -> build historical Codex
  -> predict held-out future moves
  -> compare against global frequency baseline
  -> test noise sensitivity
```

这不是自然棋谱结果，也不是发表级证据。它的作用是证明 pipeline 与核心 operation 读数能工作：历史沉积的序列结构可以在未来选择预测中提供超过全局频率的增量信息。

## 2. 核心结果

| 条件 | Codex vs Frequency | 解释 |
|------|--------------------|------|
| Main synthetic pilot | Δ = +0.637 bits | Codex 提供超过全局频率的 held-out 信息 |
| Noise = 0.1 | Δ = +1.108 bits | 低噪声时，历史序列结构优势明显 |
| Noise = 0.5 | Δ = +0.300 bits | 高噪声时，Codex 退化接近 frequency |

核心读数：

> Codex > Frequency: Δ = +0.637 bits

概念验证成立：历史棋步序列信息提高未来棋步预测，超出全局频率基线。

## 3. 为什么这是 Codex operation 信号

EE 之前已经有 Codex formation 与 selection 的证据，但 active operation 仍处于 scaffold 状态。这个 synthetic pilot 提供了最小 operation 信号：

| EE 环节 | Pilot 对应 |
|---------|------------|
| Formation | 从历史棋步序列中构建 Codex |
| Selection | 只保留对后续预测有贡献的历史结构 |
| Operation | Codex 用于 held-out 未来棋步预测，并超过 frequency |

这里的关键不是模型复杂度，而是对照关系：如果 Codex 只是在重复全局热门棋步，它不会超过 frequency baseline。Δ = +0.637 bits 表明历史上下文/序列结构携带额外预测信息。

## 4. 噪声敏感度

噪声实验方向正确：

```text
low noise  -> sequence structure survives -> Codex advantage high
high noise -> sequence structure damaged   -> Codex collapses toward frequency
```

这符合 GameCodex 的机制预期。Codex operation 不是万能预测器；它依赖历史沉积结构仍然可读。当生成过程被高噪声打散，Codex 优势下降。

## 5. 当前边界

| 边界 | 说明 |
|------|------|
| Synthetic only | 尚未接入真实 PGN / SGF 棋谱 |
| Frequency baseline only | 真实数据阶段需要加入 recency、win-rate、Elo、engine-eval 等基线 |
| 生成规则需归档 | 发表前必须保存 generator、seed、参数、split 逻辑 |
| 读数方向成立，不代表自然域成立 | 下一步必须用真实 held-out 年份检验 |

## 6. 下一步

1. 固化 pilot 脚本、参数、seed 与输出格式。
2. 接入真实 PGN 数据，优先使用公开许可数据。
3. 建立 yearly held-out split。
4. 增加 baseline：frequency、recency、win-rate、Elo。
5. 在真实数据上复现 `Codex > Frequency`。
6. 若 chess pilot 成立，再进入 Go / AI transition 线。

## 7. 里程碑句

GameCodex 的 synthetic pilot 跑通了 Codex operation 的最小信号：

> 历史沉积的棋步序列结构，在 held-out 未来选择预测中提供超过全局频率的增量信息，并随噪声上升退化。

