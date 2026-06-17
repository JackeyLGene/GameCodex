# MANUSCRIPT V6 PNAS Review

**Date:** 2026-06-15  
**Reviewed file:** `docs/MANUSCRIPT_v5_PNAS.md`  
**Note:** No separate `MANUSCRIPT_v6_PNAS.md` file was found. The updated `MANUSCRIPT_v5_PNAS.md` and newly generated figure files were treated as the V6 content.  
**Verdict:** V6 is close to a pre-submission draft, but not package-frozen yet.

---

## Executive Verdict

V6 resolves most of the V5 package blockers:

- `fig5_pattern_adoption.png` now exists.
- `figS1_katago_alignment.png`, `figS2_prefix_robustness.png`, and `figS3_player_control.png` now exist.
- The viewership claim has been softened from "over 200 million people" to "watched by a global audience."
- The broad "AI is not the most structurally disruptive event in Go history" claim has been narrowed to "By this structural metric... in the CWI record."
- The abstract now uses a more accurate historical range `[0.004, 0.034]`.

The paper's core scientific claim remains sound:

> The AI era did not produce the largest observed move-structure drift in the CWI record, but it sharply accelerated opening-pattern adoption and reuse.

However, V6 still has several package-level and reproducibility issues. These do not undermine the core result, but they should be fixed before external circulation.

---

## Status Against V5 Issues

| V5 issue | V6 status | Assessment |
|---|---:|---|
| Fig. 5 missing | Mostly fixed | File exists, but generation script still writes `fig4_pattern_adoption.png`. |
| SI figures missing | Fixed as files | S1-S3 PNGs exist, but generation is hard-coded rather than data-driven. |
| Empirical range wording | Partly fixed | Abstract fixed to `[0.004, 0.034]`; Results section still says `[0.000, 0.034]`. |
| Fig. 0 rhythm-effect provenance | Not fixed | Caption names nonexistent scripts. |
| Overbroad disruption sentence | Fixed | Now scoped to this structural metric and CWI record. |
| 200 million viewership claim | Fixed | Number removed. |

---

## P0 Blocking Issues

### P0.1 The file/version identity is inconsistent

**Location:**  
`MANUSCRIPT_v5_PNAS.md:4`, `MANUSCRIPT_v5_PNAS.md:471`

The user-facing version is V6, but the file and status still say V5:

```text
**Status:** v5 — P0/review fixes applied. 2026-06-15.
...
Internal review version. v5.
```

**Risk:** This sounds minor, but it matters for review control. A manuscript under active review needs an unambiguous filename/version identity.

**Required fix:** Save the current file as:

```text
docs/MANUSCRIPT_v6_PNAS.md
```

and update status/footer to V6.

---

### P0.2 Abstract and Results disagree on the historical range

**Locations:**  
`MANUSCRIPT_v5_PNAS.md:27`, `MANUSCRIPT_v5_PNAS.md:107-109`

Abstract:

```text
empirical 95% range [0.004, 0.034]
```

Results:

```text
The empirical 95% range is [0.000, 0.034].
```

The data support:

```text
observed pre-2016 range: 0.003800–0.034242
mean: 0.014578
sd: 0.009771
AI-era drift: 0.013046
```

**Required fix:** Use the same wording in both places. Recommended:

```text
observed historical range [0.0038, 0.0342]
```

or rounded:

```text
observed historical range [0.004, 0.034]
```

Avoid "empirical 95% range" unless the interval construction is explicitly defined.

---

### P0.3 Fig. 0 provenance now cites nonexistent scripts

**Location:**  
`MANUSCRIPT_v5_PNAS.md:397`

Current caption says:

```text
Rhythm effect sizes quoted in §1.1 were computed by `divine_move.py` and `kejie_alphago.py`
```

But neither file exists in the repository:

```text
divine_move.py       missing
kejie_alphago.py     missing
```

The existing script is:

```text
scripts/gen_paired_vignette.py
```

but that script only hard-codes/outputs rank and winrate trace values; it does not compute the reported rhythm effect sizes:

```text
adj_opp d = +0.19
adj_own d = +0.32
dist_last d = +0.55
```

**Required fix:** Either:

1. Add the missing scripts and output a source table, e.g.

```text
results/figures/fig0_rhythm_effects.csv
```

or:

2. Remove these three rhythm effect sizes from the main text and keep Fig. 0 as a rank/winrate vignette.

This is the most important remaining provenance issue.

---

## P1 Major Issues

### P1.1 Fig. 5 exists, but the generation script is still stale

**Locations:**  
`results/figures/fig5_pattern_adoption.png`  
`scripts/generate_figures.py:1-8`, `scripts/generate_figures.py:165`

The file now exists, but:

