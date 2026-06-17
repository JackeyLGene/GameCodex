# MANUSCRIPT_v4_PNAS Strict Review

**Date:** 2026-06-15  
**Target:** `docs/MANUSCRIPT_v4_PNAS.md`  
**Review mode:** strict pre-review audit.  
**Verdict:** V4 is much closer to manuscript form, but **not yet externally review-ready**. It is internally review-ready after the P0 fixes below.

---

## Executive Verdict

The paper's core scientific claim remains strong:

> AI-era move-structure drift is inside the historical envelope, while pattern circulation speed and reuse increase sharply after external AI oracles enter the Go knowledge system.

V4 improves readability and manuscript structure, but it introduces or preserves several submission-level problems:

1. Figure numbering and generated figure files are inconsistent.
2. Two external references are factually wrong.
3. Figure 0 contains a rank-index error in the opening hook.
4. Some robustness claims are stronger than the available scripts support.
5. The Supplementary/SI package is referenced but not yet present.

Recommended decision:

> Do not send V4 to external reviewers yet. Fix P0 items first; then V4 can enter serious internal review.

---

## P0 Blocking Issues

### P0.1 Figure numbering does not match generated figure files

**Manuscript locations:**  
`MANUSCRIPT_v4_PNAS.md:5`, `MANUSCRIPT_v4_PNAS.md:204`, `MANUSCRIPT_v4_PNAS.md:212`, `MANUSCRIPT_v4_PNAS.md:385-412`

V4 says:

```text
Fig. 3 — Institutional revolution vs. oracle-speed revolution
Fig. 4 — Regional event-stream three-phase distance
Fig. 5 — Pattern adoption lag and reuse density
```

But the generated files are:

```text
fig1_drift_envelope.png
fig2_fixed_horizon_adoption.png
fig3_regional_three_phase.png
fig4_pattern_adoption.png
fig0_paired_vignette.png
```

There is no generated `fig5_*` file, and no generated institutional-overlap figure matching the current `Fig. 3` caption. The current `fig3` file is regional, while V4 uses Fig. 3 for the institutional comparison.

**Risk:** This is an immediate submission-package failure. Reviewers/editors will see mismatched figure calls.

**Required fix:** Choose one of two options:

1. Rename manuscript figure calls to match existing files:
   - Fig. 3 = regional three-phase distance.
   - Fig. 4 = pattern adoption/reuse.
   - Move institutional decomposition to text/table/SI.

2. Generate the missing institutional figure and a true Fig. 5:
   - `fig3_institutional_overlap.png`
   - `fig4_regional_three_phase.png`
   - `fig5_pattern_adoption.png`

Do not proceed until figure filenames, captions, and in-text references match exactly.

---

### P0.2 External references [3] and [4] contain factual errors

**Manuscript locations:**  
`MANUSCRIPT_v4_PNAS.md:364-370`

V4 currently says:

```text
Beheim ... Evolutionary Human Sciences 7:e35. doi:10.1017/ehs.2025.35
Choi S, Kang H, Kim J, Park J ...
```

Verified sources show:

```text
Beheim BA (2025) ... Evolutionary Human Sciences 7:e28.
doi:10.1017/ehs.2025.10016

Choi S, Kang H, Kim N, Kim J (2025) ...
PNAS Nexus 4(5):pgaf138.
doi:10.1093/pnasnexus/pgaf138
```

Notes:

- Cambridge Core lists DOI `10.1017/ehs.2025.10016`.
- PubMed lists Beheim as `Evol Hum Sci. 2025 Aug 26:7:e28`.
- PubMed lists the PNAS Nexus authors as Sukwoong Choi, Hyo Kang, Namil Kim, and Junsik Kim.
- V4 incorrectly changes Namil Kim to `Kim J` and Junsik Kim to `Park J`.

**Risk:** Citation errors signal carelessness and are especially damaging because these are the closest neighboring papers.

**Required fix:** Replace references [3] and [4] with:

```text
3. Beheim BA (2025) Opening strategies in the game of Go from feudalism to
superhuman AI. Evolutionary Human Sciences 7:e28.
doi:10.1017/ehs.2025.10016

4. Choi S, Kang H, Kim N, Kim J (2025) The dual edges of AI: advancing
knowledge while reducing diversity. PNAS Nexus 4(5):pgaf138.
doi:10.1093/pnasnexus/pgaf138
```

Sources checked:

- Cambridge Core: https://www.cambridge.org/core/journals/evolutionary-human-sciences/article/opening-strategies-in-the-game-of-go-from-feudalism-to-superhuman-ai/EB5A1737EC53BD5C642CF4C471668A75
- PubMed Beheim: https://pubmed.ncbi.nlm.nih.gov/41089410/
- PubMed Choi et al.: https://pubmed.ncbi.nlm.nih.gov/40406610/

