"""Phase 2 full: KataGo policy-rhythm alignment.

For each sampled position:
  1. Run KataGo analysis → top-k policy moves
  2. Compute rhythm features for human move AND top-1 KataGo move
  3. Compare gap across eras
  4. Test: does human-KataGo rhythm gap narrow post-AI?
"""
import csv, json, os, subprocess, statistics, math, random, time
from collections import defaultdict

random.seed(42)

SGF_COLS = 'abcdefghijklmnopqrs'
GTP_COLS = 'ABCDEFGHJKLMNOPQRST'  # no 'I'
GTP_LETTER_TO_IDX = {c: i for i, c in enumerate(GTP_COLS)}

def sgf_to_gtp(move_str):
    """Convert SGF coordinate 'pd' -> GTP 'Q4'."""
    if not move_str or len(move_str) < 2: return None
    col = SGF_COLS.find(move_str[0])
    row = SGF_COLS.find(move_str[1])
    if col < 0 or row < 0: return None
    # SGF row a=top->t=bottom, GTP row 1=bottom->19=top
    gtp_col = GTP_COLS[col]
    gtp_row = str(19 - row)
    return gtp_col + gtp_row

def sgf_to_xy(move_str):
    if not move_str or len(move_str) < 2: return None
    c = SGF_COLS.find(move_str[0])
    r = SGF_COLS.find(move_str[1])
    if c < 0 or r < 0: return None
    return (c, r)

def compute_rhythm(prefix_moves_sgf, candidate_move_sgf):
    """Compute rhythm features for a candidate move on a board from prefix."""
    BOARD_SZ = 19
    board = {}
    for color, coord in prefix_moves_sgf:
        xy = sgf_to_xy(coord)
        if xy: board[xy] = color

    tx, ty = sgf_to_xy(candidate_move_sgf)
    if (tx, ty) is None: return None
    move_color = 'B' if len(prefix_moves_sgf) % 2 == 0 else 'W'
    board[(tx, ty)] = move_color
    opp_color = 'W' if move_color == 'B' else 'B'

    # Distance to last move
    last = sgf_to_xy(prefix_moves_sgf[-1][1])
    dist_last = (math.sqrt((tx-last[0])**2 + (ty-last[1])**2) / 20.0 if last else 1.0)

    # Adjacent stones
    adj_opp = adj_own = 0
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = tx+dx, ty+dy
        if 0 <= nx < BOARD_SZ and 0 <= ny < BOARD_SZ:
            s = board.get((nx, ny))
            if s == opp_color: adj_opp += 1
            elif s == move_color: adj_own += 1

    # Corner openness
    corner_d = min(math.sqrt(tx**2+ty**2), math.sqrt(tx**2+(18-ty)**2),
                   math.sqrt((18-tx)**2+ty**2), math.sqrt((18-tx)**2+(18-ty)**2)) / 13.0
    is_corner_open = 1.0 if corner_d * 13.0 < 4 else 0.0

    # Local density
    opp_count = own_count = 0
    for (sx, sy), color in board.items():
        d = math.sqrt((tx-sx)**2 + (ty-sy)**2)
        if d <= 3:
            if color == opp_color: opp_count += 1
            elif color == move_color and (sx,sy) != (tx,ty): own_count += 1

    return {
        'dist_last': dist_last, 'adj_opp': adj_opp/4.0, 'adj_own': adj_own/4.0,
        'is_corner_open': is_corner_open, 'dens_delta': (own_count-opp_count)/10.0,
    }

