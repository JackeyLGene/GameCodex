# PAPER_DRAFT_PNAS_v2 Audit Report

**Date:** 2026-06-15  
**Target draft:** `docs/PAPER_DRAFT_PNAS_v2.md`  
**Audit status:** second-pass internal review after P0/P1 fixes.  
**Overall verdict:** v2 is much stronger and internally more coherent than v1, but it is not yet PNAS-submission-ready.

---

## 1. Executive Verdict

The v2 draft now has a stable paper core:

> AI did not rewrite the move structure of professional Go; it rewrote the speed at which the Go Codex is discovered, transmitted, and stabilized.

The major v1 contradictions have mostly been repaired. The paper is now suitable for a v3 convergence pass, not for immediate submission. The remaining risks are narrower but important: statistical wording, right-censoring, data/license placeholders, figure readiness, and over-strong robustness claims.

Recommended decision:

> Continue paper convergence. Do not submit to PNAS until the P0 blockers below are resolved.

---

## 2. Scope Of Audit

Reviewed:

- `docs/PAPER_DRAFT_PNAS_v2.md`
- `docs/PAPER_DRAFT_PNAS_AUDIT_2026-06-15.md`
- `results/PHASE05_PHASE4_CONVERGENCE_2026-06-14.md`
- `results/PHASE4E_REGIONAL_RHYTHM_ORACLE_CONVERGENCE_2026-06-14.md`
- `results/phase4/archive_composition_by_decade.csv`
- `results/phase4/pattern_metrics.csv`
- `scripts/phase2_full.py`
- `scripts/phase4d_pattern_adoption.py`
- `scripts/phase4e_regional_history.py`
- `scripts/phase5_defense.py`

Also ran:

```powershell
python G:\GEME\EE\game_codex\scripts\phase5_defense.py
```

The defense script completed and confirmed the main repair direction, but exposed several remaining issues listed below.

---

## 3. Status Versus Previous Audit

| Previous item | v2 status | Audit note |
|---|---:|---|
| P0.1 contradictory drift numbers | Fixed | AI drift now consistently 0.013; 1910s->1920s now 0.034. |
| P0.2 unit confusion in archive table | Mostly fixed | Table now uses true game counts, but Total includes INTL/unknown columns that are not shown. |
| P0.3 regional/national labels | Mostly fixed | Main text uses event-stream labels, but figure/SI/player-control wording still risks nationality interpretation. |
| P0.4 right-censoring in adoption lag | Partially fixed | Caveat added, but no censoring-safe analysis yet. |
| P1.1 KataGo method details | Fixed | Exact model, sample design, visits, rules, and komi are now stated. |
| P1.2 KataGo weight in main argument | Fixed | Moved to supplementary/secondary role. |
| P1.3 coupling statistic missing | Partially fixed | Cross-harm result added, but axis-shift wording needs numeric support. |
| P1.5 "lock-in" overclaim | Fixed | Replaced with reuse density / persistence language. |
| P1.6 "professional games" scope | Fixed | Now says recorded CWI games. |
| P1.7 citations | Partially fixed | Core citations added, but placeholders remain. |

---

## 4. P0 Submission Blockers

### P0.1 "95% CI" is still statistically unsafe

**Draft locations:** `PAPER_DRAFT_PNAS_v2.md:26`, `PAPER_DRAFT_PNAS_v2.md:73`, `PAPER_DRAFT_PNAS_v2.md:238-241`

The draft says:

```text
mean 0.015 +/- 0.010, 95% CI
95% CI (pre-2016): [0.000, 0.034]
```

But the Methods describe this as a pre-2016 decade-pair drift envelope/range, not an inferential confidence interval. A confidence interval estimates uncertainty around a population parameter; this appears to be a historical distribution or envelope.

**Risk:** Reviewers will treat this as statistical imprecision in the central result.

**Required fix:** Replace "95% CI" with one of:

