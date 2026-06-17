# Data Policy

Large data files are intentionally not tracked in this repository.

## Expected Local Layout

For full recomputation, place files as follows:

```text
data/
  parsed/
    go_games_parsed.csv
  raw/
    cwi_games.7z
    cwi_extracted/
  katago/
    katago.exe
    analysis.cfg
    model.bin.gz
```

## Data Sources

- CWI Professional Go Archive: https://homepages.cwi.nl/~aeb/go/games/
- KataGo binary and model weights should be obtained from the official KataGo
  release/model channels appropriate for the target platform.

## What Is Tracked

The repository tracks derived aggregate results under `results/`, including
figure data, phase summaries, and small CSV tables needed to inspect the paper's
claims.

## What Is Not Tracked

- raw SGF archive and extracted files
- parsed 330MB `go_games_parsed.csv`
- KataGo binary, DLLs, logs, and model weights
- downloaded archives and compressed model files