# ═══ Load sampled positions ═══
parsed_csv = 'G:/GameCodex/data/parsed/go_games_parsed.csv'
positions_all = []
with open(parsed_csv, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        y = row.get('year','');
        if not y or y == 'None': continue
        year = int(y)
        if year < 2000: continue
        moves = json.loads(row.get('moves','[]'))
        if len(moves) < 40: continue
        era = 'E0' if year <= 2015 else ('E1' if year <= 2017 else ('E2' if year <= 2021 else 'E3'))
        positions_all.append({'era': era, 'year': year, 'moves': moves})

# Downsample per era
era_samples = defaultdict(list)
for p in positions_all:
    era_samples[p['era']].append(p)
MAX = 50  # pilot
sampled = []
for era in ['E0','E1','E2','E3']:
    lst = era_samples.get(era,[])
    sampled.extend(random.sample(lst, min(MAX, len(lst))))

print(f"Sampled {len(sampled)} positions ({MAX}/era target)")

# ═══ Run KataGo ═══
KATAGO = 'G:/GameCodex/data/katago/katago.exe'
CFG = 'G:/GameCodex/data/katago/analysis.cfg'
MODEL = 'G:/GameCodex/data/katago/model.bin.gz'

print("Starting KataGo analysis engine...")
proc = subprocess.Popen(
    [KATAGO, 'analysis', '-config', CFG, '-model', MODEL],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    text=True, bufsize=1)
for line in proc.stderr:
    if 'ready to begin handling requests' in line: break
print("KataGo ready.")

results = []
n_done = 0
for s in sampled:
    n_done += 1
    if n_done % 20 == 0: print(f"  {n_done}/{len(sampled)}...")

    # Convert moves to GTP
    sample_idx = 30
    prefix_moves = [(c, coord) for c, coord in s['moves'][:sample_idx]]
    actual_move_sgf = s['moves'][sample_idx][1] if len(s['moves']) > sample_idx else None
    if actual_move_sgf is None: continue

    gtp_moves = []
    for color, coord in prefix_moves:
        gtp = sgf_to_gtp(coord)
        if gtp is None: break
        gtp_moves.append([color, gtp])
    if len(gtp_moves) != sample_idx: continue

    # Query
    query = {
        'id': f'pos{n_done}', 'moves': gtp_moves,
        'rules': 'japanese', 'komi': 6.5,
        'boardXSize': 19, 'boardYSize': 19,
        'maxVisits': 100, 'includePolicy': True,
    }
    proc.stdin.write(json.dumps(query) + '\n')
    proc.stdin.flush()

    kata_data = None
    for line in proc.stdout:
        line = line.strip()
        if not line: continue
        try:
            d = json.loads(line)
            if d.get('id') == query['id']:
                kata_data = d; break
        except: continue

    if kata_data is None or 'moveInfos' not in kata_data: continue

    # Human move rhythm
    human_rhythm = compute_rhythm([(c, coord) for c, coord in prefix_moves], actual_move_sgf)
    if human_rhythm is None: continue

    # KataGo top-1 rhythm (convert GTP back to SGF for rhythm computation)
    katago_top1_gtp = kata_data['moveInfos'][0]['move']
    # GTP to SGF: Q16 -> pd
    gtp_col_letter = katago_top1_gtp[0]  # Q
    gtp_col_num = GTP_LETTER_TO_IDX.get(gtp_col_letter, -1)
    gtp_row_num = int(katago_top1_gtp[1:])  # 16
    sgf_col = SGF_COLS[gtp_col_num]  # p
    sgf_row = SGF_COLS[19 - gtp_row_num]  # d
    katago_sgf = sgf_col + sgf_row

    katago_rhythm = compute_rhythm([(c, coord) for c, coord in prefix_moves], katago_sgf)
    if katago_rhythm is None: continue

    # Rhythm gap (Euclidean distance in rhythm space)
    gap = math.sqrt(sum((human_rhythm[k] - katago_rhythm[k])**2 for k in human_rhythm))

    results.append({
        'era': s['era'], 'year': s['year'],
        'gap': gap,
        'human_rhythm': human_rhythm,
        'katago_rhythm': katago_rhythm,
        'katago_winrate': kata_data['rootInfo']['winrate'],
        'katago_top1_prior': kata_data['moveInfos'][0]['prior'],
    })

proc.stdin.close()
proc.terminate()

print(f"\nAnalyzed {len(results)} positions")

# ═══ Report ═══
print(f"\n{'='*60}")
print(f"PHASE 2: KATAGO POLICY-RHYTHM ALIGNMENT")
print(f"{'='*60}")

era_gaps = defaultdict(list)
for r in results:
    era_gaps[r['era']].append(r['gap'])

print(f"\n  Human-KataGo rhythm gap by era:")
print(f"  {'Era':<6} {'N':>4} {'Mean gap':>10} {'SD':>8}")
for era in ['E0','E1','E2','E3']:
    if era_gaps[era]:
        g = era_gaps[era]
        print(f"  {era:<6} {len(g):>4} {statistics.mean(g):>10.4f} {statistics.stdev(g):>8.4f}")

def cohen_d(a,b):
    if len(a)<2 or len(b)<2: return 0
    p = ((statistics.stdev(a)**2+statistics.stdev(b)**2)/2)**0.5
    return (statistics.mean(a)-statistics.mean(b))/max(0.001,p)

if era_gaps['E0'] and era_gaps['E3']:
    d_e0e3 = cohen_d(era_gaps['E0'], era_gaps['E3'])
    print(f"\n  d(E0 vs E3) gap = {d_e0e3:+.3f}")
    if d_e0e3 > 0.2:
        print(f"  → Human-KataGo gap NARROWED post-AI (E3 closer to KataGo)")
    elif d_e0e3 < -0.2:
        print(f"  → Human-KataGo gap WIDENED post-AI")
    else:
        print(f"  → Gap unchanged across eras")

# Feature-level comparison
print(f"\n  Rhythm feature comparison (E0 vs E3):")
feat_names = ['dist_last','adj_opp','adj_own','is_corner_open','dens_delta']
print(f"  {'Feature':<18} {'Human E0':>10} {'Human E3':>10} {'KataGo':>10} {'d(HumE0,KG)':>12} {'d(HumE3,KG)':>12}")
for feat in feat_names:
    h_e0 = [r['human_rhythm'][feat] for r in results if r['era']=='E0']
    h_e3 = [r['human_rhythm'][feat] for r in results if r['era']=='E3']
    kg_all = [r['katago_rhythm'][feat] for r in results]
    if h_e0 and h_e3 and kg_all:
        d_e0 = cohen_d(h_e0, kg_all)
        d_e3 = cohen_d(h_e3, kg_all)
        closer = 'E3 closer' if abs(d_e3)<abs(d_e0) else ('E0 closer' if abs(d_e0)<abs(d_e3) else 'same')
        print(f"  {feat:<18} {statistics.mean(h_e0):>10.4f} {statistics.mean(h_e3):>10.4f} "
              f"{statistics.mean(kg_all):>10.4f} {d_e0:>+12.3f} {d_e3:>+12.3f}  {closer}")

# Save
os.makedirs('G:/GameCodex/results/phase2', exist_ok=True)
out = 'G:/GameCodex/results/phase2/katago_alignment.csv'
with open(out, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['era','year','gap',
        'dist_last_h','adj_opp_h','adj_own_h','is_corner_open_h','dens_delta_h',
        'dist_last_kg','adj_opp_kg','adj_own_kg','is_corner_open_kg','dens_delta_kg',
        'katago_winrate','katago_top1_prior'])
    w.writeheader()
    for r in results:
        row = {'era':r['era'],'year':r['year'],'gap':r['gap'],
               'katago_winrate':r['katago_winrate'],'katago_top1_prior':r['katago_top1_prior']}
        for k in feat_names:
            row[f'{k}_h'] = r['human_rhythm'][k]
            row[f'{k}_kg'] = r['katago_rhythm'][k]
        w.writerow(row)
print(f"\nSaved: {out}")
