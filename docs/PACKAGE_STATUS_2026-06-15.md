# GameCodex Package Status

**Date:** 2026-06-15  
**Status:** repository entry prepared; technical-note package cleaned for external circulation review.

## Current Entry

- Root entry: [`../README.md`](../README.md)
- Current technical note: [`TECHNICAL_NOTE.md`](TECHNICAL_NOTE.md)
- Document map: [`INDEX.md`](INDEX.md)
- Reproduction notes: [`../REPRODUCE.md`](../REPRODUCE.md)
- Data policy: [`../data/README.md`](../data/README.md)

## Closed For Current V8 Package

- Current technical note exists as `TECHNICAL_NOTE.md`.
- Technical-note status/footer now identifies V8.
- Historical range wording is unified as observed range `[0.004, 0.034]`.
- Unsupported Fig. 0 rhythm effect-size claims were removed from the main text.
- Fig. 0 caption no longer cites nonexistent scripts.
- Fig. 5 is generated as `fig5_pattern_adoption.png`.
- Fig. 3 and Fig. 5 visual layout issues were adjusted.
- Root README now points to the current technical note, results, figures, and reproduction notes.
- Older drafts and audits were moved to `docs/archive/`.
- Research dialogue/planning notes were moved to `docs/notes/`.

## Remaining Boundaries

- Full phase scripts still expect local large data files; many defaults now point to `G:/GameCodex` but are not fully repo-relative.
- SI plotting scripts use audited aggregate constants rather than reading all source values from machine-readable result tables.
- Raw CWI data, parsed 330MB CSV, KataGo binaries, and model weights are not tracked.
- `git` was not available in the active shell, so no stage/commit was performed.

## Recommended Next Step

Before external circulation, do one dedicated reproducibility pass:

1. Convert all phase scripts to repo-relative paths or command-line arguments.
2. Add source CSVs for SI plotting constants.
3. Re-run full pipeline from `data/parsed/go_games_parsed.csv`.
4. Commit the cleaned package once `git` is available.
