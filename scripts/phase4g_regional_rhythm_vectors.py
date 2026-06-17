"""Phase 4G: regional rhythm vectors for the interactive page.

This exports phase-level country/event-stream centroids in the same SHP rhythm
space used by the manuscript. The goal is presentation: show convergence as
country vectors moving toward or away from a shared phase center.
"""

from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
OUT_VECTORS = ROOT / "results" / "phase4" / "regional_phase_vectors.csv"
OUT_PAIRS = ROOT / "results" / "phase4" / "regional_phase_pairwise.csv"
SGF_COLS = "abcdefghijklmnopqrs"
FEATURES = ["adj_opp", "adj_own", "dens_delta", "dist_last", "is_corner_open"]
REGIONS = ["JPN", "KOR", "CHN"]

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


def sgf_to_xy(move: str) -> tuple[int, int] | None:
    if not move or len(move) < 2:
        return None
    x = SGF_COLS.find(move[0])
    y = SGF_COLS.find(move[1])
    if x < 0 or y < 0:
        return None
    return x, y


def move_rhythm(prefix_moves: list[list[str]], candidate_sgf: str) -> dict[str, float] | None:
    board = {}
    for color, coord in prefix_moves:
        xy = sgf_to_xy(coord)
        if xy is not None:
            board[xy] = color

    target = sgf_to_xy(candidate_sgf)
    if target is None:
        return None

    tx, ty = target
    move_color = "B" if len(prefix_moves) % 2 == 0 else "W"
    opp_color = "W" if move_color == "B" else "B"
    board[(tx, ty)] = move_color

    adj_opp = 0
    adj_own = 0
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        neighbor = board.get((tx + dx, ty + dy))
        if neighbor == opp_color:
            adj_opp += 1
        elif neighbor == move_color:
            adj_own += 1

    own_count = 0
    opp_count = 0
    for (sx, sy), color in board.items():
        if (sx, sy) == (tx, ty):
            continue
        if math.sqrt((tx - sx) ** 2 + (ty - sy) ** 2) <= 3:
            if color == opp_color:
                opp_count += 1
            elif color == move_color:
                own_count += 1

    last = sgf_to_xy(prefix_moves[-1][1])
    dist_last = math.sqrt((tx - last[0]) ** 2 + (ty - last[1]) ** 2) / 20.0 if last else 1.0
    corner_d = (
        min(
            math.sqrt(tx**2 + ty**2),
            math.sqrt(tx**2 + (18 - ty) ** 2),
            math.sqrt((18 - tx) ** 2 + ty**2),
            math.sqrt((18 - tx) ** 2 + (18 - ty) ** 2),
        )
        / 13.0
    )

    return {
        "adj_opp": adj_opp / 4.0,
        "adj_own": adj_own / 4.0,
        "dens_delta": (own_count - opp_count) / 10.0,
        "dist_last": dist_last,
        "is_corner_open": 1.0 if corner_d * 13.0 < 4 else 0.0,
    }


def distance(left: dict[str, float], right: dict[str, float]) -> float:
    return math.sqrt(sum((left[key] - right[key]) ** 2 for key in FEATURES))


def main() -> None:
    source = parsed_csv_path()
    values: dict[tuple[str, str], dict[str, list[float]]] = defaultdict(
        lambda: defaultdict(list)
    )

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

            try:
                moves = json.loads(row.get("moves", "[]"))
            except json.JSONDecodeError:
                continue
            if len(moves) < 30:
                continue

            phase_key, _, _, _ = phase
            region = classify_region(row.get("event", ""))
            for move_index in range(15, min(len(moves) - 1, 50)):
                rhythm = move_rhythm(moves[:move_index], moves[move_index][1])
                if rhythm is None:
                    continue
                for feature in FEATURES:
                    values[(phase_key, region)][feature].append(rhythm[feature])

    centroids: dict[tuple[str, str], dict[str, float]] = {}
    for key, feature_values in values.items():
        if all(feature_values[feature] for feature in FEATURES):
            centroids[key] = {feature: mean(feature_values[feature]) for feature in FEATURES}

    phase_centers: dict[str, dict[str, float]] = {}
    for phase_key, _, _, _ in PHASES:
        region_vectors = [
            centroids[(phase_key, region)]
            for region in REGIONS
            if (phase_key, region) in centroids
        ]
        phase_centers[phase_key] = {
            feature: mean(vector[feature] for vector in region_vectors)
            for feature in FEATURES
        }

    OUT_VECTORS.parent.mkdir(parents=True, exist_ok=True)
    vector_fields = [
        "phase",
        "phase_label",
        "phase_start",
        "phase_end",
        "region",
        "n_moves",
        *FEATURES,
        "contact_index",
        "mobility_index",
        "gap_to_center",
    ]
    with OUT_VECTORS.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=vector_fields)
        writer.writeheader()
        for phase_key, phase_label, phase_start, phase_end in PHASES:
            center = phase_centers[phase_key]
            for region in REGIONS:
                key = (phase_key, region)
                if key not in centroids:
                    continue
                vector = centroids[key]
                writer.writerow(
                    {
                        "phase": phase_key,
                        "phase_label": phase_label,
                        "phase_start": phase_start,
                        "phase_end": phase_end,
                        "region": region,
                        "n_moves": len(values[key]["adj_opp"]),
                        **{feature: round(vector[feature], 6) for feature in FEATURES},
                        "contact_index": round(vector["adj_opp"] - vector["adj_own"], 6),
                        "mobility_index": round(
                            (vector["dist_last"] + vector["is_corner_open"]) / 2, 6
                        ),
                        "gap_to_center": round(distance(vector, center), 6),
                    }
                )

    pair_fields = [
        "phase",
        "phase_label",
        "phase_start",
        "phase_end",
        "pair",
        "distance",
        "mean_pairwise_distance",
    ]
    with OUT_PAIRS.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=pair_fields)
        writer.writeheader()
        for phase_key, phase_label, phase_start, phase_end in PHASES:
            pair_rows = []
            for left, right in [("JPN", "KOR"), ("JPN", "CHN"), ("KOR", "CHN")]:
                if (phase_key, left) not in centroids or (phase_key, right) not in centroids:
                    continue
                pair_rows.append(
                    {
                        "pair": f"{left}-{right}",
                        "distance": distance(
                            centroids[(phase_key, left)], centroids[(phase_key, right)]
                        ),
                    }
                )
            mean_distance = mean(row["distance"] for row in pair_rows)
            for row in pair_rows:
                writer.writerow(
                    {
                        "phase": phase_key,
                        "phase_label": phase_label,
                        "phase_start": phase_start,
                        "phase_end": phase_end,
                        "pair": row["pair"],
                        "distance": round(row["distance"], 6),
                        "mean_pairwise_distance": round(mean_distance, 6),
                    }
                )

    print(f"Wrote {OUT_VECTORS}")
    print(f"Wrote {OUT_PAIRS}")
    print(f"Source: {source}")


if __name__ == "__main__":
    main()