```text
pre-2016 historical envelope
empirical pre-2016 range
mean +/- SD across pre-2016 decade transitions
empirical 95% interval
```

Use "confidence interval" only if a bootstrap or model-based estimator is actually computed and reported.

---

### P0.2 Data availability and references remain placeholders

**Draft locations:** `PAPER_DRAFT_PNAS_v2.md:47`, `PAPER_DRAFT_PNAS_v2.md:224-227`, `PAPER_DRAFT_PNAS_v2.md:270-274`, `PAPER_DRAFT_PNAS_v2.md:287`

Remaining placeholders:

```text
[refs]
[ref]
[repository URL]
[PNAS Nexus 2025 paper ... to be added]
```

The Data Availability section also states that parsed data, scripts, and result tables are available "under CC-BY 4.0." That license statement should not be made until the CWI source-data license and the intended repository license are verified. Scripts can be licensed by the author; redistributed parsed SGF-derived data may require more careful wording.

**Risk:** This is an external-submission blocker. PNAS reviewers and editors will expect precise citations and a credible data-availability statement.

**Required fix:**

1. Replace all placeholders with final references, DOIs/URLs, and repository links.
2. Separate source data from derived aggregate results.
3. Avoid claiming CC-BY for CWI-derived parsed records unless the licensing basis is confirmed.

Recommended wording until licensing is settled:

> Analysis scripts and derived aggregate result tables will be released at [repository]. Source SGF records are available from the CWI Professional Go Archive subject to the archive's terms.

---

### P0.3 Adoption acceleration is caveated but not censoring-safe

**Draft locations:** `PAPER_DRAFT_PNAS_v2.md:29-31`, `PAPER_DRAFT_PNAS_v2.md:117-122`, `PAPER_DRAFT_PNAS_v2.md:211-216`

v2 correctly adds:

```text
observed adoption lag among qualifying recurrent patterns
```

and explicitly notes shorter post-2016 follow-up. That is a major improvement. However, the Abstract still presents the 6.3 -> 1.5 year result as a headline mechanism without the censoring qualification.

The current metric remains conditional on:

- patterns satisfying the recurrent-pattern filter,
- patterns surviving long enough to be observed,
- shorter post-2016 follow-up,
- adoption being measured after the event has already entered the qualifying set.

**Risk:** A reviewer can argue that the 4.2x speedup is partly a right-censoring and selection effect.

**Required fix:** Either add a censoring-safe analysis or move the caveat into the abstract and soften the mechanism claim.

Best next analyses:

1. Fixed-horizon adoption: probability of reaching >=3 unique players within 1, 2, 3, and 5 years after first appearance.
2. Kaplan-Meier or Cox model with not-yet-adopted patterns treated as censored.
3. Reuse density measured over a fixed post-first-seen window.

Until then, the safest wording is:

> Among qualifying recurrent opening patterns, observed adoption lag shortened from 6.3 to 1.5 years, subject to right-censoring in the post-2016 window.

---

## 5. P1 Major Issues

### P1.1 Prefix-length robustness is overstated

**Draft locations:** `PAPER_DRAFT_PNAS_v2.md:127-129`, `PAPER_DRAFT_PNAS_v2.md:265-266`

The draft says adoption acceleration is robust at prefix lengths 10, 15, and 20. The defense script shows:

```text
Prefix 10: pre-1980 9.0 yr -> 2016+ 1.3 yr
Prefix 15: pre-1980 6.3 yr -> 2016+ 1.5 yr
Prefix 20: pre-1980 4.1 yr -> 2016+ 1.4 yr
```

This supports long-term acceleration. However, prefix 20 does not support an additional post-2016 acceleration relative to 2000-2015:

```text
Prefix 20: 2000-2015 1.4 yr; 2016+ 1.4 yr
```

**Risk:** "Robust to prefix length" is too broad if the specific AI-era increment is central.

**Required fix:** Replace with:

