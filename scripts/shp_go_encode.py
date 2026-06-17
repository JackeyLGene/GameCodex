"""SHP dual-axis encoding for Go moves.

Each move = (chroma, rhythm):
  chroma: lifecycle/phase position (move index, board occupancy, stage)
  rhythm: spatial relationship to existing stones (distance, density, context)

Output:
  per-move: chroma_vec, rhythm_vec
  per-game: chroma_centroid, rhythm_centroid, cross_harm
  per-year: mean cross_harm, centroid displacement

Cross-harm = chroma × rhythm — measures how lifecycle phase couples with
spatial choice. AI transition should show as re-alignment in SHP space.
"""
import csv, json, math, statistics, os
from collections import defaultdict

# ═══════════════════════════════════════════════════════════════
# 0. Minimal Go Board
# ═══════════════════════════════════════════════════════════════

SGF_COLS = 'abcdefghijklmnopqrs'  # a-t (19x19)
BOARD_SIZE = 19
EMPTY, BLACK, WHITE = 0, 1, 2

def sgf_to_xy(move_str):
    """Convert SGF coordinate 'pd' -> (col, row) 0-indexed."""
    if not move_str or len(move_str) < 2:
        return None
    c = SGF_COLS.find(move_str[0])
    r = SGF_COLS.find(move_str[1])
    if c < 0 or r < 0:
        return None
    return (c, r)