---

### P0.3 Figure 0 rank statement is wrong under the paper's own indexing

**Manuscript location:**  
`MANUSCRIPT_v4_PNAS.md:65-69`

V4 says:

```text
mean zero-indexed policy rank = 20
The move itself ranked second—within KataGo's top-3 but not its top-1.
```

The figure trace says move 78 has:

```text
policy_rank_zero_indexed = 2
```

If rank is zero-indexed, rank 2 is the third item, not the second. The correct statement is:

```text
The move itself had zero-indexed policy rank 2—within KataGo's top-3 but not its top-1.
```

**Risk:** This is in the opening hook, so it will be noticed. It also makes the paper look confused about its own metric.

**Required fix:** Replace "ranked second" with "had zero-indexed policy rank 2" or "was among KataGo's top-3 recommendations."

---

### P0.4 Supplementary package is referenced but not available

**Manuscript locations:**  
`MANUSCRIPT_v4_PNAS.md:136`, `MANUSCRIPT_v4_PNAS.md:226`, `MANUSCRIPT_v4_PNAS.md:407-412`

V4 repeatedly references SI and supplementary figures:

```text
Full details in SI.
see SI
Fig. S1
Fig. S2
Fig. S3
```

But the repository currently does not contain a supplementary manuscript or generated S1-S3 figure files.

**Risk:** This is not a conceptual problem, but it is a submission completeness failure.

**Required fix:** Create `SUPPLEMENTARY_INFORMATION.md` or equivalent, and either generate the S figures or remove S-figure calls until they exist.

---

## P1 Major Issues

### P1.1 Fixed-horizon adoption result is still conditional; "confirms" is too strong

**Manuscript locations:**  
`MANUSCRIPT_v4_PNAS.md:153-163`, `MANUSCRIPT_v4_PNAS.md:257-259`

V4 says:

```text
Fixed-horizon adoption analysis confirms the acceleration is not solely a right-censoring artifact.
```

This is directionally right but too strong. The fixed-horizon check is still conditional on:

- qualifying recurrent patterns,
- observed first appearance,
- sufficient follow-up for each horizon,
- the same archive/source process.

For the 5-year horizon, the hardening output is:

```text
pre-1980: 79/179 = 0.44
2016+:    58/64  = 0.91
```

The denominator is not all 115 post-2016 qualifying patterns, only the 64 with sufficient 5-year follow-up.

**Required fix:** Replace "confirms" with:

```text
supports the conclusion that the acceleration is not solely a right-censoring artifact
```

and report denominators at least once, either in text or table:

```text
0.44 (79/179) vs 0.91 (58/64)
```

---

### P1.2 Japan-only robustness overclaims operation replication

**Manuscript location:**  
`MANUSCRIPT_v4_PNAS.md:337-339`

V4 says:

```text
Japan-only: all drift and operation analyses replicated on the Japan-only subset.
```

The available script evidence found in this review supports the drift/control result:

```text
Full CWI:   0.0160
Japan-only: 0.0159
```

But I did not find a Japan-only replication of the held-out Codex operation analysis analogous to `phase3_baselines.py`.

**Risk:** A reviewer can ask for the Japan-only operation table and not find it.

**Required fix:** Either:

1. Run and save a Japan-only held-out Codex operation replication, or
2. Change the Methods claim to:

```text
Japan-only: the main drift analysis replicated on the Japan-only subset.
```

---

### P1.3 Figure 0 source trace lacks full provenance for all reported values

**Manuscript locations:**  
`MANUSCRIPT_v4_PNAS.md:65-80`, `MANUSCRIPT_v4_PNAS.md:325-333`, `MANUSCRIPT_v4_PNAS.md:387-390`

The trace file supports:

```text
policy ranks
raw KataGo winrate
winrate perspective
human-perspective winrate
```

But the text also reports:

```text
adj_opp Cohen's d = +0.19
adj_own d = +0.32
dist_last d = +0.55
```

Those effect-size values are not present in `fig0_paired_vignette_trace.csv`, and the current figure script uses hard-coded arrays from prior one-off outputs.

**Risk:** Figure 0 is a hook. If the hook has incomplete provenance, it weakens the paper's trust texture.

**Required fix:** Add a Figure 0 source table containing the rhythm-effect metrics, or move those d-values to SI with their generating script/output.

---

### P1.4 Empirical "95% range [0.000, 0.034]" is not the observed min-max range

**Manuscript locations:**  
`MANUSCRIPT_v4_PNAS.md:23-24`, `MANUSCRIPT_v4_PNAS.md:103-105`

