"""Figure 0: Two AlphaGo Encounters As Microcosm — paired vignette.

Left: Lee Sedol 2016 (phase-transition into AI alignment)
Right: Ke Jie 2017 (already aligned, still lost)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
out_dir = ROOT / 'results' / 'figures'
os.makedirs(out_dir, exist_ok=True)

plt.rcParams.update({'font.size': 10, 'font.family': 'sans-serif',
                      'figure.dpi': 150, 'savefig.dpi': 300,
                      'savefig.bbox': 'tight'})

fig, axes = plt.subplots(2, 2, figsize=(14, 8))

# ═══ LEE SEDOL (Left column) ═══
lee_raw = [
    (16,99,0.536),(18,4,0.523),(20,3,0.414),(22,2,0.387),(24,1,0.380),
    (26,3,0.378),(28,0,0.377),(30,1,0.376),(32,1,0.312),(34,1,0.292),
    (36,0,0.309),(38,0,0.332),(40,99,0.333),(42,2,0.248),(44,99,0.212),
    (46,99,0.136),(48,1,0.133),(50,1,0.136),(52,99,0.145),(54,0,0.133),
    (56,1,0.121),(58,0,0.100),(60,1,0.087),(62,0,0.039),(64,1,0.037),
    (66,0,0.021),(68,3,0.029),(70,99,0.025),(72,5,0.025),(74,3,0.018),
    (76,0,0.016),
    (78,2,0.014),  # Divine move
    (80,1,0.044),(82,1,0.027),(84,6,0.032),(86,99,0.054),(88,0,0.068),
    (90,0,0.241),(92,0,0.293),(94,0,0.692),(96,1,0.636),(98,0,0.879),
    (100,0,0.855),(102,1,0.919),(104,0,0.932),(106,2,0.959),(108,0,0.938),
    (110,1,0.964),(112,1,0.967),(114,0,0.976),(116,3,0.977),(118,0,0.963),
    (120,5,0.972),(122,1,0.947),(124,0,0.976),(126,1,0.986),(128,0,0.984),
    (130,1,0.985),(132,2,0.988),(134,1,0.989),(136,0,0.992),(138,4,0.993),
    (140,0,0.989),(142,12,0.989),(144,1,0.995),(146,3,0.996),(148,1,0.996),
    (150,2,0.996),(152,0,0.994),(154,1,0.996),(156,0,0.995),(158,1,0.996),
    (160,2,0.996),
]

# ═══ KE JIE (Right column) ═══
# Retrospective KataGo trace, every second Ke Jie move starting at move 16.
kj_raw = [
    (16,0,0.434),(18,0,0.438),(20,6,0.450),(22,1,0.451),(24,0,0.427),
    (26,3,0.433),(28,0,0.445),(30,2,0.446),(32,0,0.423),(34,0,0.490),
    (36,0,0.512),(38,2,0.489),(40,0,0.488),(42,2,0.476),(44,0,0.484),
    (46,0,0.488),(48,0,0.512),(50,0,0.484),(52,1,0.468),(54,1,0.493),
    (56,0,0.522),(58,3,0.488),(60,1,0.487),
    # midgame
    (62,0,0.743),(64,0,0.717),(66,0,0.758),(68,1,0.753),(70,0,0.787),
    (72,2,0.794),(74,3,0.811),(76,1,0.794),(78,8,0.799),(80,4,0.832),
    (82,0,0.824),(84,0,0.820),(86,0,0.835),(88,6,0.800),(90,0,0.816),
    (92,1,0.793),(94,0,0.808),(96,0,0.834),(98,0,0.827),(100,0,0.837),
    (102,9,0.838),(104,0,0.861),(106,0,0.859),(108,0,0.893),(110,0,0.902),
    (112,5,0.925),(114,0,0.949),(116,0,0.936),(118,1,0.970),(120,0,0.958),
    # endgame
    (122,0,0.983),(124,1,0.983),(126,0,0.984),(128,0,0.985),(130,0,0.989),
    (132,0,0.991),(134,1,0.991),(136,1,0.993),(138,0,0.995),(140,11,0.993),
    (142,14,0.995),(144,0,0.997),(146,0,0.996),(148,0,0.997),(150,10,0.997),
    (152,0,0.998),(154,0,0.997),
]

def plot_player(ax_rank, ax_wr, raw_data, title, highlight_x=None,
                color_main='#3388CC', invert_winrate=False):
    moves = [r[0] for r in raw_data]
    ranks = [r[1] for r in raw_data]
    winrates = [1.0 - r[2] if invert_winrate else r[2] for r in raw_data]

    # Rank (clipped at 15 for visibility)
    colors_rank = [color_main if m <= (highlight_x or 999) else '#FF6644' for m in moves]
    ax_rank.bar(moves, [min(r, 15) for r in ranks], color=colors_rank,
                alpha=0.7, width=1.2)
    if highlight_x:
        ax_rank.axvline(x=highlight_x, color='#222', linewidth=2, linestyle='--', alpha=0.5)

    ax_rank.set_ylabel('KataGo policy rank\n(0 = top-1, lower = more AI-like)')
    ax_rank.set_ylim(0, 18)
    ax_rank.set_title(title, fontsize=12, fontweight='bold')

    # Winrate
    ax_wr.plot(moves, winrates, color='#333', linewidth=1.5, alpha=0.8)
    ax_wr.fill_between(moves, 0, winrates, alpha=0.12, color='#333')
    if highlight_x:
        ax_wr.axvline(x=highlight_x, color='#222', linewidth=2, linestyle='--', alpha=0.5)
    ax_wr.axhline(y=0.5, color='gray', linestyle=':', alpha=0.3)
    ax_wr.set_ylabel('KataGo winrate\n(human perspective)')
    ax_wr.set_xlabel('Move number')
    ax_wr.set_ylim(0, 1.05)

# Lee Sedol (Left)
plot_player(axes[0,0], axes[1,0], lee_raw,
            'Lee Sedol vs AlphaGo, 2016\nGame 4, March 13',
            highlight_x=78)

# Annotations for Lee
axes[0,0].annotate('Move 78\n"Divine Move"\nrank=2 (top-3)',
            xy=(78, 2), xytext=(48, 10),
            arrowprops=dict(arrowstyle='->', color='#222', lw=1.3),
            fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF9C4', alpha=0.9))

axes[0,0].annotate('rank≈20\n(low AI-alignment)',
            xy=(45, 20), fontsize=8, color='#3388CC',
            ha='center', fontstyle='italic')

axes[0,0].annotate('rank≈4\n(high AI-alignment)',
            xy=(120, 3), fontsize=8, color='#FF6644',
            ha='center', fontstyle='italic')

axes[1,0].annotate('1.4%\nwinrate at\nmove 78', xy=(78, 0.014),
            xytext=(90, 0.25), fontsize=8, color='#CC4400',
            arrowprops=dict(arrowstyle='->', color='#CC4400', lw=1))

axes[1,0].annotate('99.6%', xy=(152, 0.996),
            xytext=(140, 0.72), fontsize=9, fontweight='bold', color='#226622',
            arrowprops=dict(arrowstyle='->', color='#226622', lw=1.2))

# Ke Jie (Right)
plot_player(axes[0,1], axes[1,1], kj_raw,
            'Ke Jie vs AlphaGo Master, 2017\nFuture of Go Summit, Game 1',
            highlight_x=None, color_main='#44AA66', invert_winrate=True)

# Annotations for Ke Jie
axes[0,1].annotate('rank≈1.4\n(61% top-1;\nhigh alignment)',
            xy=(80, 4), fontsize=9, color='#44AA66',
            ha='center', fontstyle='italic', fontweight='bold')

axes[1,1].annotate('near even', xy=(16, 0.566),
            xytext=(25, 0.35), fontsize=8, color='#CC4400',
            arrowprops=dict(arrowstyle='->', color='#CC4400', lw=0.8))

axes[1,1].annotate('0.3%', xy=(154, 0.003),
            xytext=(130, 0.22), fontsize=9, fontweight='bold', color='#CC4400',
            arrowprops=dict(arrowstyle='->', color='#CC4400', lw=1.2))

# Summary boxes
axes[0,0].text(0.02, 0.98, 'Phase-transition\ninto AI-alignment',
               transform=axes[0,0].transAxes, fontsize=9, va='top',
               bbox=dict(boxstyle='round', facecolor='#FFF9C4', alpha=0.8))
axes[0,1].text(0.02, 0.98, 'Already AI-aligned\nfrom the start',
               transform=axes[0,1].transAxes, fontsize=9, va='top',
               bbox=dict(boxstyle='round', facecolor='#DFFFDF', alpha=0.8))

plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'fig0_paired_vignette.png'))
plt.close()

trace_path = os.path.join(out_dir, 'fig0_paired_vignette_trace.csv')
with open(trace_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'game', 'move_number', 'policy_rank_zero_indexed',
        'raw_katago_winrate', 'raw_winrate_perspective',
        'human_perspective_winrate'
    ])
    writer.writeheader()
    for move, rank, wr in lee_raw:
        writer.writerow({
            'game': 'Lee Sedol vs AlphaGo Game 4',
            'move_number': move,
            'policy_rank_zero_indexed': rank,
            'raw_katago_winrate': wr,
            'raw_winrate_perspective': 'human',
            'human_perspective_winrate': wr,
        })
    for move, rank, wr in kj_raw:
        writer.writerow({
            'game': 'Ke Jie vs AlphaGo Master Game 1',
            'move_number': move,
            'policy_rank_zero_indexed': rank,
            'raw_katago_winrate': wr,
            'raw_winrate_perspective': 'alphago',
            'human_perspective_winrate': 1.0 - wr,
        })
print("Paired vignette figure saved.")
