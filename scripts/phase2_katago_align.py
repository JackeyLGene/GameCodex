"""Phase 2: KataGo policy alignment with rhythm-axis shift.

Core test: Do KataGo's top-k policy moves share the rhythm characteristics
that shifted in Phase 1 (adj_opp, is_corner_open, dens_delta, dist_near_opp)?

If yes → the Phase 1 rhythm shift is toward AI policy = AI Codex operation.

Pipeline:
  1. Sample positions from CWI-parsed games
  2. Convert to SGF, run KataGo analysis
  3. Compute rhythm features for actual move vs KataGo top-k moves
  4. Compare: actual_move_rhythm vs top1_rhythm vs top3_rhythm
  5. By era: does the gap narrow post-AI?
"""
import csv, json, os, subprocess, tempfile, statistics, math, random
from collections import defaultdict

random.seed(42)

# ═══════════════════════════════════════════════════════════════
# 0. Load parsed game data and sample positions
# ═══════════════════════════════════════════════════════════════

parsed_csv = 'G:/GameCodex/data/parsed/go_games_parsed.csv'

# Sample positions: one position per game at move 30
positions = []
with open(parsed_csv, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        year_str = row.get('year', '')
        if not year_str or year_str == 'None': continue
        year = int(year_str)
        if year < 2000: continue

        moves = json.loads(row.get('moves', '[]'))
        if len(moves) < 40: continue

        # Sample at move 30 (opening-early midgame transition)
        # Store the first 30 moves as SGF, and the 31st as the actual move
        sample_move_idx = 30
        sample_moves = moves[:sample_move_idx]
        actual_move = moves[sample_move_idx] if len(moves) > sample_move_idx else None
        if actual_move is None: continue

        positions.append({
            'year': year,
            'era': 'E0' if year <= 2015 else ('E1' if year <= 2017 else
                   ('E2' if year <= 2021 else 'E3')),
            'prefix_moves': sample_moves,
            'actual_move': actual_move,
        })

        # Limit per era for manageable sample
        if len([p for p in positions if p['era'] == 'E0']) >= 1000:
            pass  # keep collecting other eras

# Downsample equally per era
era_samples = defaultdict(list)
for p in positions:
    era_samples[p['era']].append(p)

MAX_PER_ERA = 200  # pilot sample
sampled = []
for era in ['E0', 'E1', 'E2', 'E3']:
    era_list = era_samples.get(era, [])
    if len(era_list) > MAX_PER_ERA:
        era_list = random.sample(era_list, MAX_PER_ERA)
    sampled.extend(era_list)

print(f"Sampled {len(sampled)} positions across eras:")
for era in ['E0', 'E1', 'E2', 'E3']:
    n = len([p for p in sampled if p['era'] == era])
    print(f"  {era}: {n}")

# ═══════════════════════════════════════════════════════════════
# 1. SGF conversion for KataGo input
# ═══════════════════════════════════════════════════════════════

SGF_COLS = 'abcdefghijklmnopqrs'

def coord_to_katago(coord):
    """Convert SGF lowercase coordinates to KataGo explicit coordinates."""
    xy = sgf_to_xy(coord)
    if xy is None:
        return 'pass'
    return f'({xy[0]},{xy[1]})'

def make_analysis_query(prefix_moves, query_id='pos'):
    """Convert move list to one JSON-line query for KataGo analysis."""
    moves = []
    for color, coord in prefix_moves:
        c = 'B' if color == 'B' else 'W'
        moves.append([c, coord_to_katago(coord)])
    return json.dumps({
        'id': query_id,
        'moves': moves,
        'rules': 'tromp-taylor',
        'komi': 7.5,
        'boardXSize': 19,
        'boardYSize': 19,
        'maxVisits': 200,
        'analysisPVLen': 5,
    })

# ═══════════════════════════════════════════════════════════════
# 2. KataGo analysis runner
# ═══════════════════════════════════════════════════════════════

KATAGO = 'G:/GameCodex/data/katago/katago.exe'
MODEL = 'G:/GameCodex/data/katago/model.bin.gz'
CONFIG = 'G:/GameCodex/data/katago/analysis_config.cfg'

def create_config():
    """Create minimal analysis config for KataGo."""
    cfg = """
numAnalysisThreads = 2
nnFile = MODEL_PATH
nnCacheSizePowerOfTwo = 18
maxVisits = 200
analysisPVLen = 5
reportDuringSearchEvery = 0.5
""".replace('MODEL_PATH', MODEL.replace('\\', '/'))
    with open(CONFIG, 'w') as f:
        f.write(cfg)

def run_katago_analysis(query_text):
    """Run KataGo analysis on a position, return policy data.

    Returns list of (move_sgf, winrate, policy_prob) for top moves.
    """
    try:
        proc = subprocess.run(
            [KATAGO, 'analysis', '-config', CONFIG, '-model', MODEL],
            input=query_text + '\n',
            capture_output=True, text=True, timeout=30
        )
        # Parse JSON output
        output = proc.stdout.strip()
        if not output:
            return []

        # KataGo outputs JSON lines; last line is the analysis result
        lines = output.split('\n')
        for line in reversed(lines):
            line = line.strip()
            if line.startswith('{'):
                data = json.loads(line)
                if 'moveInfos' in data:
                    results = []
                    for mi in data['moveInfos'][:10]:
                        results.append({
                            'move': mi.get('move', ''),
                            'winrate': mi.get('winrate', 0.5),
                            'policy': mi.get('prior', 0.0),
                            'order': mi.get('order', 99),
                        })
                    return results
        return []
    except Exception as e:
        return []

# ═══════════════════════════════════════════════════════════════
# 3. Rhythm feature computation for comparison
# ═══════════════════════════════════════════════════════════════

def sgf_to_xy(move_str):
    if not move_str: return None
    move_str = str(move_str).strip()
    if move_str.lower() == 'pass': return None
    if move_str.startswith('(') and move_str.endswith(')'):
        try:
            x, y = move_str[1:-1].split(',')
            return (int(x), int(y))
        except Exception:
            return None
    if len(move_str) >= 2 and move_str[0].islower():
        c = SGF_COLS.find(move_str[0])
        r = SGF_COLS.find(move_str[1])
        if c >= 0 and r >= 0:
            return (c, r)
    # GTP coordinates, e.g. D4. I is skipped.
    col_letters = 'ABCDEFGHJKLMNOPQRST'
    col = col_letters.find(move_str[0].upper())
    if col >= 0:
        try:
            row = int(move_str[1:]) - 1
            if 0 <= row < 19:
                return (col, row)
        except Exception:
            return None
    return None

def compute_rhythm_features(prefix_moves, candidate_move):
    """For a candidate move, compute the same rhythm features as Phase 1.
    Uses a simple board representation built from prefix_moves.
    Returns just the key features that shifted in Phase 1.
    """
    BOARD_SIZE = 19
    board = {}  # (x,y) -> 'B' or 'W'

    for color, coord in prefix_moves:
        xy = sgf_to_xy(coord)
        if xy: board[xy] = color

    target_xy = sgf_to_xy(candidate_move)
    if not target_xy: return None

    tx, ty = target_xy
    move_color = 'B' if len(prefix_moves) % 2 == 0 else 'W'

    # Place candidate move
    board[target_xy] = move_color

    # Distance to last move
    last_move = prefix_moves[-1]
    last_xy = sgf_to_xy(last_move[1])
    if last_xy:
        dist_last = math.sqrt((tx - last_xy[0])**2 + (ty - last_xy[1])**2) / 20.0
    else:
        dist_last = 1.0

    # Adjacent opponent stones (normalized by 4)
    opp_color = 'W' if move_color == 'B' else 'B'
    adj_opp = 0
    adj_own = 0
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = tx + dx, ty + dy
        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
            s = board.get((nx, ny))
            if s == opp_color: adj_opp += 1
            elif s == move_color: adj_own += 1

    # Corner openness: distance to nearest corner
    corner_d = min(
        math.sqrt(tx**2 + ty**2),
        math.sqrt(tx**2 + (18-ty)**2),
        math.sqrt((18-tx)**2 + ty**2),
        math.sqrt((18-tx)**2 + (18-ty)**2),
    ) / 13.0
    is_corner_open = 1.0 if corner_d * 13.0 < 4 else 0.0

    # Opponent density (approximate — count stones within radius 3)
    opp_count = 0
    own_count = 0
    for (sx, sy), color in board.items():
        d = math.sqrt((tx - sx)**2 + (ty - sy)**2)
        if d <= 3:
            if color == opp_color: opp_count += 1
            elif color == move_color and (sx, sy) != (tx, ty): own_count += 1

    dens_delta = (own_count - opp_count) / 10.0

    return {
        'dist_last': dist_last,
        'adj_opp': adj_opp / 4.0,
        'adj_own': adj_own / 4.0,
        'is_corner_open': is_corner_open,
        'dens_delta': dens_delta,
    }

# ═══════════════════════════════════════════════════════════════
# 4. Analysis: gap between human and AI rhythm features
# ═══════════════════════════════════════════════════════════════

def run_rhythm_alignment(positions, n_max=None):
    """For each sampled position, compute rhythm features of:
    - actual human move
    - KataGo top-1 move
    Compute the gap and compare across eras.
    """
    if n_max: positions = positions[:n_max]

    results = []
    n_processed = 0

    for p in positions:
        n_processed += 1
        if n_processed % 50 == 0:
            print(f"  {n_processed}/{len(positions)}...")

        # Compute rhythm for actual human move
        human_rhythm = compute_rhythm_features(p['prefix_moves'], p['actual_move'][1])
        if human_rhythm is None: continue

        # Skip KataGo analysis for now (will be run when binary is ready)
        # For initial test: compare human rhythm vs "random legal move" baseline
        # This gives us the pipeline verification

        results.append({
            'year': p['year'], 'era': p['era'],
            **human_rhythm,
        })

    return results

# ═══════════════════════════════════════════════════════════════
# 5. Baseline: human rhythm features across eras (without KataGo)
# ═══════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print(f"PHASE 2 PILOT: Human move rhythm features across eras")
print(f"{'='*60}")

# Use the sampled positions to compute rhythm features for the ACTUAL move
# This replicates Phase 1 at a finer grain (per-position instead of per-game)
feature_names = ['dist_last', 'adj_opp', 'adj_own', 'is_corner_open', 'dens_delta']
era_feats = defaultdict(lambda: defaultdict(list))
per_position_results = []

print(f"\nComputing rhythm features for {len(sampled)} positions...")
n_done = 0
for p in sampled:
    feat = compute_rhythm_features(p['prefix_moves'], p['actual_move'][1])
    if feat is None: continue
    for k, v in feat.items():
        era_feats[p['era']][k].append(v)
    per_position_results.append({'era': p['era'], 'year': p['year'], **feat})
    n_done += 1
    if n_done % 200 == 0:
        print(f"  {n_done}/{len(sampled)}...")

print(f"\nDone: {n_done} positions computed")

# Report by era
def cohen_d(a, b):
    if len(a) < 2 or len(b) < 2: return 0
    pooled = ((statistics.stdev(a)**2 + statistics.stdev(b)**2) / 2) ** 0.5
    return (statistics.mean(a) - statistics.mean(b)) / max(0.001, pooled)

print(f"\n{'='*60}")
print(f"RHYTHM FEATURES BY ERA (per-position)")
print(f"{'='*60}")
print(f"  {'Feature':<18} {'E0':>8} {'E3':>8} {'d(E0,E3)':>10}")
print(f"  {'-'*18} {'-'*8} {'-'*8} {'-'*10}")

for feat_name in feature_names:
    e0_vals = era_feats['E0'].get(feat_name, [])
    e3_vals = era_feats['E3'].get(feat_name, [])
    if e0_vals and e3_vals:
        d_val = cohen_d(e0_vals, e3_vals)
        print(f"  {feat_name:<18} {statistics.mean(e0_vals):>8.4f} "
              f"{statistics.mean(e3_vals):>8.4f} {d_val:>+10.3f}")

# Save for later KataGo comparison
out_csv = 'G:/GameCodex/results/phase2/position_rhythm_features.csv'
os.makedirs('G:/GameCodex/results/phase2', exist_ok=True)
with open(out_csv, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['era', 'year'] + feature_names)
    w.writeheader()
    for r in per_position_results:
        w.writerow(r)
print(f"\nSaved: {out_csv}")

print(f"\n{'='*60}")
print(f"NEXT: Run KataGo analysis on these positions")
print(f"{'='*60}")
print(f"  1. Verify KataGo binary + model downloaded")
print(f"  2. Run: katago analysis on sampled positions")
print(f"  3. Compare KataGo top-k rhythm vs human actual rhythm")
print(f"  4. Test: does human-KataGo gap narrow post-AI?")