> Long-term adoption acceleration is robust to prefix length. The additional post-2016 reduction is strongest for prefix lengths 10 and 15, but not detectable at prefix length 20, where 2000-2015 and 2016+ both show 1.4-year observed lag.

---

### P1.2 Archive composition table omits INTL/unknown columns

**Draft locations:** `PAPER_DRAFT_PNAS_v2.md:136-141`

The table shows JPN/KOR/CHN/Total, but Total includes INTL and unknown games:

```text
1950s: JPN 1,668 + KOR 0 + CHN 0 != Total 1,868
1980s: JPN 9,640 + KOR 1 + CHN 0 != Total 9,747
```

**Risk:** The table appears internally inconsistent unless readers know that omitted categories are included in Total.

**Required fix:** Either add INTL and unknown columns, or add a table note:

> Total includes INTL and unknown event-stream classifications not shown in the three main regional columns.

---

### P1.3 Regional event-stream labels are improved, but S3/player-control wording remains risky

**Draft locations:** `PAPER_DRAFT_PNAS_v2.md:165-186`, `PAPER_DRAFT_PNAS_v2.md:267-268`, `PAPER_DRAFT_PNAS_v2.md:309`

The main regional section now correctly says event-stream labels are tournament/archive provenance, not player nationality. However, the Methods and figure list still say:

```text
Leave-one-out player control
Player-level decomposition of Korea-coded stream
```

The defense script's "Top 10 Korean players" list includes non-Korean-nationality players such as Ke Jie, Yang Dingxin, Nakamura Sumire, and Cho Chikun. That is not a bug in the event-stream analysis, but it means this cannot be framed as Korean-nationality style or player-nationality decomposition.

**Risk:** The regional result can be attacked if any wording invites a nationality interpretation.

**Required fix:** Rename S3 and the robustness claim:

```text
Event-stream top-player leave-one-out control
```

Do not call it a player-level nationality decomposition unless external nationality metadata is added.

---

### P1.4 Figures are marked "ready" but no generated figure files are present

**Draft locations:** `PAPER_DRAFT_PNAS_v2.md:298-309`

The figure table marks all main and supplementary figures as ready. A repository scan found no generated figure files outside raw extracted image data.

**Risk:** This is not a scientific contradiction, but it is a workflow/submission-readiness mismatch.

**Required fix:** Change status from "ready" to "data ready" or "planned" until figure files exist. Before external circulation, generate:

- Figure 1: encoding schematic + archive composition timeline.
- Figure 2: drift envelope with AI era marked.
- Figure 3: 1910s->1920s overlap-player decomposition.
- Figure 4: adoption lag and reuse density by era.
- Figure 5: regional event-stream three-phase distance.

---

### P1.5 Coupling/operating-point claim needs one more numeric anchor

**Draft locations:** `PAPER_DRAFT_PNAS_v2.md:87-91`

v2 adds the key cross-harm statistic:

```text
d(E0 vs E3) = -0.029
```

This fixes the largest v1 gap. But the sentence says:

```text
both the game-phase and spatial-relation axes shifted, but their interaction did not
```

The paper provides rhythm-axis evidence, but it does not give a chroma-axis effect size in the same section.

**Risk:** Reviewers may ask where the game-phase-axis shift is quantified.

**Required fix:** Add one sentence with the actual chroma-axis effect sizes, or soften to:

> rhythm features shifted within a stable observed chroma-rhythm coupling structure.

---

### P1.6 Regional "independent replication" should be softened unless a formal joint test is added

**Draft locations:** `PAPER_DRAFT_PNAS_v2.md:182-186`

The regional three-phase sequence is very valuable. But "independently replicates" is stronger than the current evidence unless the paper reports a formal test comparing the regional-distance trajectory to the held-out Codex-operation trajectory.

Similarly, "pulled them toward the global mean" should be more precise, because the labels are event streams within the CWI archive.

**Required fix:** Replace with:

> This three-phase pattern is consistent with the held-out Codex-operation trajectory...

