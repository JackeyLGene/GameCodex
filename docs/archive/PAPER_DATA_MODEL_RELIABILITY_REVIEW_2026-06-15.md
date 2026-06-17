# Paper Data And Model Reliability Review

**Date:** 2026-06-15  
**Draft reviewed:** `docs/PAPER_DRAFT_PNAS_v3.md`  
**Status after review:** internally review-ready; external submission needs final repository/data-availability packaging.  

---

## 1. Verdict

The paper's core empirical chain is reliable enough to enter an internal
review / pre-submission review stage:

> AI-era move-structure drift lies inside the historical envelope, while
> recurrent opening-pattern circulation accelerates sharply after external AI
> oracles enter the Go knowledge system.

The strongest results are now supported by reproducible local scripts and
result files:

1. Century-scale drift envelope.
2. Archive-composition control and Japan-only replication.
3. Pattern adoption / reuse acceleration, including fixed-horizon and bootstrap
   hardening.
4. Held-out Codex operation against frequency and recency baselines.
5. Regional event-stream dynamics, now using the exact five-feature distance
   metric and bootstrap intervals.

The paper should not expand into a new empirical phase. The remaining work is
submission packaging: final figure numbering, repository/data availability,
and traceability of the Figure 0 vignette source.

---

## 2. Checks Performed

Reran or inspected:

```powershell
python scripts/phase5_hardening.py
python scripts/generate_figures.py
python scripts/gen_paired_vignette.py
```

Saved hardening output:

```text
results/PHASE5_HARDENING_2026-06-15.txt
```

Generated / regenerated figures:

```text
results/figures/fig0_paired_vignette.png
results/figures/fig0_paired_vignette_trace.csv
results/figures/fig1_drift_envelope.png
results/figures/fig2_fixed_horizon_adoption.png
results/figures/fig3_regional_three_phase.png
results/figures/fig4_pattern_adoption.png
```

Also verified the external DOI placeholders for the two Go/AI-cultural
references and updated the draft references.

---

## 3. Data Integrity

### Parsed CWI Data

From `data/parsed/go_games_parsed.csv`:

```text
parsed rows:             95,831
records with valid year: 95,076
main 1600-2026 records:  95,071
pre-1600 sparse records: 5
missing-year records:    755
mean game length:        206.8 moves
median game length:      208 moves
min/max game length:     1 / 541 moves
```

Assessment:

**Green.** The draft's "95,000 recorded games, mostly spanning 1600-2026"
language is accurate. The existence of 5 sparse pre-1600 records and 755
missing-year rows is correctly handled by "mostly spanning" and by the Methods
statement that sparse earlier records are excluded from the main century-scale
analysis.

### Archive Composition

From `results/phase4/archive_composition_by_decade.csv`:

| Decade | JPN | KOR | CHN | INTL/Unk | Total | Check |
|---|---:|---:|---:|---:|---:|---|
| 1950s | 1,668 | 0 | 0 | 200 | 1,868 | ok |
| 1980s | 9,640 | 1 | 0 | 106 | 9,747 | ok |
| 2000s | 9,198 | 1,078 | 4 | 831 | 11,111 | ok |
| 2020s | 12,175 | 1,642 | 207 | 523 | 14,547 | ok |

Assessment:

**Green.** The previous unit error is fixed. The table now sums correctly.

---

## 4. Core Model Results

### 4.1 Century-Scale Drift

Source:

```text
results/phase05/decade_drift.csv
```

Recomputed from the five rhythm features:

```text
pre-2016 transitions: n = 15
pre-2016 mean drift:  0.0145777
pre-2016 SD:          0.0097707
pre-2016 min/max:     0.0038003 / 0.0342417
AI-era drift:         0.0130461
maximum drift:        1910s->1920s = 0.0342417
```

Assessment:

**Green.** The central "AI is inside historical envelope" result is stable.
The paper correctly uses "historical envelope / empirical range" rather than a
confidence interval for this result.

### 4.2 Chroma-Rhythm Coupling

Source:

```text
results/PHASE1_SHP_GO_2026-06-14.md
```

Claim:

```text
Cohen's d(E0 vs E3) = -0.029
```

Assessment:

