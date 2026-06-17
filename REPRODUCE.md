# Reproduction Notes

This repository contains the current manuscript, derived aggregate results, and
figure-generation scripts. It does not track large raw CWI files, the parsed
330MB game table, KataGo binaries, or model weights.

## Environment

Python 3.10+ is sufficient for the figure scripts.

```powershell
cd G:\GameCodex
python -m pip install -r requirements.txt
```

## Regenerate Manuscript Figures

These commands regenerate the current figure package from constants and derived
tables already present in the repository:

```powershell
cd G:\GameCodex
python scripts\generate_figures.py
python scripts\gen_fig3_1910s.py
python scripts\gen_paired_vignette.py
python scripts\gen_si_figures.py
```

Expected outputs:

```text
results/figures/fig0_paired_vignette.png
results/figures/fig0_paired_vignette_trace.csv
results/figures/fig1_drift_envelope.png
results/figures/fig2_fixed_horizon_adoption.png
results/figures/fig3_1910s_decomposition.png
results/figures/fig4_regional_three_phase.png
results/figures/fig5_pattern_adoption.png
results/figures/figS1_katago_alignment.png
results/figures/figS2_prefix_robustness.png
results/figures/figS3_player_control.png
```

## Full Analysis Pipeline

Full recomputation requires the parsed CWI game table:

```text
data/parsed/go_games_parsed.csv
```

and, for KataGo-related analyses:

```text
data/katago/katago.exe
data/katago/analysis.cfg
data/katago/model.bin.gz
```

See [`data/README.md`](data/README.md) for placement details.

## Current Caveat

The phase analysis scripts were originally run in a working directory with local
large data files. Their default paths have been updated for `G:/GameCodex`, but
some deeper full-pipeline scripts are not yet fully repo-relative. The
manuscript figures and entry-point scripts have been made repository-relative;
deeper full-pipeline cleanup should be done before public release.