def xy_dist(p1, p2):
    """Euclidean distance between two board positions."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def xy_to_idx(x, y):
    return y * BOARD_SIZE + x

class GoBoard:
    """Minimal Go board for SHP feature extraction — no rules, just stone placement."""
    def __init__(self):
        self.board = [EMPTY] * (BOARD_SIZE * BOARD_SIZE)
        self.move_history = []  # list of (x, y, color)
        self.n_moves = 0

    def place(self, x, y, color):
        idx = xy_to_idx(x, y)
        self.board[idx] = color
        self.move_history.append((x, y, color))
        self.n_moves += 1

    def get(self, x, y):
        return self.board[xy_to_idx(x, y)]

    def occupancy(self):
        """Fraction of board occupied."""
        n_stones = sum(1 for s in self.board if s != EMPTY)
        return n_stones / 361.0

    def neighbors(self, x, y, radius=1):
        """Count stones within manhattan distance <= radius."""
        own, opp = 0, 0
        color = self.get(x, y)
        if color == EMPTY:
            return 0, 0
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                    s = self.get(nx, ny)
                    if s == color:
                        own += 1
                    elif s != EMPTY:
                        opp += 1
        return own, opp

    def local_density(self, x, y, radius=3):
        """Count own/opponent stones within radius."""
        own, opp = 0, 0
        color = self.get(x, y)
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                    d2 = dx*dx + dy*dy
                    if d2 <= radius*radius:
                        s = self.get(nx, ny)
                        if s == color:
                            own += 1
                        elif s != EMPTY:
                            opp += 1
        return own, opp

    def distance_to_nearest(self, x, y, target_color=None):
        """Distance to nearest stone of given color (or any if None)."""
        best = float('inf')
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if i == x and j == y:
                    continue
                s = self.get(i, j)
                if s == EMPTY:
                    continue
                if target_color is not None and s != target_color:
                    continue
                d = xy_dist((x, y), (i, j))
                if d < best:
                    best = d
        return best if best < float('inf') else 20.0

    def edge_distance(self, x, y):
        """Min distance to any edge."""
        return min(x, y, BOARD_SIZE - 1 - x, BOARD_SIZE - 1 - y)

    def corner_distance(self, x, y):
        """Min distance to any corner."""
        return min(xy_dist((x, y), (0, 0)),
                   xy_dist((x, y), (0, 18)),
                   xy_dist((x, y), (18, 0)),
                   xy_dist((x, y), (18, 18)))


# ═══════════════════════════════════════════════════════════════
# 1. Per-move feature extraction
# ═══════════════════════════════════════════════════════════════

def extract_move_features(board, x, y, color, move_idx, game_length=None):
    """Compute (chroma_vec, rhythm_vec) for one move.

    chroma: lifecycle position (6-dim)
    rhythm: spatial relationship (12-dim)
    """
    # ── Chroma: lifecycle/phase ──
    # move_index (raw, for within-game context)
    move_idx_raw = move_idx
    # normalized by fixed horizon (300 = typical full game length)
    move_norm_300 = min(move_idx / 300.0, 1.0)
    # board occupancy
    occ = board.occupancy()

    # Phase bucket (1-hot): opening(0-50), early_mid(51-100), mid(101-150),
    #                        late_mid(151-200), endgame(201+)
    phase_bins = [0.0] * 5
    if move_idx <= 50: phase_bins[0] = 1.0
    elif move_idx <= 100: phase_bins[1] = 1.0
    elif move_idx <= 150: phase_bins[2] = 1.0
    elif move_idx <= 200: phase_bins[3] = 1.0
    else: phase_bins[4] = 1.0

    # occupancy bin
    if occ < 0.1: occ_bin = 0
    elif occ < 0.3: occ_bin = 1
    elif occ < 0.5: occ_bin = 2
    else: occ_bin = 3

    chroma = [
        float(move_idx_raw),
        move_norm_300,
        occ,
        float(occ_bin),
        *phase_bins,
    ]

    # ── Rhythm: spatial relationship ──
    if board.n_moves >= 2:
        last_x, last_y, _ = board.move_history[-2]
        dist_to_last = xy_dist((x, y), (last_x, last_y))
    else:
        dist_to_last = 20.0

    dist_nearest_any = board.distance_to_nearest(x, y)
    dist_nearest_own = board.distance_to_nearest(x, y, color)
    opp_color = WHITE if color == BLACK else BLACK
    dist_nearest_opp = board.distance_to_nearest(x, y, opp_color)

    own_density, opp_density = board.local_density(x, y, radius=3)
    adj_own, adj_opp = board.neighbors(x, y, radius=1)

    edge_d = board.edge_distance(x, y) / 9.0  # normalize to [0, 1]
    corner_d = board.corner_distance(x, y) / 13.0  # normalize

    # Is this an "empty corner" move? (corner d < 4 and low local density)
    is_corner_open = 1.0 if (corner_d * 13.0 < 4 and own_density + opp_density < 3) else 0.0

    # Local density delta: own - opponent
    density_delta = own_density - opp_density

    rhythm = [
        dist_to_last / 20.0,
        dist_nearest_any / 20.0,
        dist_nearest_own / 20.0,
        dist_nearest_opp / 20.0,
        own_density / 10.0,
        opp_density / 10.0,
        adj_own / 4.0,
        adj_opp / 4.0,
        edge_d,
        corner_d,
        is_corner_open,
        density_delta / 10.0,
    ]

    return chroma, rhythm

# ═══════════════════════════════════════════════════════════════
# 2. Cross-harm computation
# ═══════════════════════════════════════════════════════════════

def cross_harm(chroma, rhythm):
    """Cross-harm: outer product summed, normalized.
    Measures coupling between lifecycle-phase and spatial-choice.
    """
    # Outer product, summed
    total = 0.0
    for c in chroma:
        for r in rhythm:
            total += abs(c * r)
    return total

def vector_mean(vectors):
    n = len(vectors)
    if n == 0:
        return []
    dim = len(vectors[0])
    return [sum(v[d] for v in vectors) / n for d in range(dim)]

# ═══════════════════════════════════════════════════════════════
# 3. Main pipeline
# ═══════════════════════════════════════════════════════════════

def process_game(moves_json, year):
    """Process one game: replay moves, extract SHP features per move,
    compute game-level centroids and cross-harm.
    """
    moves = json.loads(moves_json)
    board = GoBoard()
    chroma_vecs = []
    rhythm_vecs = []
    cross_harms = []

    for idx, (color_str, coord) in enumerate(moves):
        xy = sgf_to_xy(coord)
        if xy is None:
            continue
        x, y = xy

        # Place stone first to compute features (board up to this move)
        color = BLACK if color_str == 'B' else WHITE
        board.place(x, y, color)

        chroma, rhythm = extract_move_features(board, x, y, color, idx + 1)
        ch = cross_harm(chroma, rhythm)

        chroma_vecs.append(chroma)
        rhythm_vecs.append(rhythm)
        cross_harms.append(ch)

    if not chroma_vecs:
        return None

    return {
        'year': year,
        'n_moves': len(chroma_vecs),
        'chroma_centroid': vector_mean(chroma_vecs),
        'rhythm_centroid': vector_mean(rhythm_vecs),
        'mean_cross_harm': statistics.mean(cross_harms),
        'sd_cross_harm': statistics.stdev(cross_harms) if len(cross_harms) > 1 else 0.0,
    }

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='G:/GameCodex/data/parsed/go_games_parsed.csv')
    parser.add_argument('--out', default='G:/GameCodex/results')
    parser.add_argument('--max-games', type=int, default=0, help='Limit games (0=all)')
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    print("Loading parsed games...")
    games_by_year = defaultdict(list)
    with open(args.input, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            year_str = row.get('year', '')
            if not year_str or year_str == 'None':
                continue
            year = int(year_str)
            if year < 2000:
                continue  # focus on E0-E3
            moves = row.get('moves', '[]')
            if moves == '[]':
                continue
            games_by_year[year].append(moves)
            if args.max_games > 0 and sum(len(v) for v in games_by_year.values()) >= args.max_games:
                break

    total_games = sum(len(v) for v in games_by_year.values())
    print(f"Loaded {total_games} games across {len(games_by_year)} years (2000+)")

    # Process each game
    print("Extracting SHP features...")
    year_results = defaultdict(list)  # year -> [game_results]

    n_processed = 0
    for year in sorted(games_by_year.keys()):
        for moves_json in games_by_year[year]:
            result = process_game(moves_json, year)
            if result:
                year_results[year].append(result)
                n_processed += 1
                if n_processed % 5000 == 0:
                    print(f"  {n_processed}/{total_games} games...")
    print(f"  Done: {n_processed} games processed")

    # ══ Year-level aggregation ══
    print("\nAggregating by year...")
    annual = []
    for year in sorted(year_results.keys()):
        results = year_results[year]
        n = len(results)
        ch_vals = [r['mean_cross_harm'] for r in results]

        # Mean chroma centroid
        chroma_cents = [r['chroma_centroid'] for r in results]
        chroma_mean = vector_mean(chroma_cents)

        rhythm_cents = [r['rhythm_centroid'] for r in results]
        rhythm_mean = vector_mean(rhythm_cents)

        annual.append({
            'year': year,
            'n_games': n,
            'mean_cross_harm': statistics.mean(ch_vals),
            'sd_cross_harm': statistics.stdev(ch_vals) if n > 1 else 0,
            'chroma_mean': chroma_mean,
            'rhythm_mean': rhythm_mean,
        })

    # Save annual summary
    out_csv = os.path.join(args.out, 'shp_annual.csv')
    with open(out_csv, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['year', 'n_games', 'mean_cross_harm',
                                           'sd_cross_harm', 'chroma_mean', 'rhythm_mean'])
        w.writeheader()
        for a in annual:
            a['chroma_mean'] = json.dumps(a['chroma_mean'])
            a['rhythm_mean'] = json.dumps(a['rhythm_mean'])
            w.writerow(a)
    print(f"\nSaved annual summary: {out_csv}")

    # ══ Era comparison ══
    print(f"\n{'='*60}")
    print(f"SHP CROSS-HARM BY ERA")
    print(f"{'='*60}")
    eras = {'E0': (2000, 2015), 'E1': (2016, 2017), 'E2': (2018, 2021), 'E3': (2022, 2026)}
    era_stats = {}
    for era, (y0, y1) in eras.items():
        era_results = [r for y, rs in year_results.items() if y0 <= y <= y1 for r in rs]
        if not era_results:
            continue
        ch = [r['mean_cross_harm'] for r in era_results]
        era_stats[era] = {'mean': statistics.mean(ch), 'sd': statistics.stdev(ch), 'n': len(ch)}
        print(f"  {era} ({y0}-{y1}): mean_cross_harm = {era_stats[era]['mean']:.4f} "
              f"(sd={era_stats[era]['sd']:.4f}, n={era_stats[era]['n']})")

    # E0 -> E3 displacement
    if 'E0' in era_stats and 'E3' in era_stats:
        delta = era_stats['E3']['mean'] - era_stats['E0']['mean']
        print(f"\n  Δ(E3 - E0) = {delta:+.4f}")
        if abs(delta) > 0.01:
            print(f"  → SHP cross-harm SHIFT detected across AI transition.")

    # ══ Save game-level cross-harm for later held-out ══
    out_game = os.path.join(args.out, 'shp_game_level.csv')
    with open(out_game, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['year', 'mean_cross_harm', 'n_moves'])
        for year in sorted(year_results.keys()):
            for r in year_results[year]:
                w.writerow([r['year'], r['mean_cross_harm'], r['n_moves']])
    print(f"Saved game-level: {out_game}")

if __name__ == '__main__':
    main()