Recomputed from `results/phase05/decade_drift.csv`:

```text
pre-2016 min drift: 0.0038003
pre-2016 max drift: 0.0342417
```

V4 says:

```text
empirical 95% range [0.000, 0.034]
```

That interval may be defensible as a truncated mean ± 1.96 SD envelope, but it is not the empirical min-max range.

**Required fix:** Use one of:

```text
historical envelope [0.0038, 0.0342]
```

or:

```text
mean 0.0146, SD 0.0098; AI-era drift 0.0130, Z = -0.16
```

Avoid calling `[0.000, 0.034]` an empirical range unless the exact procedure is specified.

---

### P1.5 "AI is not the most structurally disruptive event in Go history" needs metric scope

**Manuscript location:**  
`MANUSCRIPT_v4_PNAS.md:109-112`

This sentence is rhetorically strong but too global:

```text
AI is not the most structurally disruptive event in Go history.
```

The supported claim is metric- and archive-specific:

```text
AI is not the largest move-structure drift event in the CWI record under this five-feature rhythm metric.
```

**Risk:** A reviewer can object that "Go history" includes many dimensions not measured here.

**Required fix:** Scope the sentence:

```text
Under this move-level rhythm metric, AI is not the largest structural drift event in the CWI record.
```

---

### P1.6 "Stable chroma-rhythm coupling" should be scoped to post-2000

**Manuscript locations:**  
`MANUSCRIPT_v4_PNAS.md:118-124`

The evidence is:

```text
44,368 post-2000 games
Cohen's d(E0 vs E3) = -0.029
```

The section title says:

```text
Chroma-rhythm coupling remained stable
```

This is fine if scoped to the observed post-2000 period. It should not imply four-century stability.

**Required fix:** Change title or first sentence to:

```text
Chroma-rhythm coupling remained stable in the post-2000 AI-era comparison.
```

---

### P1.7 "200 million people" needs a source or should be removed

**Manuscript location:**  
`MANUSCRIPT_v4_PNAS.md:44-45`

The sentence:

```text
watched by over 200 million people [1,2]
```

is not clearly supported by the AlphaGo Nature papers [1,2]. It may be true from public reporting, but it needs a specific media/statistical source.

**Required fix:** Either add a source for the viewership number or remove the exact number:

```text
In March 2016, AlphaGo defeated Lee Sedol 4-1 in a widely watched five-game match...
```

---

## P2 Minor / Manuscript Hygiene

### P2.1 "The move itself ranked second" also conflicts with zero-index terminology

Covered under P0.3, but worth repeating because it is stylistically prominent. Use one rank convention everywhere.

### P2.2 "Oracle-speed revolution" is strong but acceptable if defined once

The phrase works rhetorically. Define it once in the Introduction or Discussion:

```text
By oracle-speed revolution, we mean an acceleration in discovery, adoption, and reuse, not an increase in move-structure drift.
```

### P2.3 Figure 0 should stay a vignette, not evidence pillar

V4 mostly handles this correctly. Keep it as "motivate the framework" and do not use it to prove the main result.

### P2.4 Table 2 uses event-stream labels correctly

This is good. Preserve `JPN-coded`, `KOR-coded`, `CHN-coded`; do not revert to national style labels.

---

## What Is Strong In V4

The manuscript now has a clean evidence spine:

1. Historical envelope:
   `AI drift = 0.013`, pre-2016 mean `0.0146`, max `1910s->1920s = 0.0342`.

2. Archive control:
   Japan-only drift `0.0159` nearly equals full archive `0.0160`.

3. Adoption/reuse mechanism:
   observed lag `6.3 -> 1.5`, reuse `0.35 -> 0.78`, fixed-horizon support, bootstrap ratios.

4. Codex operation:
   Human Codex exceeds Frequency in `22/22` held-out years.

5. Regional dynamics:
   exact five-feature distance now supports:
   `shock convergence -> diffusion re-divergence -> partial oracle re-convergence`.

This is a real paper. The remaining problems are mostly packaging, citation accuracy, and overclaim control.

---

## Required Pre-Review Checklist

Before sending to external reviewers:

1. Fix references [3] and [4].
2. Fix Figure 0 rank wording.
3. Resolve figure numbering and generate missing figures or rename existing ones.
4. Create SI / supplementary figure package or remove SI references.
5. Add denominators to fixed-horizon adoption result.
6. Scope "not most structurally disruptive" to the CWI rhythm metric.
7. Remove or cite "over 200 million people."
8. Remove unsupported "operation analyses replicated on Japan-only" unless replicated.
9. Add provenance for Figure 0 rhythm-effect d-values.

After these fixes, V4 can enter serious internal review.
