"""Phase 1 Pilot: Walk Lichess opening tree via Opening Explorer API.

Builds an opening Codex from the Lichess database:
  - Tree of positions → next moves → frequency/win-rate/rating
  - ECO code assignment
  - Time-period stratification (pre-2020 vs post-2020)

Output: opening_tree.json — structured position tree
        eco_summary.csv — per-ECO statistics
"""
import json, time, urllib.request, urllib.parse, os, csv, statistics
from collections import defaultdict, Counter

BASE_URL = "https://explorer.lichess.ovh/lichess"
REQUEST_DELAY = 0.3  # be polite

OUT_DIR = "G:/GameCodex/data"
os.makedirs(OUT_DIR, exist_ok=True)

def query_position(play_moves=None, since=None, until=None,
                   speeds=None, ratings=None):
    """Query the Lichess opening explorer for a position.

    play_moves: list of UCI moves from start, e.g. ['e2e4', 'e7e5']
    Returns: dict with 'white','draws','black','moves','opening','averageRating'
    """
    params = {}
    if play_moves:
        params['play'] = ','.join(play_moves)
    if since:
        params['since'] = since
    if until:
        params['until'] = until
    if speeds:
        params['speeds[]'] = speeds
    if ratings:
        params['ratings[]'] = ratings

    url = BASE_URL + '?' + urllib.parse.urlencode(params, doseq=True)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'game_codex/0.1'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"  API error: {e}")
        return None

def walk_tree(max_depth=8, top_n=5, since=None, until=None,
              speeds=None, ratings=None):
    """Walk the opening tree BFS, collecting position stats.

    Returns: list of position dicts, each with:
      - depth, fen, eco, moves_info, total_games
    """
    visited = set()
    positions = []
    queue = [([], 0)]  # (move_list, depth)

    while queue:
        moves, depth = queue.pop(0)
        if depth > max_depth:
            continue

        # Query
        data = query_position(moves, since=since, until=until,
                              speeds=speeds, ratings=ratings)
        time.sleep(REQUEST_DELAY)

        if not data:
            continue

        total = data.get('white', 0) + data.get('draws', 0) + data.get('black', 0)
        eco = data.get('opening', {})
        eco_code = eco.get('eco', '?') if eco else '?'

        pos_info = {
            'depth': depth,
            'moves': moves,
            'uci_path': ','.join(moves) if moves else 'start',
            'total_games': total,
            'white_wins': data.get('white', 0),
            'draws': data.get('draws', 0),
            'black_wins': data.get('black', 0),
            'avg_rating': data.get('averageRating', 0),
            'eco': eco_code,
            'eco_name': eco.get('name', '?') if eco else '?',
            'top_moves': [],
        }

        # Process top moves
        api_moves = data.get('moves', [])
        for m in api_moves[:top_n]:
            pos_info['top_moves'].append({
                'uci': m['uci'],
                'san': m.get('san', m['uci']),
                'white': m.get('white', 0),
                'draws': m.get('draws', 0),
                'black': m.get('black', 0),
                'total': m.get('white', 0) + m.get('draws', 0) + m.get('black', 0),
                'avg_rating': m.get('averageRating', 0),
            })

        positions.append(pos_info)

        # Enqueue children
        for m in api_moves[:top_n]:
            child_moves = moves + [m['uci']]
            key = ','.join(child_moves)
            if key not in visited:
                visited.add(key)
                queue.append((child_moves, depth + 1))

        # Show progress
        if len(positions) % 50 == 0:
            print(f"  Visited {len(positions)} positions, queue={len(queue)}")

    return positions

# ═══════════════════════════════════════════════════════════════
# Run: collect opening tree for two time periods
# ═══════════════════════════════════════════════════════════════

print("=" * 60)
print("PHASE 1: LICHESS OPENING TREE EXPLORATION")
print("=" * 60)

# Period 1: pre-2020 (since 2012, until 2019-12)
print("\n[1/3] Collecting pre-2020 opening tree...")
pre2020 = walk_tree(
    max_depth=8, top_n=5,
    since='2012-01', until='2019-12',
    speeds=['blitz', 'rapid'],
    ratings=['2000', '2200', '2500']
)
print(f"  Pre-2020: {len(pre2020)} positions")

# Period 2: post-2020
print("\n[2/3] Collecting post-2020 opening tree...")
post2020 = walk_tree(
    max_depth=8, top_n=5,
    since='2020-01', until='2026-06',
    speeds=['blitz', 'rapid'],
    ratings=['2000', '2200', '2500']
)
print(f"  Post-2020: {len(post2020)} positions")

# Combined (all time)
print("\n[3/3] Collecting all-time opening tree...")
all_time = walk_tree(
    max_depth=8, top_n=5,
    speeds=['blitz', 'rapid'],
    ratings=['2000', '2200', '2500']
)
print(f"  All-time: {len(all_time)} positions")

# ═══════════════════════════════════════════════════════════════
# Save
# ═══════════════════════════════════════════════════════════════

print("\n=== Saving ===")

with open(os.path.join(OUT_DIR, 'opening_tree_pre2020.json'), 'w') as f:
    json.dump(pre2020, f, indent=2)
with open(os.path.join(OUT_DIR, 'opening_tree_post2020.json'), 'w') as f:
    json.dump(post2020, f, indent=2)
with open(os.path.join(OUT_DIR, 'opening_tree_all.json'), 'w') as f:
    json.dump(all_time, f, indent=2)

# ECO summary
def eco_summary(positions, name):
    eco_stats = defaultdict(lambda: {'total_games': 0, 'n_positions': 0})
    for p in positions:
        eco = p['eco']
        eco_stats[eco]['total_games'] += p['total_games']
        eco_stats[eco]['n_positions'] += 1

    rows = []
    for eco, s in sorted(eco_stats.items(), key=lambda x: -x[1]['total_games']):
        rows.append({'eco': eco, 'name': name, **s})
    return rows

eco_all = eco_summary(all_time, 'all')
eco_pre = eco_summary(pre2020, 'pre2020')
eco_post = eco_summary(post2020, 'post2020')

with open(os.path.join(OUT_DIR, 'eco_summary.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['eco', 'name', 'total_games', 'n_positions'])
    w.writeheader()
    for row in eco_all + eco_pre + eco_post:
        w.writerow(row)

print(f"Saved to {OUT_DIR}/")
print(f"  opening_tree_pre2020.json  ({len(pre2020)} positions)")
print(f"  opening_tree_post2020.json ({len(post2020)} positions)")
print(f"  opening_tree_all.json      ({len(all_time)} positions)")
print(f"  eco_summary.csv")

# Quick summary
print(f"\n=== Quick Summary ===")
for label, data in [('All-time', all_time), ('Pre-2020', pre2020), ('Post-2020', post2020)]:
    total_g = sum(p['total_games'] for p in data)
    avg_rating = statistics.mean([p['avg_rating'] for p in data if p['avg_rating'] > 0]) if data else 0
    top_eco = Counter(p['eco'] for p in data).most_common(5)
    print(f"\n  {label}:")
    print(f"    Positions: {len(data)}")
    print(f"    Total games: {total_g:,}")
    print(f"    Mean rating: {avg_rating:.0f}")
    print(f"    Top ECO: {', '.join(f'{e}({c})' for e,c in top_eco)}")