**Green / bounded.** This supports the paper's "operating-point shift within a
stable coupling structure" wording. It should not be expanded into a
four-century coupling claim unless a long-history cross-harm analysis is added.
The current v3 wording stays inside the supported range.

### 4.3 Pattern Adoption And Reuse

Sources:

```text
results/phase4/pattern_metrics.csv
results/PHASE5_HARDENING_2026-06-15.txt
scripts/phase5_hardening.py
```

Main observed metrics:

```text
unique first-15 patterns:       74,501
qualifying recurrent patterns:  546

Observed adoption lag:
pre-1980     6.3 yr
1980-1999    5.7 yr
2000-2015    2.6 yr
2016+        1.5 yr

Observed reuse density:
pre-1980     0.35
1980-1999    0.37
2000-2015    0.67
2016+        0.78
```

Hardening:

```text
Fixed-horizon adoption probability:
pre-1980:  <=1yr 0.31, <=2yr 0.37, <=3yr 0.39, <=5yr 0.44
2016+:     <=1yr 0.57, <=2yr 0.73, <=3yr 0.80, <=5yr 0.91

Adoption-lag ratio: 4.2x [95% CI: 2.9x, 5.9x]
Reuse-density ratio: 2.3x [95% CI: 2.1x, 2.5x]
```

Assessment:

**Green with one explicit boundary.** The direction survives censoring-aware
fixed-horizon analysis and bootstrap resampling. The paper still correctly
phrases the primary metric as "observed adoption lag among qualifying recurrent
patterns"; it should not become "all new patterns adopt 4.2x faster."

### 4.4 Codex Operation

Source:

```text
results/phase3/baselines_plus.csv
```

Recomputed summary:

```text
Human Codex > Frequency: 22/22 years, mean Δ = +0.1195 bits/move
Recency > Frequency:     22/22 years, mean Δ = +0.0940 bits/move
Hist > Recency:          19/22 years

Era means:
E0  +0.1044
E1  +0.1576
E2  +0.0871
E3  +0.1635
```

Assessment:

**Green.** The held-out evidence supports "Codex operation is real and
persistent." It also supports the destabilization/recovery narrative: E1 high,
E2 lower, E3 recovered.

### 4.5 KataGo Selective Alignment

Source:

```text
results/phase2/katago_alignment.csv
scripts/phase2_full.py
```

Setup:

```text
KataGo v1.16.4 OpenCL
model: kata1-b28c512nbt-s13255194368-d5935380940
50 positions per era
ply 30
maxVisits = 100
Japanese rules, komi 6.5
```

Assessment:

**Yellow / supplementary only.** The sample is small but useful as a modern
policy proxy. v3 correctly keeps this as supplementary and does not let it
carry the primary claim.

### 4.6 Regional Event-Stream Dynamics

Source:

```text
scripts/phase5_hardening.py
results/PHASE5_HARDENING_2026-06-15.txt
```

Exact five-feature regional distance:

```text
Pre-AI 1990-2015:   0.0144 [0.0109, 0.0361]
Shock 2016-2017:    0.0066 [0.0037, 0.0151]
Diffusion 2018-2021:0.0167 [0.0109, 0.0323]
Oracle 2022-2025:   0.0102 [0.0056, 0.0212]
```

Assessment:

**Green / bounded.** The pattern is no longer "simple convergence to the
lowest distance." It is:

```text
shock convergence -> diffusion re-divergence -> partial oracle re-convergence
```

v3 now uses this more conservative wording. Event-stream labels remain
tournament/archive provenance, not player nationality; this boundary must stay
visible in the paper.

### 4.7 Figure 0 Paired Vignette

Sources:

```text
scripts/gen_paired_vignette.py
results/figures/fig0_paired_vignette.png
results/figures/fig0_paired_vignette_trace.csv
```

Current supported values:

```text
Lee pre-78:  mean zero-indexed rank 20.26, top1 25.8%, top3 61.3%
Lee move 78: zero-indexed rank 2, top-3 but not top recommendation
Lee post-78: mean zero-indexed rank 3.76, top1 39.0%, top3 82.9%

Ke Jie trace: mean zero-indexed rank 1.44, top1 61.4%, top3 82.9%
```

