"""Phase 1 Pilot: Minimal Codex operation test using python-chess.

Self-contained: generates synthetic opening games, builds Codex,
tests held-out prediction. No external data required.

Design:
  1. Generate N games that follow ECO opening lines with controlled noise
  2. Split chronologically: T1 (training) vs T2 (test)
  3. Build Codex from T1: position -> move frequency
  4. Predict T2 move choices; compare with baselines
  5. Measure: does historical Codex improve prediction?

Baselines:
  - Uniform: all legal moves equally likely
  - Frequency: most common move in T1 (no position context)
  - Codex: position-specific frequency from T1

If Codex > Frequency, the position context matters = Codex operation.
"""
import chess, chess.pgn, random, math, io
from collections import defaultdict, Counter

random.seed(42)

# ═══════════════════════════════════════════════════════════════
# 1. Define ECO opening lines (top 20 most common openings)
# ═══════════════════════════════════════════════════════════════

# Each ECO line is a (code, name, UCI move sequence)
ECO_LINES = [
    ("B50", "Sicilian", "e2e4 c7c5"),
    ("B30", "Sicilian Rossolimo", "e2e4 c7c5 g1f3 b8c6 f1b5"),
    ("B90", "Sicilian Najdorf", "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 a7a6"),
    ("C50", "Italian", "e2e4 e7e5 g1f3 b8c6 f1c4"),
    ("C54", "Italian Giuoco Piano", "e2e4 e7e5 g1f3 b8c6 f1c4 f8c5"),
    ("C60", "Ruy Lopez", "e2e4 e7e5 g1f3 b8c6 f1b5"),
    ("C88", "Ruy Lopez Closed", "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6"),
    ("B12", "Caro-Kann", "e2e4 c7c6"),
    ("B19", "Caro-Kann Classical", "e2e4 c7c6 d2d4 d7d5 b1c3 d5e4 c3e4 f8f5"),
    ("C00", "French", "e2e4 e7e6"),
    ("C11", "French Classical", "e2e4 e7e6 d2d4 d7d5 b1c3 g8f6"),
    ("D00", "Queen's Pawn", "d2d4 d7d5"),
    ("D06", "Queen's Gambit", "d2d4 d7d5 c2c4"),
    ("D37", "QGD", "d2d4 d7d5 c2c4 e7e6 b1c3 g8f6"),
    ("E00", "Catalan", "d2d4 g8f6 c2c4 e7e6 g2g3"),
    ("A00", "English", "c2c4"),
    ("A20", "English Symmetrical", "c2c4 c7c5"),
    ("A40", "Modern", "d2d4 g7g6"),
    ("A45", "Trompowsky", "d2d4 g8f6 c1g5"),
    ("A80", "Dutch", "d2d4 f7f5"),
]

def eco_line_to_board(moves_str):
    """Parse a UCI move string to a board+move sequence."""
    board = chess.Board()
    moves = []
    for uci in moves_str.split():
        move = chess.Move.from_uci(uci)
        moves.append(uci)
        board.push(move)
    return board, moves

# ═══════════════════════════════════════════════════════════════
# 2. Generate synthetic games with noise
# ═══════════════════════════════════════════════════════════════

