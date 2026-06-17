# Fingerprints on the World Cup

Standalone SHP football prototype for post-tournament structural reading:

`index.html`

Title:

**Fingerprints on the World Cup**

Subtitle:

**A structural analysis of how teams shape the game**

## What It Shows

- 2018 and 2022 World Cup event fingerprints.
- A method walkthrough using Argentina vs France, 2022 final.
- 2022 team territory-pressure fingerprints.
- A low-sample 2018 to 2022 drift note.
- Opponent-induced field-position shifts.
- A selectable matchup explorer with structural read-strength labels.

## Position

This page is better after a match or tournament is complete. It is not a live
World Cup tracker: the latest useful signal depends on full event data, stable
rosters, and the complete match context.

## Data

Generated from StatsBomb Open Data:

`G:/GEME/EE/game_codex/scripts/export_football_site_data.py`

Outputs:

- `G:/GEME/EE/game_codex/results/football/football_site_data.json`
- `G:/GameCodex/football/data/football-data.js`

Current encoded sample:

- 128 World Cup matches.
- 456,536 located events.
- 32 team fingerprints.

## Caveat

This is not a win model, score predictor, roster forecast, or real-time
updater. It reads structural tendency after the match record exists: territory,
pressure, event texture, opponent effect, and matchup shape.