Assessment:

**Yellow / motivating vignette.** The paired contrast is valuable and now
internally consistent after the rank-index and winrate-perspective fixes.
However, it should remain a motivating case study, not primary evidence. For
external submission, preserve the source trace CSV and be ready to explain that
this is retrospective KataGo analysis, not original AlphaGo policy.

---

## 5. Changes Applied During This Review

Updated `docs/PAPER_DRAFT_PNAS_v3.md`:

1. Replaced "ranked second" with "zero-indexed policy rank 2 / top-3."
2. Replaced unsupported "Ke Jie rank=5, 70% top-1" with values computed from
   the current trace: mean rank 1.4, top1 61%, top3 83%.
3. Normalized the Ke Jie winrate description to human perspective.
4. Added fixed-horizon adoption probabilities and bootstrap ratios.
5. Replaced old regional distances with exact five-feature bootstrap values.
6. Changed regional conclusion to "partial oracle re-stabilization."
7. Added Methods wording for fixed-horizon checks and per-pattern bootstrap.
8. Replaced placeholder Go/AI references with verified DOI metadata.
9. Updated Figure 0 status to generated.

Updated `scripts/gen_paired_vignette.py`:

1. Added Ke Jie winrate inversion to plot human-perspective winrate.
2. Updated rank annotations to match zero-indexed rank values.
3. Exported `fig0_paired_vignette_trace.csv` for figure provenance.

Regenerated:

```text
fig0_paired_vignette.png
fig1_drift_envelope.png
fig2_fixed_horizon_adoption.png
fig3_regional_three_phase.png
fig4_pattern_adoption.png
```

---

## 6. Remaining Risks Before External Submission

### R1. Data Availability And Repository Language

Status: **must resolve before external submission.**

The current wording is safe:

```text
Analysis scripts and derived aggregate result tables will be released...
Source SGF records are available from CWI...
```

But the repository URL, license, and exact release policy must be finalized.
Do not claim that CWI-derived parsed data are CC-BY unless the source license
allows it.

### R2. Figure Production Is Not Yet Fully Matched To The Figure Table

Status: **minor but practical.**

Generated files currently include Figures 0-4, while the draft's conceptual
figure table still lists a separate 1910s->1920s decomposition figure and a
regional Figure 5. This is a numbering / packaging issue, not a scientific
issue. Resolve before manuscript assembly.

### R3. Figure 0 Source Analysis Scripts Are Not Fully Preserved

Status: **minor-to-moderate.**

The trace CSV now exists, but script comments still refer to prior one-off
outputs such as `divine_ai_gap.py` / `kejie_alphago.py`. For a strict
reproducibility package, either restore those scripts or add a short
supplementary note explaining how the trace was produced.

### R4. Regional Labels Must Never Be Reframed As National Style

Status: **conceptual guardrail.**

The paper currently handles this correctly. Maintain the terms:

```text
Japan-coded / Korea-coded / China-coded event streams
```

Avoid:

```text
Japanese style / Korean style / Chinese style
```

unless player-nationality metadata is added.

---

## 7. Final Reliability Matrix

| Component | Status | Main-paper use |
|---|---|---|
| Century-scale drift envelope | Green | Primary |
| Archive composition and Japan-only control | Green | Primary |
| Pattern adoption/reuse acceleration | Green with qualifying-pattern caveat | Primary |
| Fixed-horizon adoption hardening | Green | Primary or SI |
| Held-out Codex operation | Green | Primary / mechanism support |
| Regional event-stream dynamics | Green with event-stream caveat | Primary or SI |
| KataGo selective alignment | Yellow | Supplementary |
| Figure 0 Lee/Ke vignette | Yellow | Motivating vignette only |
| External references | Green after DOI fix | Submission-ready |
| Data availability / repository | Yellow | Needs final packaging |

---

## 8. Recommendation

Proceed to review stage.

Recommended framing:

> This is no longer an exploratory result pile. It is a coherent empirical
> paper with one central claim, a historical control, a mechanism measure, and
> multiple robustness checks.

Do not add a new phase unless a reviewer specifically asks for it. The next
work unit should be manuscript assembly and reviewer-defense preparation.
