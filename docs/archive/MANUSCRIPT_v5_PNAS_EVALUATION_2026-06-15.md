# MANUSCRIPT_v5_PNAS Evaluation

**Date:** 2026-06-15  
**Target:** `docs/MANUSCRIPT_v5_PNAS.md`  
**Mode:** strict post-v4-fix audit  
**Verdict:** V5 is scientifically much stronger than V4. The core claim is now reviewable, but the submission package is not sealed yet.

---

## Executive Verdict

V5 closes the most important V4 scientific-risk items:

- References [3] and [4] are now factually corrected.
- Fig. 0 rank language is fixed: zero-indexed rank 2 is correctly described as third-ranked / top-3, not second.
- Japan-only robustness is narrowed to decade drift replication.
- KataGo is correctly scoped as supplementary / case-study evidence.
- The main claim is now appropriately centered on circulation speed rather than structural rupture.

The central empirical story remains intact:

> AI-era rhythm drift is inside the historical envelope, while opening-pattern adoption and reuse accelerate sharply after external AI oracles enter the Go knowledge system.

However, V5 still has several package-level blockers and a few wording/statistical precision problems. I would not send this version to external reviewers yet. After the P0 items below are fixed, it can enter serious final internal review.

---

## Status Against V4 P0 Items

| V4 issue | V5 status | Assessment |
|---|---:|---|
| Figure numbering mismatch | Partly fixed | Fig. 3 and Fig. 4 are now realigned, but Fig. 5 still points to `fig4_pattern_adoption.png`. |
| Wrong references [3]/[4] | Fixed | Beheim and Choi et al. now match external bibliographic records. |
| Fig. 0 zero-index rank error | Fixed | Text now says third-ranked / zero-indexed rank 2. |
| SI absent | Partly fixed | SI text exists, but S1-S3 figures/files do not. |
| Japan-only overclaim | Fixed | Now limited to decade drift replication. |

---

## P0 Blocking Issues

### P0.1 Fig. 5 still has no matching generated file

**Manuscript locations:**  
`MANUSCRIPT_v5_PNAS.md:5`, `MANUSCRIPT_v5_PNAS.md:416-418`

V5 declares Figs. 1-5 as main figures, and the figure list defines:

```text
Fig. 5 - Pattern adoption lag and reuse density by era of first appearance.
File: results/figures/fig4_pattern_adoption.png
```

But the generated file is still named:

```text
results/figures/fig4_pattern_adoption.png
```

There is no:

```text
results/figures/fig5_pattern_adoption.png
```

**Risk:** This is a submission-package mismatch. It is easy to fix, but it should not survive into a review bundle.

**Required fix:** Rename/regenerate the file as `fig5_pattern_adoption.png`, update `scripts/generate_figures.py`, and remove or archive stale duplicate figure files if needed.

---

### P0.2 SI figures S1-S3 are referenced but not generated

**Manuscript locations:**  
`MANUSCRIPT_v5_PNAS.md:140`, `MANUSCRIPT_v5_PNAS.md:173`, `MANUSCRIPT_v5_PNAS.md:231`, `MANUSCRIPT_v5_PNAS.md:423-463`

V5 now includes a Supplementary Information section, which is good. But no generated files matching Fig. S1, Fig. S2, or Fig. S3 exist in `results/figures`.

Referenced but absent:

```text
Fig. S1 - KataGo feature-level human-KataGo rhythm gap by era
Fig. S2 - Adoption lag by era for prefix lengths 10, 15, and 20
Fig. S3 - Korea-coded stream fighting index under per-player removal
```

**Risk:** The SI is no longer absent conceptually, but it is not yet a reproducible supplement package.

**Required fix:** Either generate actual `figS1_*`, `figS2_*`, and `figS3_*` files, or rewrite the SI as text/table-only and remove figure labels.

---

## P1 Major Issues

### P1.1 "Empirical 95% range [0.000, 0.034]" is still mislabeled

**Manuscript locations:**  
`MANUSCRIPT_v5_PNAS.md:27`, `MANUSCRIPT_v5_PNAS.md:107-109`

Recomputing from `results/phase05/decade_drift.csv` gives:

```text
pre-2016 observed drift min = 0.003800
pre-2016 observed drift max = 0.034242
mean = 0.014578
sd = 0.009771
AI-era drift = 0.013046
```

So `[0.000, 0.034]` is not the empirical observed range. It looks like a truncated parametric interval or rounded envelope.

**Required fix:** Use one of:

```text
observed historical range [0.0038, 0.0342]
```

or:

```text
mean 0.0146; SD 0.0098; AI-era Z = -0.16
```

Do not call `[0.000, 0.034]` an empirical 95% range unless the construction is defined.

---

### P1.2 The "most structurally disruptive event in Go history" sentence remains too global

**Manuscript location:**  
`MANUSCRIPT_v5_PNAS.md:116`

Current wording:

```text
AI is not the most structurally disruptive event in Go history.
```

This is too broad. The evidence supports a scoped claim:

```text
Under this five-feature rhythm-drift metric in the CWI record, the AI-era transition is not the largest structural drift observed.
```

The narrower version is stronger because it is exactly what was measured.

---

### P1.3 Fixed-horizon adoption wording is still slightly too strong