def generate_games(n_games, noise_level=0.3):
    """Generate games following ECO lines with controlled noise.

    Parameters:
      n_games: total games to generate
      noise_level: probability of deviating from ECO line at each move

    Returns: list of (game_id, move_sequence, positions_seen)
    """
    games = []
    for i in range(n_games):
        # Pick a random ECO line weighted by popularity
        eco_idx = random.choices(range(len(ECO_LINES)),
                                  weights=[20, 8, 15, 12, 5, 10, 5, 8, 3,
                                           12, 5, 15, 10, 8, 5, 8, 3, 5, 3, 3],
                                  k=1)[0]
        eco_code, eco_name, moves_str = ECO_LINES[eco_idx]

        _, eco_moves = eco_line_to_board(moves_str)  # validate only
        board = chess.Board()  # fresh board for each game
        positions = []
        game_moves = []

        # Play through the ECO line
        for move_uci in eco_moves:
            fen_before = board.fen()
            positions.append((fen_before, board.turn))

            # Check if ECO move is legal in current position
            eco_move = chess.Move.from_uci(move_uci)
            if eco_move not in board.legal_moves:
                break  # ECO line invalid for current position

            # Occasionally deviate (noise)
            if random.random() < noise_level and len(list(board.legal_moves)) > 1:
                legal = list(board.legal_moves)
                legal.remove(eco_move)
                if legal:
                    move = random.choice(legal)
                    game_moves.append(move.uci())
                    board.push(move)
                    positions.append((board.fen(), board.turn))
                    break  # Stop following ECO line after deviation
                else:
                    game_moves.append(move_uci)
                    board.push(eco_move)
            else:
                game_moves.append(move_uci)
                board.push(eco_move)

        # Continue with random legal moves after ECO line ends or deviates
        for _ in range(random.randint(5, 20)):
            legal = list(board.legal_moves)
            if not legal or board.is_game_over():
                break
            # Weighted: 70% pick common/central moves, 30% random
            move = random.choice(legal)
            game_moves.append(move.uci())
            positions.append((board.fen(), board.turn))
            board.push(move)

        games.append({
            'id': i,
            'moves': game_moves,
            'positions': positions,
            'eco': eco_code,
            'eco_name': eco_name,
        })

    return games

# ═══════════════════════════════════════════════════════════════
# 3. Build Codex from training set
# ═══════════════════════════════════════════════════════════════

def build_codex(games, max_positions=5000):
    """Build opening Codex: move-sequence-prefix -> next-move frequency.

    Key = first N moves as UCI string. This is how real opening books work:
    the same sequence of moves defines a position, regardless of FEN.
    """
    codex = defaultdict(Counter)
    for g in games:
        for n in range(1, min(len(g['moves']), 12)):
            prefix = ','.join(g['moves'][:n])
            if n < len(g['moves']):
                next_move = g['moves'][n]
                codex[prefix][next_move] += 1
                codex[prefix]['_total'] += 1

    return dict(codex)

# ═══════════════════════════════════════════════════════════════
# 4. Held-out evaluation
# ═══════════════════════════════════════════════════════════════

def evaluate_prediction(games_train, games_test, top_n_positions=200):
    """Test whether Codex improves held-out move prediction.

    For each position in test set that appears in training:
      - Uniform baseline: 1/N legal moves
      - Frequency baseline: most common move globally in training
      - Codex: position-specific move frequency from training

    Metric: negative log-likelihood of test moves under each model.
    Lower = better prediction.
    """
    # Build Codex from training
    codex = build_codex(games_train)

    # Global move frequency (position-independent baseline)
    global_freq = Counter()
    for g in games_train:
        for m in g['moves']:
            global_freq[m] += 1
    global_total = sum(global_freq.values())

    uniform_nll = []
    freq_nll = []
    codex_nll = []
    n_positions = 0

    for g in games_test:
        for fen, turn in g['positions']:
            n_positions += 1
            if n_positions > top_n_positions:
                break

            # Get the actual move played in test
            # We need to reconstruct: find the game's move at this position
            # Simplified: use the move from test game at corresponding index
            # For now, use a sampling approach

        if n_positions > top_n_positions:
            break

    # Redo with proper move matching
    uniform_nll = []
    freq_nll = []
    codex_nll = []
    n_predictions = 0

    for g in games_test:
        board = chess.Board()
        for i, move_uci in enumerate(g['moves']):
            if i >= len(g['positions']):
                break

            fen_before = board.fen()
            turn = board.turn
            legal_moves = list(board.legal_moves)
            n_legal = len(legal_moves)
            if n_legal == 0:
                break

            actual_move = chess.Move.from_uci(move_uci)

            # Uniform baseline
            p_uniform = 1.0 / n_legal
            uniform_nll.append(-math.log2(p_uniform))

            # Global frequency baseline
            p_freq = global_freq.get(move_uci, 1) / max(1, global_total)
            p_freq = max(0.001, min(0.999, p_freq))
            freq_nll.append(-math.log2(p_freq))

            # Codex baseline: move-sequence-prefix -> next move frequency
            prefix = ','.join(g['moves'][:i])
            if prefix in codex and move_uci in codex[prefix] and codex[prefix]['_total'] >= 3:
                p_codex = codex[prefix][move_uci] / codex[prefix]['_total']
                p_codex = max(0.001, min(0.999, p_codex))
            else:
                # Fallback: use global frequency as prior
                p_codex = global_freq.get(move_uci, 1) / max(1, global_total)
                p_codex = max(0.001, min(0.999, p_codex))
            codex_nll.append(-math.log2(p_codex))

            # Only evaluate opening phase (first 10 moves)
            if i >= 10:
                break

            board.push(actual_move)
            n_predictions += 1

    return {
        'uniform': statistics.mean(uniform_nll) if uniform_nll else 0,
        'freq': statistics.mean(freq_nll) if freq_nll else 0,
        'codex': statistics.mean(codex_nll) if codex_nll else 0,
        'n_predictions': n_predictions,
        'n_positions_in_codex': len(codex),
    }

