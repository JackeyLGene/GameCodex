"""Generate Figure: Divine move — per-move KataGo rank + winrate trajectory."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
out_dir = ROOT / 'results' / 'figures'
os.makedirs(out_dir, exist_ok=True)

plt.rcParams.update({'font.size': 11, 'font.family': 'sans-serif',
                      'figure.dpi': 150, 'savefig.dpi': 300,
                      'savefig.bbox': 'tight'})

# Data from divine_ai_gap.py KataGo analysis output (Lee moves, every 2nd)
# Parsed directly from script output
raw = [
    (16, 99, 0.536), (18, 4, 0.523), (20, 3, 0.414), (22, 2, 0.387),
    (24, 1, 0.380), (26, 3, 0.378), (28, 0, 0.377), (30, 1, 0.376),
    (32, 1, 0.312), (34, 1, 0.292), (36, 0, 0.309), (38, 0, 0.332),
    (40, 99, 0.333), (42, 2, 0.248), (44, 99, 0.212), (46, 99, 0.136),
    (48, 1, 0.133), (50, 1, 0.136), (52, 99, 0.145), (54, 0, 0.133),
    (56, 1, 0.121), (58, 0, 0.100), (60, 1, 0.087), (62, 0, 0.039),
    (64, 1, 0.037), (66, 0, 0.021), (68, 3, 0.029), (70, 99, 0.025),
    (72, 5, 0.025), (74, 3, 0.018), (76, 0, 0.016),
    (78, 2, 0.014),   # Divine move
    (80, 1, 0.044), (82, 1, 0.027), (84, 6, 0.032), (86, 99, 0.054),
    (88, 0, 0.068), (90, 0, 0.241), (92, 0, 0.293), (94, 0, 0.692),
    (96, 1, 0.636), (98, 0, 0.879), (100, 0, 0.855), (102, 1, 0.919),
    (104, 0, 0.932), (106, 2, 0.959), (108, 0, 0.938), (110, 1, 0.964),
    (112, 1, 0.967), (114, 0, 0.976), (116, 3, 0.977), (118, 0, 0.963),
    (120, 5, 0.972), (122, 1, 0.947), (124, 0, 0.976), (126, 1, 0.986),
    (128, 0, 0.984), (130, 1, 0.985), (132, 2, 0.988), (134, 1, 0.989),
    (136, 0, 0.992), (138, 4, 0.993), (140, 0, 0.989), (142, 12, 0.989),
    (144, 1, 0.995), (146, 3, 0.996), (148, 1, 0.996), (150, 2, 0.996),
    (152, 0, 0.994), (154, 1, 0.996), (156, 0, 0.995), (158, 1, 0.996),
    (160, 2, 0.996),
]
moves = [r[0] for r in raw]
ranks = [r[1] for r in raw]
winrates = [r[2] for r in raw]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True,
                                 gridspec_kw={'height_ratios': [3, 2]})

# Panel A: KataGo policy rank (lower = more AI-like)
colors = ['#3388CC' if m <= 78 else '#FF6644' for m in moves]
ax1.bar(moves, [min(r, 30) for r in ranks], color=colors, alpha=0.7, width=1.2)
ax1.axvline(x=78, color='#222222', linewidth=2.5, linestyle='--', alpha=0.6)
ax1.set_ylabel('KataGo policy rank\n(0 = top-1, lower = more AI-like)')
ax1.set_title('Lee Sedol vs AlphaGo — Game 4 (March 13, 2016)', fontsize=13, fontweight='bold')

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#3388CC', alpha=0.7, label='Before move 78\n(mean rank = 20)'),
    Patch(facecolor='#FF6644', alpha=0.7, label='After move 78\n(mean rank = 4)'),
]
ax1.legend(handles=legend_elements, loc='upper left', fontsize=9)

# Annotation for divine move
ax1.annotate('Move 78\n"Divine Move"\nrank=2',
             xy=(78, 2), xytext=(58, 8),
             arrowprops=dict(arrowstyle='->', color='#222', lw=1.5),
             fontsize=10, fontweight='bold', color='#222',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF9C4', alpha=0.9))

# Panel B: KataGo winrate (Black's perspective = AlphaGo)
ax2.plot(moves, winrates, color='#333333', linewidth=1.5, alpha=0.8)
ax2.fill_between(moves, 0, winrates, alpha=0.15, color='#333333')
ax2.axvline(x=78, color='#222222', linewidth=2.5, linestyle='--', alpha=0.6)
ax2.set_ylabel("KataGo winrate\n(AlphaGo's perspective)")
ax2.set_xlabel('Move number')
ax2.set_ylim(0, 1.05)
ax2.axhline(y=0.5, color='gray', linestyle=':', alpha=0.3)

# Annotations for winrate
ax2.annotate('1.4%\n(AlphaGo\n98.6% confident)', xy=(78, 0.014),
             xytext=(88, 0.18), fontsize=9, color='#CC4400',
             arrowprops=dict(arrowstyle='->', color='#CC4400', lw=1.2))

ax2.annotate('99.6%', xy=(152, 0.996), xytext=(140, 0.78),
             fontsize=10, fontweight='bold', color='#226622',
             arrowprops=dict(arrowstyle='->', color='#226622', lw=1.2))

# Phase labels at top
for x_start, x_end, label, col in [
    (14, 76, 'Human-style\n(rank≈20)', '#3388CC'),
    (78, 78, '', '#222222'),
    (80, 160, 'AI-aligned\n(rank≈4)', '#FF6644'),
]:
    if x_start == 78: continue
    ax1.annotate(label, xy=((x_start+x_end)/2, 28),
                 ha='center', fontsize=9, color=col, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7))

plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'fig_divine_move_ai_gap.png'))
plt.close()
print("Divine move figure saved.")