**Manuscript locations:**  
`MANUSCRIPT_v5_PNAS.md:161-164`

Current wording:

```text
Fixed-horizon adoption analysis confirms the acceleration is not solely a right-censoring artifact...
```

The denominators are now good and should be reported:

```text
pre-1980: 79/179 = 0.44
2016+:    58/64  = 0.91
```

But "confirms" is stronger than warranted because censoring and qualification filters remain nontrivial.

**Recommended wording:**

```text
Fixed-horizon adoption analysis supports the conclusion that the acceleration is not solely a right-censoring artifact...
```

---

### P1.4 Fig. 0 rhythm effect sizes remain under-proven in the file package

**Manuscript locations:**  
`MANUSCRIPT_v5_PNAS.md:75-77`

V5 reports:

```text
adj_opp Cohen's d = +0.19
adj_own d = +0.32
dist_last d = +0.55
```

But `results/figures/fig0_paired_vignette_trace.csv` only supports policy ranks and winrates. I could not find a named output table containing these three rhythm-effect values.

**Required fix:** Add a small source table, for example:

```text
results/figures/fig0_rhythm_effects.csv
```

or remove those effect sizes from the main text and leave the case-study hook to ranks/winrates only.

---

### P1.5 Main figure visual QA still needs one pass

Observed from rendered PNGs:

- `fig3_1910s_decomposition.png`: the annotation "85% of drift from same players" is partially obscured by the bars/layout.
- `fig4_pattern_adoption.png`: the "6.3 yr" label is pressed against or clipped by the top of the panel.

These are not scientific defects, but they matter for a PNAS-facing figure set.

---

### P1.6 The "over 200 million people" viewership claim needs a source

**Manuscript location:**  
`MANUSCRIPT_v5_PNAS.md:47-48`

Current citation points to AlphaGo technical papers [1,2], which do not appear to be viewership sources. Either add a direct source for the viewership figure or remove the number.

Safer wording:

```text
In March 2016, AlphaGo defeated Lee Sedol 4-1 in a globally watched five-game match...
```

---

## P2 Minor Issues

### P2.1 Fig. 3 Panel B should clarify asymmetric quantities

`fig3_1910s_decomposition.png` compares structural drift for both revolutions, but adoption acceleration is only shown for the AI-era case. This is acceptable as an interpretive figure, but the caption should state that adoption-speed ratio is measured for the AI-era pattern analysis and is not a symmetric 1910s metric.

### P2.2 Data availability is still placeholder-like

**Manuscript locations:**  
`MANUSCRIPT_v5_PNAS.md:350-356`

For final review, the paper needs a clean public or private-review repository bundle:

- scripts
- derived aggregate tables
- generated figures
- SI source tables
- exact run order

This is not a V5 scientific blocker, but it is a submission-readiness item.

---

## Core Claims That Now Look Solid

### Historical envelope

Supported. Recalculation from `decade_drift.csv` reproduces:

```text
AI-era drift = 0.013046
pre-2016 mean = 0.014578
pre-2016 sd = 0.009771
largest drift = 1910s->1920s = 0.034242
```

The conclusion "AI-era drift is inside the historical envelope" is robust.

### Archive-composition control

Supported at the drift level. Existing results report:

```text
Full CWI:   0.0160
Japan-only: 0.0159
```

V5 correctly limits this to drift replication.

### 1910s decomposition

Supported, with figure polish needed:

```text
Full drift = 0.0342
Overlap-player drift = 0.0291
Overlap accounts for about 85% of full drift magnitude
```

This supports the interpretation that the 1910s->1920s signal is not merely roster turnover.

### Pattern adoption and reuse

Supported by `PHASE5_HARDENING_2026-06-15.txt`:

```text
Observed lag: 6.3 yr -> 1.5 yr
Reuse density: 0.35 -> 0.78
Lag ratio: 4.2x [2.9x, 5.9x]
Reuse ratio: 2.3x [2.1x, 2.5x]
Fixed horizon <=5 yr: 0.44 -> 0.91
```

This is the strongest positive result in the manuscript.

### Regional three-phase dynamics

Supported, but interpret cautiously because CIs overlap and event-stream categories are provenance labels:

```text
Pre-AI:    0.0144 [0.0109, 0.0361]
Shock:     0.0066 [0.0037, 0.0151]
Diffusion: 0.0167 [0.0109, 0.0323]
Oracle:    0.0102 [0.0056, 0.0212]
```

V5 correctly uses "event-stream" language rather than national-style claims.

---

## Recommended Decision

V5 is a major improvement. The scientific manuscript is now coherent enough to justify continued paper development.

Recommended next step:

1. Fix Fig. 5 filename/package mismatch.
2. Generate or remove S1-S3 supplementary figures.
3. Correct the empirical-range wording.
4. Add provenance for Fig. 0 rhythm effect sizes or delete them.
5. Polish Fig. 3 and Fig. 5 layouts.
6. Replace or source the 200-million-viewer sentence.

After those changes, the paper can move from "internal working draft" to "serious pre-submission draft."

---

## Bottom Line

V4 had submission-level conceptual fragility. V5 mostly removes that fragility. What remains is not a collapse of the argument; it is the ordinary, slightly tedious but essential work of making the manuscript auditable.

The paper is no longer just interesting. It is becoming real.