and:

> pulled them toward the full-archive event-stream centroid

or:

> toward the CWI network mean

---

### P1.7 "All factual claims verified" is too strong

**Draft locations:** `PAPER_DRAFT_PNAS_v2.md:313-315`

The closing note says:

```text
All factual claims have been verified against the source scripts and data.
...
P0 issues resolved.
```

Given the open issues above, this should not remain in the draft.

**Required fix:** Remove the closing certification note or replace it with:

> v2 incorporates the first audit's major repairs; remaining submission checks are tracked separately.

---

## 6. P2 Style And Submission Hygiene

### P2.1 "consistent-with" typo

**Draft location:** `PAPER_DRAFT_PNAS_v2.md:99-100`

Replace:

```text
consistent-with the main findings
```

with:

```text
consistent with the main findings
```

---

### P2.2 KataGo feature list omits one aligned feature

**Draft locations:** `PAPER_DRAFT_PNAS_v2.md:97-99`

Earlier Phase 2 results identified three aligned dimensions:

```text
adj_opp, adj_own, dens_delta
```

The v2 text lists only:

```text
adj_opp, dens_delta
```

This is not fatal, but the supplement should either include all three or explain why `adj_own` is omitted.

---

### P2.3 Data span wording should mention sparse earlier records or filtering

**Draft locations:** `PAPER_DRAFT_PNAS_v2.md:21-23`, `PAPER_DRAFT_PNAS_v2.md:224`

The archive composition file contains sparse records before 1600. If the analysis filters to 1600-2026, state that explicitly. If not, revise the phrase to:

> mostly spanning 1600-2026, with sparse earlier records excluded from the main century-scale analysis

or equivalent.

---

### P2.4 "Structural grammar" needs an operational definition before the Abstract ends

The term is central and attractive, but reviewers may read it as philosophical unless operationalized early. Add a compact definition in the Introduction or first Results paragraph:

> Here, structural grammar refers to stable constraints linking game phase and spatial move-choice features, operationalized by chroma-rhythm coupling and rhythm-centroid drift.

---

## 7. Recommended v3 Checklist

Minimum v3 repairs:

1. Replace all "95% CI" language with "historical envelope" or compute a real interval.
2. Move the adoption-lag censoring caveat into the Abstract.
3. Run a fixed-horizon or survival-style adoption analysis if the adoption-speed claim remains central.
4. Revise prefix-length robustness: long-term acceleration is robust; post-2016 increment is not robust at prefix 20.
5. Add INTL/unknown columns or a table note to the archive composition table.
6. Rename S3/player-control language as event-stream top-player leave-one-out control.
7. Replace "independently replicates" with "is consistent with" unless a formal joint test is added.
8. Replace `[refs]`, `[ref]`, `[repository URL]`, and placeholder reference [4].
9. Fix Data Availability and avoid unsupported CC-BY claims for CWI-derived parsed data.
10. Generate figure files or mark all figures as "planned/data ready."
11. Remove the closing "all factual claims verified" note.

Optional but high-value analyses before external review:

1. Bootstrap the exact five-feature regional-distance metric used in Figure 5.
2. Bootstrap adoption-lag and reuse-density ratios by per-pattern resampling.
3. Add a horizon-controlled adoption table for 1-, 2-, 3-, and 5-year adoption.
4. Add a small chroma-axis effect-size table to support the operating-point language.

---

## 8. Final Assessment

v2 successfully repairs the main narrative instability of v1. The paper is no longer overclaiming "AI rewrote Go"; it now has the stronger and more original claim that AI accelerated Codex circulation inside a historically continuous structural space.

The remaining work is not conceptual rescue. It is submission hardening:

- make statistical language exact,
- make adoption-speed inference censoring-aware,
- make regional labels impossible to misread,
- replace placeholders,
- generate figures.

Current recommendation:

> Proceed to v3. The paper is promising, but not yet ready for PNAS submission.
