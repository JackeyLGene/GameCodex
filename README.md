# GameCodex

**External oracles accelerate cultural Codex circulation without rewriting structural grammar.**

GameCodex studies professional Go as a natural symbolic ecology: recorded games
form an external memory, players select and reuse patterns, and AI systems act as
external oracles. The current paper argues that the AlphaGo/KataGo era did not
produce the largest observed move-structure drift in the CWI record; instead, it
accelerated how opening patterns are discovered, transmitted, and stabilized.

中文一句话：AI 没有重写围棋棋步结构，但重写了围棋 Codex 被发现、传播和稳定的速度。

## Interactive Pages

The public interactive page lives at [`site/index.html`](site/index.html). It is a static
black-and-white interactive page: SHP board lens, Lee/Ke policy trace,
historical drift envelope, adoption-speed chart, and regional Codex flow.

The football prototype lives at [`football/index.html`](football/index.html).
It uses the same SHP logic on StatsBomb World Cup event data: team
fingerprints, opponent mirrors, and a selectable structural matchup explorer.

## Start Here

| Purpose | File |
|---|---|
| Technical note | [`docs/TECHNICAL_NOTE.md`](docs/TECHNICAL_NOTE.md) |
| Repository map | [`docs/INDEX.md`](docs/INDEX.md) |
| Package status | [`docs/PACKAGE_STATUS_2026-06-15.md`](docs/PACKAGE_STATUS_2026-06-15.md) |
| Reproduction notes | [`REPRODUCE.md`](REPRODUCE.md) |
| Data and large-file policy | [`data/README.md`](data/README.md) |
| Main figures | [`results/figures/`](results/figures/) |
| Final hardening output | [`results/PHASE5_HARDENING_2026-06-15.txt`](results/PHASE5_HARDENING_2026-06-15.txt) |

Legacy planning notes and older manuscript audits are kept under
[`docs/notes/`](docs/notes/) and [`docs/archive/`](docs/archive/).

## Core Findings

| Layer | Result | Interpretation |
|---|---:|---|
| Historical drift | AI-era drift = `0.0130`; pre-2016 mean = `0.0146` | AI-era structure lies inside the historical envelope. |
| Largest historical drift | 1910s to 1920s = `0.0342` | Oteai/Nihon Ki-in institutionalization moved structure more than the AI era. |
| Archive control | Full CWI `0.0160`; Japan-only `0.0159` | Main drift signal is in moves, not just archive composition. |
| Pattern adoption | `6.3` years to `1.5` years | Opening-pattern adoption accelerated about `4.2x`. |
| Reuse density | `0.35` to `0.78` | Recurrent patterns stabilized more densely after AI oracles. |
| Codex operation | Human Codex > Frequency in `22/22` held-out years | Historical move memory improves future move prediction. |
| Regional streams | shock convergence -> diffusion divergence -> oracle re-stabilization | AI adoption is selective and mediated by event-stream history. |

## Why SHP Matters

Each move is factorized into:

- **Chroma:** where the move falls in the game lifecycle.
- **Rhythm:** how the move relates spatially to stones already on the board.

This separates "when in the game" from "how the move answers the current board."
That is the methodological advantage of this project: the analysis does not only
ask whether human moves match AI policy; it asks which structural layer of move
choice changed.

## Main Figures

| Figure | File |
|---|---|
| Fig. 0: Lee Sedol / Ke Jie paired vignette | [`results/figures/fig0_paired_vignette.png`](results/figures/fig0_paired_vignette.png) |
| Fig. 1: Century-scale drift envelope | [`results/figures/fig1_drift_envelope.png`](results/figures/fig1_drift_envelope.png) |
| Fig. 2: Fixed-horizon adoption | [`results/figures/fig2_fixed_horizon_adoption.png`](results/figures/fig2_fixed_horizon_adoption.png) |
| Fig. 3: 1910s decomposition and two mechanisms | [`results/figures/fig3_1910s_decomposition.png`](results/figures/fig3_1910s_decomposition.png) |
| Fig. 4: Regional three-phase response | [`results/figures/fig4_regional_three_phase.png`](results/figures/fig4_regional_three_phase.png) |
| Fig. 5: Pattern adoption and reuse | [`results/figures/fig5_pattern_adoption.png`](results/figures/fig5_pattern_adoption.png) |

## Repository Shape

```text
GameCodex/
  docs/
    TECHNICAL_NOTE.md           current technical note
    INDEX.md                    document map
    notes/                      research plans and dialogue
    archive/                    older drafts and audits
  results/
    figures/                    technical-note and SI figures
    phase*/                     derived aggregate outputs
    PHASE*_*.md                 phase summaries
  scripts/
    generate_figures.py         Figs. 1, 2, 4, 5
    gen_fig3_1910s.py           Fig. 3
    gen_paired_vignette.py      Fig. 0
    gen_si_figures.py           Figs. S1-S3
    phase*.py                   analysis scripts
  data/
    README.md                   data placement and large-file policy
```

Large raw data, parsed CWI tables, KataGo binaries, and model weights are not
tracked in this repository. See [`data/README.md`](data/README.md).
