"""Phase 4F: country-level opening fingerprint penetration.

This script is intentionally narrow: it computes country/event-stream usage
rates only for qualifying 15-move opening fingerprints already listed in
results/phase4/pattern_metrics.csv.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATTERN_METRICS = ROOT / "results" / "phase4" / "pattern_metrics.csv"
OUT = ROOT / "results" / "phase4" / "pattern_country_phase_counts.csv"
PREFIX_LEN = 15

PARSED_CANDIDATES = [
    ROOT / "data" / "parsed" / "go_games_parsed.csv",
    Path("G:/GEME/EE/game_codex/data/parsed/go_games_parsed.csv"),
]

PHASES = [
    ("pre", "Pre-AI", 1990, 2015),
    ("shock", "Shock", 2016, 2017),
    ("diffusion", "Diffusion", 2018, 2021),
    ("oracle", "Oracle", 2022, 2025),
]

JPN_KW = [
    "meijin",
    "kisei",
    "honinbo",
    "oza",
    "tengen",
    "gosei",
    "judan",
    "nhk",
    "oteai",
    "jal",
    "nec",
    "shinjin",
    "king of new star",
    "ryusei",
    "agon",
    "daiwa",
    "go-net",
    "sumitomo",
    "kirin",
    "all japan",
    "japan",
    "kakusei",
    "shin-ei",
    "hayago",
    "kansai",
    "ki-in",
    "shusaku",
    "dosaku",
    "shusai",
    "honda",
    "nagoya",
    "osaka",
    "tokyo",
]
KOR_KW = [
    "samsung",
    "nongshim",
    "lg",
    "bc card",
    "gs caltex",
    "maxim",
    "korean",
    "kuksu",
    "myungin",
    "chunwon",
    "prices information",
    "wonik",
    "siptan",
    "korea",
    "baduk",
    "hanguk",
    "kbs",
    "olleh",
    "kt",
    "masters",
    "let's run",
]
CHN_KW = [
    "mlily",
    "chinese",
    "tianyuan",
    "mingren",
    "changqi",
    "quzhou",
    "longxing",
    "bailing",
    "weifu",
    "xinao",
    "china",
    "weichi",
    "jianqiao",
    "a han",
    "titan",
    "golden statue",
    "lanke",
]


def parsed_csv_path() -> Path:
    for path in PARSED_CANDIDATES:
        if path.exists():
            return path
    candidates = "\n".join(str(path) for path in PARSED_CANDIDATES)
    raise FileNotFoundError(f"go_games_parsed.csv not found. Checked:\n{candidates}")


def classify_region(event: str) -> str:
    text = (event or "").lower().strip()
    for keyword in JPN_KW:
        if keyword in text:
            return "JPN"
    for keyword in KOR_KW:
        if keyword in text:
            return "KOR"
    for keyword in CHN_KW:
        if keyword in text:
            return "CHN"
    return "JPN"


def phase_for_year(year: int) -> tuple[str, str, int, int] | None:
    for phase in PHASES:
        _, _, start, end = phase
        if start <= year <= end:
            return phase
    return None


def load_patterns() -> set[str]:
    with PATTERN_METRICS.open(newline="", encoding="utf-8") as handle:
        return {row["pattern"] for row in csv.DictReader(handle)}


def prefix_from_moves(raw_moves: str) -> str | None:
    try:
        moves = json.loads(raw_moves)
    except json.JSONDecodeError:
        return None
    if len(moves) < PREFIX_LEN + 1:
        return None
    return ",".join(f"{color}{coord}" for color, coord in moves[:PREFIX_LEN])


def main() -> None:
    patterns = load_patterns()
    source = parsed_csv_path()
    denominators: Counter[tuple[str, str]] = Counter()
    counts: Counter[tuple[str, str, str]] = Counter()
    years_seen: dict[tuple[str, str, str], list[int]] = defaultdict(list)

    with source.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            raw_year = row.get("year") or ""
            if not raw_year or raw_year == "None":
                continue
            year = int(raw_year)
            phase = phase_for_year(year)
            if phase is None:
                continue
            phase_key, _, _, _ = phase
            region = classify_region(row.get("event", ""))
            if region not in {"JPN", "KOR", "CHN"}:
                continue
            prefix = prefix_from_moves(row.get("moves", ""))
            if prefix is None:
                continue

            denominators[(phase_key, region)] += 1
            if prefix in patterns:
                counts[(prefix, phase_key, region)] += 1
                years_seen[(prefix, phase_key, region)].append(year)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "pattern",
        "phase",
        "phase_label",
        "phase_start",
        "phase_end",
        "region",
        "count",
        "denominator",
        "per_1000_games",
        "first_year_in_phase",
        "last_year_in_phase",
    ]
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for pattern in sorted(patterns):
            for phase_key, phase_label, phase_start, phase_end in PHASES:
                for region in ["JPN", "KOR", "CHN"]:
                    count = counts[(pattern, phase_key, region)]
                    denominator = denominators[(phase_key, region)]
                    years = years_seen.get((pattern, phase_key, region), [])
                    writer.writerow(
                        {
                            "pattern": pattern,
                            "phase": phase_key,
                            "phase_label": phase_label,
                            "phase_start": phase_start,
                            "phase_end": phase_end,
                            "region": region,
                            "count": count,
                            "denominator": denominator,
                            "per_1000_games": round((count / denominator) * 1000, 6)
                            if denominator
                            else 0,
                            "first_year_in_phase": min(years) if years else "",
                            "last_year_in_phase": max(years) if years else "",
                        }
                    )

    print(f"Wrote {OUT}")
    print(f"Source: {source}")
    print(f"Patterns: {len(patterns)}")


if __name__ == "__main__":
    main()