- `fig4_pattern_adoption.png` and `fig5_pattern_adoption.png` are byte-identical.
- `scripts/generate_figures.py` still documents and saves the pattern figure as Fig. 4.
- Re-running the figure-generation script would not regenerate `fig5_pattern_adoption.png`.

**Required fix:** Update `generate_figures.py` so the pattern adoption figure is generated directly as:

```text
fig5_pattern_adoption.png
```

and update comments/print labels accordingly.

---

### P1.2 SI figures are generated from hard-coded arrays

**Location:**  
`scripts/gen_si_figures.py`

The new SI figures are useful, but the values are hard-coded:

```text
d_e0 = [-0.220, -0.209, +0.216, -0.240, +0.061]
d_e3 = [-0.016, +0.007, -0.043, -0.444, -0.337]
prefix10 = [9.0, 8.0, 3.0, 1.3]
...
fis = [+0.0341, +0.0337, ...]
```

This is acceptable for a draft figure, but not ideal for a reproducible package.

**Recommended fix:** Either:

- make `gen_si_figures.py` read saved CSV/TSV result tables, or
- explicitly label it as a plotting script that consumes already audited aggregate constants, with those constants stored in a machine-readable table.

---

### P1.3 Main figures still need visual polish

Rendered PNG inspection shows two lingering issues:

- `fig3_1910s_decomposition.png`: the "85% of drift from same players" annotation is partially obscured.
- `fig5_pattern_adoption.png`: the "6.3 yr" label sits against the top boundary.

These do not damage the science, but they should not survive into a polished PNAS package.

---

### P1.4 "Confirms" is still a bit strong for fixed-horizon adoption

**Locations:**  
`MANUSCRIPT_v5_PNAS.md:162`, `MANUSCRIPT_v5_PNAS.md:261-262`

Current wording:

```text
Fixed-horizon adoption analysis confirms the acceleration is not solely a right-censoring artifact...
```

Given that the pattern set is still filtered by recurrence and the post-2016 follow-up is shorter, "supports" remains safer:

```text
Fixed-horizon adoption analysis supports the conclusion that the acceleration is not solely a right-censoring artifact...
```

This is a wording-risk issue, not a result-risk issue.

---

## P2 Minor Issues

### P2.1 Fig. 3 Panel B should clarify asymmetric measurements

Fig. 3 compares two revolutions, but the adoption acceleration ratio is only meaningful for the AI-era pattern analysis. The caption should explicitly say this, so readers do not infer a symmetric 1910s adoption-speed measure.

### P2.2 Data availability remains placeholder-like

**Location:**  
`MANUSCRIPT_v5_PNAS.md:351-357`

This is fine for internal drafting, but before submission the manuscript needs a clean review bundle:

- exact manuscript version,
- exact figure-generation scripts,
- derived aggregate CSVs,
- SI source tables,
- run order,
- CWI access note.

---

## Strong Points in V6

### The main empirical spine is now stable

The following claims are well supported by existing result files:

```text
AI-era drift = 0.013046
pre-2016 mean drift = 0.014578
largest drift = 1910s->1920s = 0.034242
Japan-only drift = 0.0159 vs full archive = 0.0160
adoption lag = 6.3 yr -> 1.5 yr
reuse density = 0.35 -> 0.78
fixed-horizon <=5yr adoption = 0.44 -> 0.91
regional distances reproduce the shock/diffusion/oracle three-phase pattern
```

### The rhetoric is much safer than V4/V5

The manuscript no longer depends on a strong "AI rewrote Go" claim. It now distinguishes:

- structural drift,
- circulation speed,
- archive composition,
- regional event-stream response,
- retrospective AI policy alignment.

That is the right shape for the paper.

### The "global audience" replacement is good

Removing the unsourced "over 200 million" number was the right move.

---

## Recommended Decision

V6 is not merely a nicer draft; it is close to a real pre-submission manuscript. I would classify it as:

```text
Scientific core:       ready for serious internal review
Submission package:    not yet frozen
External circulation:  after P0 fixes
```

Minimum V6.1 checklist:

1. Rename/save the manuscript as `MANUSCRIPT_v6_PNAS.md`.
2. Fix `[0.000, 0.034]` in Results to match the abstract/data.
3. Remove or substantiate the Fig. 0 rhythm effect sizes.
4. Update `generate_figures.py` so Fig. 5 is generated as Fig. 5.
5. Polish Fig. 3 and Fig. 5 visual layout.
6. Decide whether SI plotting scripts must be data-driven before external review.

---

## Bottom Line

The paper's main argument has survived the hardening process. The remaining problems are no longer conceptual failures; they are version-control, provenance, and figure-package problems.

That is a very good sign. V6 is the first version that feels like it is being cleaned for reviewers rather than still discovering what it wants to be.