import statistics

# ═══════════════════════════════════════════════════════════════
# 5. Run experiment
# ═══════════════════════════════════════════════════════════════

print("=" * 60)
print("PHASE 1 PILOT: CODEX OPERATION — SYNTHETIC OPENING DATA")
print("=" * 60)

# Generate data
print("\n[1] Generating synthetic games...")
all_games = generate_games(n_games=2000, noise_level=0.25)
train_games = all_games[:1000]
test_games = all_games[1000:]
print(f"  Training: {len(train_games)} games")
print(f"  Test:     {len(test_games)} games")

# Build Codex
print("\n[2] Building opening Codex from training set...")
codex = build_codex(train_games)
print(f"  Codex entries: {len(codex)}")

# Evaluate
print("\n[3] Held-out prediction...")
result = evaluate_prediction(train_games, test_games)

print(f"\n{'='*60}")
print(f"RESULTS")
print(f"{'='*60}")
print(f"  Predictions made: {result['n_predictions']}")
print(f"  Codex size: {result['n_positions_in_codex']} positions")
print(f"")
print(f"  Bits per move (lower = better prediction):")
print(f"    Uniform baseline:    {result['uniform']:.3f}")
print(f"    Global frequency:    {result['freq']:.3f}")
print(f"    Position Codex:      {result['codex']:.3f}")
print(f"")

delta_freq = result['uniform'] - result['freq']
delta_codex = result['freq'] - result['codex']
delta_uniform = result['uniform'] - result['codex']

print(f"  Δ(Uniform -> Freq):  {delta_freq:+.3f} bits")
print(f"  Δ(Freq -> Codex):    {delta_codex:+.3f} bits")
print(f"  Δ(Uniform -> Codex): {delta_uniform:+.3f} bits")
print(f"")

if delta_codex > 0:
    print(f"  Codex > Frequency: position context improves prediction.")
    print(f"  -> Codex operation signal detected in synthetic data.")
else:
    print(f"  Codex <= Frequency: position context does NOT improve.")
    print(f"  -> Check experimental setup or noise level.")

# Vary noise level
print(f"\n{'='*60}")
print(f"NOISE SENSITIVITY")
print(f"{'='*60}")
print(f"  {'Noise':>8} {'Uniform':>10} {'Freq':>10} {'Codex':>10} {'Δ(Codex)':>10}")
for noise in [0.1, 0.2, 0.3, 0.4, 0.5]:
    g_all = generate_games(2000, noise)
    r = evaluate_prediction(g_all[:1000], g_all[1000:])
    d = r['freq'] - r['codex']
    print(f"  {noise:>8.1f} {r['uniform']:>10.3f} {r['freq']:>10.3f} "
          f"{r['codex']:>10.3f} {d:>+10.3f}")
