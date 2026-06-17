"""Export lightweight data for the static GameCodex interactive page."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_DATA = ROOT / "site" / "data"
REGION_ORDER = ("JPN", "KOR", "CHN")
REGION_LABELS = {"JPN": "Japan", "KOR": "Korea", "CHN": "China"}
PHASE_KEYS = {
    (1990, 2015): "pre",
    (2016, 2017): "shock",
    (2018, 2021): "diffusion",
    (2022, 2025): "oracle",
}
PHASES = [
    ("pre", "Pre-AI", 1990, 2015),
    ("shock", "Shock", 2016, 2017),
    ("diffusion", "Diffusion", 2018, 2021),
    ("oracle", "Oracle", 2022, 2025),
]


def read_trace() -> list[dict]:
    rows = []
    path = ROOT / "results" / "figures" / "fig0_paired_vignette_trace.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            raw_rank = int(row["policy_rank_zero_indexed"]) + 1
            rows.append(
                {
                    "game": row["game"],
                    "move": int(row["move_number"]),
                    "rank": min(raw_rank, 100),
                    "rawRank": raw_rank,
                    "winrate": round(float(row["human_perspective_winrate"]), 4),
                }
            )
    return rows


def read_decades() -> list[dict]:
    path = ROOT / "results" / "phase05" / "decade_drift.csv"
    decades = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            decades.append(
                {
                    "decade": int(row["decade"]),
                    "label": row["label"],
                    "n_games": int(row["n_games"]),
                    "n_moves": int(row["n_moves"]),
                    "features": {
                        "adj_opp": float(row["adj_opp"]),
                        "adj_own": float(row["adj_own"]),
                        "dens_delta": float(row["dens_delta"]),
                        "dist_last": float(row["dist_last"]),
                        "is_corner_open": float(row["is_corner_open"]),
                    },
                    "novelty": float(row["novelty_rate"]),
                    "cross_harm": float(row["mean_cross_harm"]),
                }
            )
    return decades


def rhythm_distance(left: dict, right: dict) -> float:
    return math.sqrt(
        sum((left["features"][key] - right["features"][key]) ** 2 for key in left["features"])
    )


def stones_from(rows: list[tuple[int, int, str]]) -> list[dict]:
    return [{"x": x, "y": y, "color": color} for x, y, color in rows]


def drift_annotation(left: dict, right: dict) -> dict:
    key = (left["decade"], right["decade"])
    specific = {
        (1910, 1920): {
            "event": "Largest historical comparator",
            "read": (
                "This is the largest jump in the sampled archive. It is a reminder "
                "that institutional circulation and recorded-game composition can "
                "move rhythm more than any single style story."
            ),
        },
        (1950, 1960): {
            "event": "Postwar archive rebuild",
            "read": (
                "The sample expands sharply from 1,868 to 10,847 games. Treat the "
                "bar as a mixed signal: playing style plus a new recording regime."
            ),
        },
        (1970, 1980): {
            "event": "Quiet baseline",
            "read": (
                "The smallest decade-to-decade movement in the panel. This is the "
                "kind of low-drift background the AI decade should be compared with."
            ),
        },
        (1990, 2000): {
            "event": "Regional stream expansion",
            "read": (
                "Korea-coded games become much more visible in the CWI stream. The "
                "database is turning from a Japan-heavy archive into a broader flow."
            ),
        },
        (2010, 2020): {
            "event": "AlphaGo to oracle decade",
            "read": (
                "A real recent movement: stronger open-corner signal and denser "
                "AI-era rhythm. It is large for the last ten years, but not outside "
                "the historical envelope."
            ),
        },
    }
    return specific.get(
        key,
        {
            "event": "Recorded rhythm movement",
            "read": (
                f"The sample changes from {left['n_games']:,} to {right['n_games']:,} "
                "games. Read this bar as a joint trace of board rhythm and archive "
                "composition."
            ),
        },
    )


def build_drift_pairs(decades: list[dict]) -> list[dict]:
    pairs = []
    for left, right in zip(decades, decades[1:]):
        annotation = drift_annotation(left, right)
        pairs.append(
            {
                "from": left["label"],
                "to": right["label"],
                "from_decade": left["decade"],
                "to_decade": right["decade"],
                "value": round(rhythm_distance(left, right), 4),
                "n_games_to": right["n_games"],
                "is_ai_era": left["decade"] == 2010 and right["decade"] == 2020,
                "is_largest": left["decade"] == 1910 and right["decade"] == 1920,
                "event": annotation["event"],
                "read": annotation["read"],
            }
        )
    return pairs


def read_archive() -> list[dict]:
    path = ROOT / "results" / "phase4" / "archive_composition_by_decade.csv"
    rows = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if int(row["decade"]) < 1950:
                continue
            rows.append(
                {
                    "decade": int(row["decade"]),
                    "label": row["label"],
                    "total": int(row["total"]),
                    "JPN": int(row["JPN"]),
                    "KOR": int(row["KOR"]),
                    "CHN": int(row["CHN"]),
                    "INTL": int(row["INTL"]),
                    "unknown": int(row["unknown"]),
                    "entropy": round(float(row["region_entropy"]), 4),
                }
            )
    return rows


def read_region_share_timeline() -> list[dict]:
    path = ROOT / "results" / "phase4" / "region_share_timeline.csv"
    rows = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                {
                    "year": int(row["year"]),
                    "JPN": int(row["JPN"]),
                    "KOR": int(row["KOR"]),
                    "CHN": int(row["CHN"]),
                }
            )
    return rows


def phase_region_mix(start: int, end: int) -> dict:
    rows = [row for row in read_region_share_timeline() if start <= row["year"] <= end]
    counts = {
        "Japan": sum(row["JPN"] for row in rows),
        "Korea": sum(row["KOR"] for row in rows),
        "China": sum(row["CHN"] for row in rows),
    }
    total = sum(counts.values()) or 1
    return {
        "counts": counts,
        "shares": {key: round(value / total, 3) for key, value in counts.items()},
        "total": total,
    }


def read_pattern_examples() -> list[dict]:
    path = ROOT / "results" / "phase4" / "pattern_metrics.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    def has_lag(row: dict) -> bool:
        return row.get("adoption_lag") not in ("", None)

    def make_example(row: dict, label: str, summary: str) -> dict:
        first_seen = int(row["first_seen"])
        adoption_lag = int(float(row["adoption_lag"])) if has_lag(row) else None
        adopted_year = first_seen + adoption_lag if adoption_lag is not None else None
        return {
            "label": label,
            "pattern": row["pattern"],
            "firstSeen": first_seen,
            "adoptedYear": adopted_year,
            "adoptionLag": adoption_lag,
            "peakYear": int(row["peak_year"]),
            "peakUsage": int(row["peak_usage"]),
            "lastSeen": int(row["last_seen"]),
            "totalUses": int(row["total_uses"]),
            "reuseRate": round(float(row["reuse_rate"]), 3),
            "nRegions": int(row["n_regions"]),
            "summary": summary,
        }

    pre_candidates = [
        row
        for row in rows
        if has_lag(row) and int(row["first_seen"]) < 1980 and 4 <= float(row["adoption_lag"]) <= 9
    ]
    ai_candidates = [
        row
        for row in rows
        if has_lag(row) and int(row["first_seen"]) >= 2016 and float(row["adoption_lag"]) <= 2
    ]
    pre = sorted(pre_candidates, key=lambda row: -int(row["total_uses"]))[0]
    ai = sorted(ai_candidates, key=lambda row: -int(row["total_uses"]))[0]
    return [
        make_example(
            pre,
            "Pre-1980 circulation",
            "A slow-moving opening fingerprint: it appears in 1960, reaches three-plus players five years later, and peaks near the end of that decade.",
        ),
        make_example(
            ai,
            "AI-era circulation",
            "A fast-moving opening fingerprint: it appears after public AI oracles and reaches multi-player reuse immediately in the observed record.",
        ),
    ]


def read_regional_convergence_example() -> dict:
    path = ROOT / "results" / "phase4" / "pattern_metrics.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    candidates = [
        row
        for row in rows
        if int(row["first_seen"]) >= 2018
        and int(row["n_regions"]) == 3
        and row.get("cross_region_lag") not in ("", None)
    ]
    row = sorted(candidates, key=lambda item: -int(item["total_uses"]))[0]
    first_seen = int(row["first_seen"])
    cross_lag = int(float(row["cross_region_lag"]))
    return {
        "label": "Cross-stream opening fingerprint",
        "pattern": row["pattern"],
        "firstSeen": first_seen,
        "threeStreamYear": first_seen + cross_lag,
        "crossRegionLag": cross_lag,
        "totalUses": int(row["total_uses"]),
        "peakYear": int(row["peak_year"]),
        "peakUsage": int(row["peak_usage"]),
        "reuseRate": round(float(row["reuse_rate"]), 3),
        "penetration": [
            {"name": "Japan", "observed": True},
            {"name": "Korea", "observed": True},
            {"name": "China", "observed": True},
        ],
        "note": (
            "Observed in all three event streams. This is a conservative presence/absence "
            "reading, not a per-player market-share estimate."
        ),
    }


def read_country_pattern_counts() -> dict[tuple[str, str], dict[str, dict]]:
    path = ROOT / "results" / "phase4" / "pattern_country_phase_counts.csv"
    if not path.exists():
        return {}

    data: dict[tuple[str, str], dict[str, dict]] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            key = (row["pattern"], row["phase"])
            region = row["region"]
            data.setdefault(key, {})[region] = {
                "code": region,
                "name": REGION_LABELS.get(region, region),
                "count": int(row["count"]),
                "denominator": int(row["denominator"]),
                "per1000": round(float(row["per_1000_games"]), 3),
                "firstYear": int(row["first_year_in_phase"]) if row["first_year_in_phase"] else None,
                "lastYear": int(row["last_year_in_phase"]) if row["last_year_in_phase"] else None,
            }
    return data


def read_fingerprint_penetration(start: int, end: int) -> list[dict]:
    path = ROOT / "results" / "phase4" / "pattern_metrics.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    phase_key = PHASE_KEYS[(start, end)]
    country_counts = read_country_pattern_counts()

    def as_int(row: dict, key: str) -> int:
        return int(float(row[key]))

    def countries_for(row: dict) -> list[dict]:
        observed = country_counts.get((row["pattern"], phase_key), {})
        countries = []
        for code in REGION_ORDER:
            countries.append(
                observed.get(
                    code,
                    {
                        "code": code,
                        "name": REGION_LABELS[code],
                        "count": 0,
                        "denominator": 0,
                        "per1000": 0.0,
                        "firstYear": None,
                        "lastYear": None,
                    },
                )
            )
        return countries

    def country_count(row: dict) -> int:
        return sum(1 for country in countries_for(row) if country["count"] > 0)

    def phase_uses(row: dict) -> int:
        return sum(country["count"] for country in countries_for(row))

    def max_rate(row: dict) -> float:
        return max((country["per1000"] for country in countries_for(row)), default=0.0)

    active = [
        row
        for row in rows
        if as_int(row, "first_seen") <= end and as_int(row, "last_seen") >= start
        and phase_uses(row) > 0
    ]
    selected = []
    used = set()

    for n_countries in [1, 2, 3]:
        candidates = [row for row in active if country_count(row) == n_countries]
        if not candidates:
            continue
        candidates.sort(
            key=lambda row: (
                0 if start <= as_int(row, "first_seen") <= end else 1,
                -phase_uses(row),
                -max_rate(row),
                as_int(row, "first_seen"),
            )
        )
        row = candidates[0]
        selected.append(row)
        used.add(row["pattern"])

    if len(selected) < 3:
        fillers = [row for row in active if row["pattern"] not in used]
        fillers.sort(key=lambda row: (-country_count(row), -phase_uses(row), -max_rate(row)))
        selected.extend(fillers[: 3 - len(selected)])

    def make(row: dict) -> dict:
        countries = countries_for(row)
        n_countries = sum(1 for country in countries if country["count"] > 0)
        phase_total = sum(country["count"] for country in countries)
        peak_country = max(countries, key=lambda country: country["per1000"])
        first_seen = as_int(row, "first_seen")
        last_seen = as_int(row, "last_seen")
        cross_lag = row.get("cross_region_lag")
        adoption_lag = row.get("adoption_lag")
        status = "new in phase" if start <= first_seen <= end else "active carry-over"
        return {
            "pattern": row["pattern"],
            "firstSeen": first_seen,
            "lastSeen": last_seen,
            "totalUses": as_int(row, "total_uses"),
            "phaseUses": phase_total,
            "peakYear": as_int(row, "peak_year"),
            "peakUsage": as_int(row, "peak_usage"),
            "nRegions": as_int(row, "n_regions"),
            "countryCount": n_countries,
            "countries": countries,
            "maxPer1000": round(max(country["per1000"] for country in countries), 3),
            "penetration": round(n_countries / 3, 3),
            "streamLabel": f"{n_countries}/3 countries",
            "crossRegionLag": int(float(cross_lag)) if cross_lag not in ("", None) else None,
            "adoptionLag": int(float(adoption_lag)) if adoption_lag not in ("", None) else None,
            "reuseRate": round(float(row["reuse_rate"]), 3),
            "status": status,
            "summary": (
                f"{status}; {phase_total} uses in this phase. "
                f"Highest normalized rate: {peak_country['name']} "
                f"({peak_country['per1000']:.2f}/1k games)."
            ),
        }

    selected.sort(key=lambda row: country_count(row))
    return [make(row) for row in selected[:3]]


def read_regional_rhythm_vectors() -> dict:
    vector_path = ROOT / "results" / "phase4" / "regional_phase_vectors.csv"
    pair_path = ROOT / "results" / "phase4" / "regional_phase_pairwise.csv"
    if not vector_path.exists() or not pair_path.exists():
        return {"phases": {}, "bounds": {}}

    phases: dict[str, dict] = {}
    contact_values = []
    mobility_values = []

    with vector_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            phase = row["phase"]
            vector = {
                "region": row["region"],
                "label": REGION_LABELS.get(row["region"], row["region"]),
                "nMoves": int(row["n_moves"]),
                "features": {
                    "adj_opp": float(row["adj_opp"]),
                    "adj_own": float(row["adj_own"]),
                    "dens_delta": float(row["dens_delta"]),
                    "dist_last": float(row["dist_last"]),
                    "is_corner_open": float(row["is_corner_open"]),
                },
                "contactIndex": float(row["contact_index"]),
                "mobilityIndex": float(row["mobility_index"]),
                "gapToCenter": float(row["gap_to_center"]),
            }
            phases.setdefault(phase, {"vectors": [], "pairs": [], "meanDistance": None})
            phases[phase]["vectors"].append(vector)
            contact_values.append(vector["contactIndex"])
            mobility_values.append(vector["mobilityIndex"])

    with pair_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            phase = row["phase"]
            phases.setdefault(phase, {"vectors": [], "pairs": [], "meanDistance": None})
            phases[phase]["pairs"].append(
                {
                    "pair": row["pair"].replace("-", " - "),
                    "distance": float(row["distance"]),
                }
            )
            phases[phase]["meanDistance"] = float(row["mean_pairwise_distance"])

    ordered = [phase for phase, _, _, _ in PHASES]
    previous = None
    for phase in ordered:
        data = phases.get(phase)
        if not data or data["meanDistance"] is None:
            continue
        if previous:
            prev_distance = phases[previous]["meanDistance"]
            data["deltaFromPrevious"] = round(data["meanDistance"] - prev_distance, 6)
            data["deltaFromPreviousPct"] = round(
                ((data["meanDistance"] / prev_distance) - 1) * 100, 1
            )
        else:
            data["deltaFromPrevious"] = None
            data["deltaFromPreviousPct"] = None
        previous = phase

    def padded_bounds(values: list[float]) -> dict:
        low = min(values)
        high = max(values)
        pad = (high - low) * 0.18 or 0.001
        return {"min": round(low - pad, 6), "max": round(high + pad, 6)}

    return {
        "phases": phases,
        "bounds": {
            "contact": padded_bounds(contact_values),
            "mobility": padded_bounds(mobility_values),
        },
    }


def build_payload() -> dict:
    trace_rows = read_trace()
    decades = read_decades()
    regional_rhythm = read_regional_rhythm_vectors()
    return {
        "meta": {
            "title": "How AI Changed Go: A Decade Review",
            "claim": (
                "AlphaGo changed how Go learns: moves query an oracle, patterns "
                "spread faster, and regional event streams reorganize."
            ),
            "generatedFrom": [
                "fig0_paired_vignette_trace.csv",
                "decade_drift.csv",
                "archive_composition_by_decade.csv",
                "PHASE5_HARDENING_2026-06-15.txt",
            ],
        },
        "pairedVignette": {
            "games": [
                {
                    "id": "lee",
                    "label": "Lee Sedol vs AlphaGo, Game 4 (2016)",
                    "shortLabel": "Lee Sedol 2016",
                    "note": (
                        "The red tick marks move 68, where Lee begins the forcing sequence. "
                        "Ten moves later, the famous God Move appears: KataGo reads it as policy "
                        "rank 3 while the win-rate trace is still only 1.4%."
                    ),
                    "markers": [
                        {
                            "move": 68,
                            "label": "move 68: forcing sequence begins",
                            "kind": "event",
                        },
                    ],
                    "quote": {
                        "lead": "Lee later described the sequence this way:",
                        "text": "Every move from 68 to 78 was a trick.",
                        "sourceLabel": "Korea JoongAng Daily",
                        "url": "https://www.koreajoongangdaily.com/business/grandmaster-lee-se-dol-reveals-how-he-beat-alphago-every-move-was-a-trick/12299151",
                    },
                    "pivotMove": 78,
                    "rows": [row for row in trace_rows if row["game"].startswith("Lee Sedol")],
                },
                {
                    "id": "ke",
                    "label": "Ke Jie vs AlphaGo Master, Game 1 (2017)",
                    "shortLabel": "Ke Jie 2017",
                    "note": (
                        "The red tick marks AlphaGo's white 54 cut. Ke stays policy-aligned "
                        "around moves 58-60, but by move 62 the win-rate trace has fallen "
                        "from about 51% to 25.7%."
                    ),
                    "markers": [
                        {
                            "move": 54,
                            "label": "move 54: AlphaGo cut",
                            "kind": "event",
                        },
                    ],
                    "quote": {
                        "lead": "Later reporting paraphrased Ke's pressure this way:",
                        "text": "Ke felt he had entered AlphaGo's rhythm.",
                        "sourceLabel": "INSIDE / Leiphone",
                        "url": "https://www.inside.com.tw/article/9392-analyzing-alphago-versus-ke-jie-round-1",
                        "isParaphrase": True,
                    },
                    "pivotMove": None,
                    "rows": [row for row in trace_rows if row["game"].startswith("Ke Jie")],
                },
            ]
        },
        "stageVignettes": {
            "stages": [
                {
                    "id": "opening",
                    "label": "Opening / JPN",
                    "chroma": 18,
                    "regionTag": "Japan-coded opening anchor",
                    "source": "Yasuda Shusaku vs Inoue Gennan Inseki, 1846",
                    "sourceUrl": "https://homepages.cwi.nl/~aeb/go/games/games/Shusaku/126.sgf",
                    "positionNote": (
                        "Position after 17 moves. Candidate A is the recorded next "
                        "move; B and C are KataGo-style policy probes for the same board."
                    ),
                    "stones": stones_from(
                        [
                            (3, 2, "white"),
                            (14, 2, "white"),
                            (16, 3, "black"),
                            (15, 4, "black"),
                            (2, 5, "white"),
                            (15, 13, "black"),
                            (14, 14, "white"),
                            (15, 14, "black"),
                            (16, 14, "white"),
                            (2, 15, "black"),
                            (4, 15, "black"),
                            (13, 15, "white"),
                            (14, 15, "black"),
                            (15, 15, "white"),
                            (16, 15, "white"),
                            (14, 16, "black"),
                            (15, 16, "black"),
                        ]
                    ),
                    "candidates": [
                        {
                            "id": "opening_actual",
                            "key": "A",
                            "name": "recorded corner answer",
                            "moveNumber": 18,
                            "x": 16,
                            "y": 16,
                            "color": "white",
                            "aiGap": 0,
                            "reference": "actual",
                            "rhythm": "local answer in a live corner",
                        },
                        {
                            "id": "opening_trad",
                            "key": "B",
                            "name": "upper-right attachment",
                            "moveNumber": 18,
                            "x": 16,
                            "y": 2,
                            "color": "white",
                            "aiGap": 0.17,
                            "reference": "KG-style",
                            "rhythm": "corner contact probe",
                        },
                        {
                            "id": "opening_center",
                            "key": "C",
                            "name": "left-side shoulder hit",
                            "x": 3,
                            "y": 6,
                            "moveNumber": 18,
                            "color": "white",
                            "aiGap": 0.28,
                            "reference": "KG-style",
                            "rhythm": "side pressure probe",
                        },
                    ],
                },
                {
                    "id": "middle",
                    "label": "Middle / KOR",
                    "chroma": 52,
                    "regionTag": "Korea-coded fighting pressure",
                    "source": "AlphaGo vs Lee Sedol, Game 4, 2016",
                    "sourceUrl": "https://homepages.cwi.nl/~aeb/go/games/games/AlphaGo/LeeSedol/4.sgf",
                    "positionNote": (
                        "Position after 67 moves, just before Lee's move-68 forcing "
                        "sequence. Candidate A is the recorded next move and rank 4 "
                        "in the KataGo trace."
                    ),
                    "stones": stones_from(
                        [
                            (13, 1, "black"),
                            (3, 2, "black"),
                            (4, 2, "white"),
                            (7, 2, "black"),
                            (11, 2, "white"),
                            (12, 2, "white"),
                            (13, 2, "black"),
                            (2, 3, "black"),
                            (4, 3, "black"),
                            (7, 3, "black"),
                            (8, 3, "white"),
                            (12, 3, "black"),
                            (13, 3, "black"),
                            (15, 3, "black"),
                            (12, 4, "black"),
                            (13, 4, "white"),
                            (5, 5, "white"),
                            (6, 5, "black"),
                            (11, 5, "black"),
                            (12, 5, "white"),
                            (13, 5, "white"),
                            (2, 6, "white"),
                            (5, 6, "white"),
                            (6, 6, "black"),
                            (9, 6, "white"),
                            (12, 6, "black"),
                            (13, 6, "white"),
                            (4, 7, "white"),
                            (5, 7, "black"),
                            (11, 7, "black"),
                            (12, 7, "black"),
                            (13, 7, "white"),
                            (4, 8, "white"),
                            (5, 8, "black"),
                            (11, 8, "black"),
                            (12, 8, "white"),
                            (13, 8, "black"),
                            (14, 8, "white"),
                            (15, 8, "white"),
                            (16, 8, "white"),
                            (1, 9, "white"),
                            (2, 9, "white"),
                            (3, 9, "white"),
                            (4, 9, "black"),
                            (12, 9, "white"),
                            (13, 9, "black"),
                            (14, 9, "black"),
                            (15, 9, "black"),
                            (2, 10, "black"),
                            (3, 10, "black"),
                            (5, 10, "black"),
                            (12, 10, "white"),
                            (2, 13, "black"),
                            (4, 14, "white"),
                            (15, 14, "white"),
                            (1, 15, "white"),
                            (3, 15, "white"),
                            (4, 15, "black"),
                            (5, 15, "white"),
                            (12, 15, "black"),
                            (14, 15, "black"),
                            (16, 15, "white"),
                            (5, 16, "white"),
                            (8, 16, "black"),
                            (13, 16, "black"),
                            (14, 16, "white"),
                            (15, 16, "white"),
                        ]
                    ),
                    "candidates": [
                        {
                            "id": "middle_actual",
                            "key": "A",
                            "name": "recorded right-side probe",
                            "moveNumber": 68,
                            "x": 16,
                            "y": 9,
                            "color": "white",
                            "aiGap": 0,
                            "reference": "rank 4",
                            "rhythm": "contact pressure",
                        },
                        {
                            "id": "middle_godpoint",
                            "key": "B",
                            "name": "right-side clamp",
                            "moveNumber": 68,
                            "x": 16,
                            "y": 7,
                            "color": "white",
                            "aiGap": 0.08,
                            "reference": "KG-style",
                            "rhythm": "edge fight compression",
                        },
                        {
                            "id": "middle_tenuki",
                            "key": "C",
                            "name": "upper-side attachment",
                            "moveNumber": 68,
                            "x": 8,
                            "y": 2,
                            "color": "white",
                            "aiGap": 0.24,
                            "reference": "KG-style",
                            "rhythm": "thin-shape pressure",
                        },
                    ],
                },
                {
                    "id": "endgame",
                    "label": "Endgame / CHN",
                    "chroma": 84,
                    "regionTag": "China-coded oracle pressure",
                    "source": "Ke Jie vs AlphaGo, Game 1, 2017",
                    "sourceUrl": "https://homepages.cwi.nl/~aeb/go/games/games/AlphaGo/May2017/1.sgf",
                    "positionNote": (
                        "Position after 115 moves in the same match used in the "
                        "policy trace. Candidate A is the recorded next move and "
                        "KataGo's top-ranked move in the trace."
                    ),
                    "stones": stones_from(
                        [
                            (6, 1, "black"),
                            (7, 1, "white"),
                            (1, 2, "white"),
                            (2, 2, "black"),
                            (3, 2, "white"),
                            (6, 2, "black"),
                            (8, 2, "white"),
                            (10, 2, "white"),
                            (11, 2, "white"),
                            (13, 2, "black"),
                            (16, 2, "black"),
                            (1, 3, "white"),
                            (2, 3, "black"),
                            (3, 3, "white"),
                            (8, 3, "white"),
                            (9, 3, "black"),
                            (11, 3, "black"),
                            (14, 3, "black"),
                            (16, 3, "black"),
                            (17, 3, "white"),
                            (1, 4, "black"),
                            (2, 4, "white"),
                            (3, 4, "white"),
                            (6, 4, "black"),
                            (8, 4, "white"),
                            (9, 4, "black"),
                            (11, 4, "black"),
                            (15, 4, "black"),
                            (16, 4, "white"),
                            (17, 4, "white"),
                            (0, 5, "black"),
                            (2, 5, "black"),
                            (3, 5, "black"),
                            (4, 5, "black"),
                            (7, 5, "white"),
                            (9, 5, "white"),
                            (15, 5, "white"),
                            (16, 5, "black"),
                            (17, 5, "white"),
                            (1, 6, "black"),
                            (4, 6, "black"),
                            (5, 6, "white"),
                            (6, 6, "black"),
                            (7, 6, "white"),
                            (16, 6, "black"),
                            (17, 6, "white"),
                            (0, 7, "black"),
                            (1, 7, "white"),
                            (2, 7, "white"),
                            (3, 7, "white"),
                            (4, 7, "white"),
                            (5, 7, "black"),
                            (10, 7, "black"),
                            (13, 7, "black"),
                            (15, 7, "black"),
                            (16, 7, "black"),
                            (2, 8, "black"),
                            (3, 8, "white"),
                            (4, 8, "black"),
                            (5, 8, "black"),
                            (16, 8, "white"),
                            (2, 9, "black"),
                            (3, 9, "black"),
                            (4, 9, "white"),
                            (4, 10, "white"),
                            (13, 10, "white"),
                            (8, 11, "white"),
                            (2, 12, "white"),
                            (16, 12, "white"),
                            (17, 12, "white"),
                            (8, 13, "white"),
                            (9, 13, "black"),
                            (10, 13, "black"),
                            (14, 13, "white"),
                            (15, 13, "black"),
                            (16, 13, "white"),
                            (17, 13, "black"),
                            (1, 14, "white"),
                            (8, 14, "white"),
                            (9, 14, "white"),
                            (10, 14, "black"),
                            (15, 14, "white"),
                            (16, 14, "black"),
                            (1, 15, "black"),
                            (2, 15, "white"),
                            (3, 15, "white"),
                            (4, 15, "white"),
                            (5, 15, "white"),
                            (7, 15, "black"),
                            (9, 15, "black"),
                            (10, 15, "white"),
                            (11, 15, "black"),
                            (15, 15, "white"),
                            (16, 15, "black"),
                            (1, 16, "black"),
                            (2, 16, "black"),
                            (3, 16, "black"),
                            (4, 16, "black"),
                            (6, 16, "white"),
                            (7, 16, "black"),
                            (10, 16, "white"),
                            (11, 16, "black"),
                            (14, 16, "black"),
                            (15, 16, "white"),
                            (16, 16, "black"),
                            (6, 17, "white"),
                            (8, 17, "white"),
                            (10, 17, "white"),
                            (11, 17, "black"),
                            (14, 17, "white"),
                            (15, 17, "black"),
                            (17, 17, "black"),
                            (16, 18, "black"),
                        ]
                    ),
                    "candidates": [
                        {
                            "id": "endgame_actual",
                            "key": "A",
                            "name": "recorded boundary sente",
                            "moveNumber": 116,
                            "x": 17,
                            "y": 7,
                            "color": "white",
                            "aiGap": 0,
                            "reference": "rank 1",
                            "rhythm": "local forcing move",
                        },
                        {
                            "id": "endgame_safe",
                            "key": "B",
                            "name": "right-side follow-up",
                            "moveNumber": 116,
                            "x": 16,
                            "y": 9,
                            "color": "white",
                            "aiGap": 0.14,
                            "reference": "KG-style",
                            "rhythm": "edge boundary test",
                        },
                        {
                            "id": "endgame_far",
                            "key": "C",
                            "name": "lower-side sente",
                            "moveNumber": 116,
                            "x": 12,
                            "y": 17,
                            "color": "white",
                            "aiGap": 0.27,
                            "reference": "KG-style",
                            "rhythm": "late boundary probe",
                        },
                    ],
                },
            ]
        },
        "drift": {
            "decades": decades,
            "pairs": build_drift_pairs(decades),
            "summary": {
                "aiEra": 0.0130,
                "pre2016Mean": 0.0146,
                "largest": 0.0342,
                "largestLabel": "1910s -> 1920s",
                "minLabel": "1970s -> 1980s",
                "min": 0.0040,
            },
        },
        "adoption": {
            "definition": {
                "unit": "Exact 15-move opening fingerprint",
                "qualifier": "Counted only if it appears at least 5 times and across at least 3 years.",
                "interpretation": (
                    "This is a conservative proxy for an opening pattern: exact, reproducible, "
                    "and easy to track through the archive."
                ),
                "nPatterns": 546,
            },
            "examples": read_pattern_examples(),
            "horizons": [1, 2, 3, 5],
            "eras": [
                {
                    "era": "pre-1980",
                    "n": 190,
                    "rates": {"1": 0.31, "2": 0.37, "3": 0.39, "5": 0.44},
                    "meanLag": 6.3,
                    "medianLag": 2,
                },
                {
                    "era": "1980-1999",
                    "n": 154,
                    "rates": {"1": 0.24, "2": 0.29, "3": 0.36, "5": 0.43},
                    "meanLag": 5.7,
                    "medianLag": 3,
                },
                {
                    "era": "2000-2015",
                    "n": 87,
                    "rates": {"1": 0.47, "2": 0.60, "3": 0.63, "5": 0.59},
                    "meanLag": 2.6,
                    "medianLag": 1,
                },
                {
                    "era": "2016+",
                    "n": 115,
                    "rates": {"1": 0.57, "2": 0.73, "3": 0.80, "5": 0.91},
                    "meanLag": 1.5,
                    "medianLag": 1,
                },
            ],
            "lagRatio": 4.2,
            "lagRatioCI": [2.9, 5.9],
            "reuseRatio": 2.3,
            "reuseRatioCI": [2.1, 2.5],
        },
        "regional": {
            "streams": [
                {
                    "id": "jpn",
                    "label": "Japan",
                    "short": "anchor stream",
                    "note": "Long archive anchor",
                    "color": "#101010",
                },
                {
                    "id": "kor",
                    "label": "Korea",
                    "short": "fighting stream",
                    "note": "Contact-heavy diffusion peak",
                    "color": "#a33c2f",
                },
                {
                    "id": "chn",
                    "label": "China",
                    "short": "mobility stream",
                    "note": "Strongest oracle-era convergence",
                    "color": "#23645b",
                },
            ],
            "convergenceExample": read_regional_convergence_example(),
            "rhythmBounds": regional_rhythm.get("bounds", {}),
            "phases": [
                {
                    "phase": "Pre-AI",
                    "plain": "Separate streams",
                    "years": "1990-2015",
                    "distance": regional_rhythm["phases"].get("pre", {}).get(
                        "meanDistance", 0.0144
                    ),
                    "note": "Three recorded streams have distinct rhythm signatures before AlphaGo.",
                    "mechanism": "Baseline: the Japan, Korea, and China streams are already not the same archive flow.",
                    "styleReads": [
                        {
                            "label": "Japan",
                            "value": "adj_opp 0.1421",
                            "note": "corner 0.1326; step 0.1794. Least opponent contact and most continuous stepping.",
                        },
                        {
                            "label": "Korea",
                            "value": "adj_opp 0.1454",
                            "note": "corner 0.1422; step 0.1825. More contact and mobility than Japan.",
                        },
                        {
                            "label": "China",
                            "value": "adj_opp 0.1484",
                            "note": "corner 0.1464; step 0.1834. Highest baseline contact and mobility.",
                        },
                    ],
                    "rhythm": regional_rhythm["phases"].get("pre", {}),
                    "mix": phase_region_mix(1990, 2015),
                },
                {
                    "phase": "Shock",
                    "plain": "Shared surprise",
                    "years": "2016-2017",
                    "distance": regional_rhythm["phases"].get("shock", {}).get(
                        "meanDistance", 0.0066
                    ),
                    "note": "AlphaGo becomes a single public reference point, so recorded rhythms pull closer.",
                    "mechanism": "Everyone is reacting to the same event before local adaptations have time to separate.",
                    "styleReads": [
                        {
                            "label": "mean distance",
                            "value": "0.0070",
                            "note": "Mean of the three pairwise gaps in phase-aggregated SHP rhythm vectors.",
                        },
                        {
                            "label": "tightest pair",
                            "value": "JPN-KOR 0.0033",
                            "note": "The two largest archive streams pull closest during the public shock.",
                        },
                        {
                            "label": "vs Pre-AI",
                            "value": "-33%",
                            "note": "Distance drops relative to the 1990-2015 baseline.",
                        },
                    ],
                    "rhythm": regional_rhythm["phases"].get("shock", {}),
                    "mix": phase_region_mix(2016, 2017),
                },
                {
                    "phase": "Diffusion",
                    "plain": "Local adaptation",
                    "years": "2018-2021",
                    "distance": regional_rhythm["phases"].get("diffusion", {}).get(
                        "meanDistance", 0.0167
                    ),
                    "note": "Public engines spread into training, and each stream absorbs them differently.",
                    "mechanism": "This is where AI does not simply flatten style: it can temporarily amplify local habits.",
                    "styleReads": [
                        {
                            "label": "mean distance",
                            "value": "0.0121",
                            "note": "Mean of the three pairwise gaps in phase-aggregated SHP rhythm vectors.",
                        },
                        {
                            "label": "Korea combat",
                            "value": "+0.038",
                            "note": "Fighting index peak in 2018-2021, up from +0.027 in 2008-2015.",
                        },
                        {
                            "label": "vs Shock",
                            "value": "+153%",
                            "note": "The distance rebound shows differentiated absorption rather than flat convergence.",
                        },
                    ],
                    "rhythm": regional_rhythm["phases"].get("diffusion", {}),
                    "mix": phase_region_mix(2018, 2021),
                },
                {
                    "phase": "Oracle",
                    "plain": "Routine reference",
                    "years": "2022-2025",
                    "distance": regional_rhythm["phases"].get("oracle", {}).get(
                        "meanDistance", 0.0102
                    ),
                    "note": "Engine consultation becomes ordinary; streams settle into a closer configuration.",
                    "mechanism": "The oracle is no longer a shock. It becomes background infrastructure for move choice.",
                    "styleReads": [
                        {
                            "label": "mean distance",
                            "value": "0.0065",
                            "note": "Mean of the three pairwise gaps in phase-aggregated SHP rhythm vectors.",
                        },
                        {
                            "label": "Korea combat",
                            "value": "+0.032",
                            "note": "Down from the diffusion peak, suggesting stabilization after amplification.",
                        },
                        {
                            "label": "China pairs",
                            "value": "0.0071 / 0.0068",
                            "note": "JPN-CHN and KOR-CHN distances in the 2020s convergence check.",
                        },
                    ],
                    "rhythm": regional_rhythm["phases"].get("oracle", {}),
                    "mix": phase_region_mix(2022, 2025),
                },
            ],
            "signatures": [
                {
                    "region": "JPN-coded",
                    "adj_opp": 0.1421,
                    "is_corner_open": 0.1326,
                    "dist_last": 0.1794,
                },
                {
                    "region": "KOR-coded",
                    "adj_opp": 0.1454,
                    "is_corner_open": 0.1422,
                    "dist_last": 0.1825,
                },
                {
                    "region": "CHN-coded",
                    "adj_opp": 0.1484,
                    "is_corner_open": 0.1464,
                    "dist_last": 0.1834,
                },
            ],
            "reviewRows": [
                {
                    "region": "JPN-coded",
                    "before": "Long archive anchor: least opponent contact, fewer open-corner starts, most continuous stepping.",
                    "after": "Remains the baseline; JPN-KOR distance is essentially unchanged (0.0106 -> 0.0107).",
                    "stat": "anchor",
                },
                {
                    "region": "KOR-coded",
                    "before": "Fighting stream: more opponent contact and longer step distance than Japan-coded games.",
                    "after": "During diffusion, the fighting index rises from +0.027 in 2008-15 to +0.038 in 2018-21, then settles to +0.032.",
                    "stat": "+0.038",
                },
                {
                    "region": "CHN-coded",
                    "before": "High-mobility stream: strongest opponent contact and open-corner signal among the three.",
                    "after": "Shows the strongest convergence, with JPN-CHN 0.0195 -> 0.0071 and KOR-CHN 0.0186 -> 0.0068.",
                    "stat": "0.007",
                },
            ],
            "archive": read_archive(),
        },
        "codex": {
            "humanOverFrequency": "22/22 years",
            "histDeltaBits": 0.120,
            "recencyDeltaBits": 0.094,
            "histOverRecency": "19/22 years",
            "histOverRecencyP": 0.000428,
            "e2ToE3RecoveryBits": 0.076,
        },
    }


def main() -> None:
    SITE_DATA.mkdir(parents=True, exist_ok=True)
    payload = build_payload()
    output = "window.GAME_CODEX_DATA = " + json.dumps(
        payload, ensure_ascii=False, separators=(",", ":")
    )
    (SITE_DATA / "app-data.js").write_text(output + ";\n", encoding="utf-8")
    print(f"Wrote {SITE_DATA / 'app-data.js'}")


if __name__ == "__main__":
    main()
