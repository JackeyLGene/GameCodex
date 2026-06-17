"""Generate SI figures S1, S2, S3."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
out_dir = ROOT / 'results' / 'figures'
os.makedirs(out_dir, exist_ok=True)
plt.rcParams.update({'font.size': 10, 'font.family': 'sans-serif',
                      'figure.dpi': 150, 'savefig.dpi': 200,
                      'savefig.bbox': 'tight'})

# S1: KataGo feature-level selective convergence
fig, ax = plt.subplots(figsize=(7, 5))
features = ['adj_opp', 'adj_own', 'dens_delta', 'dist_last', 'is_corner_open']
d_e0 = [-0.220, -0.209, +0.216, -0.240, +0.061]
d_e3 = [-0.016, +0.007, -0.043, -0.444, -0.337]
x = np.arange(len(features)); w = 0.35
ax.bar(x-w/2, d_e0, w, label='E0 (pre-AI)', color='#3388CC', alpha=0.8, edgecolor='white')
ax.bar(x+w/2, d_e3, w, label='E3 (post-AI)', color='#FF6644', alpha=0.8, edgecolor='white')
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.set_xticks(x); ax.set_xticklabels(features)
ax.set_ylabel("Cohen's d (human-KataGo gap)")
ax.set_title('S1: KataGo feature-level selective convergence')
ax.legend(fontsize=9)
for i in range(len(features)):
    if abs(d_e3[i]) < abs(d_e0[i]):
        ax.annotate('closer', (i, d_e3[i]), textcoords="offset points",
                     xytext=(0, -15), ha='center', fontsize=7, color='#CC0000')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'figS1_katago_alignment.png'))
plt.close()

# S2: Prefix-length robustness
fig, ax = plt.subplots(figsize=(7, 5))
eras = ['pre-1980', '1980-1999', '2000-2015', '2016+']
prefix10 = [9.0, 8.0, 3.0, 1.3]
prefix15 = [6.3, 5.7, 2.6, 1.5]
prefix20 = [4.1, 6.1, 1.4, 1.4]
x = np.arange(len(eras)); w = 0.25
ax.bar(x-w, prefix10, w, label='prefix 10', color='#3388CC', alpha=0.8, edgecolor='white')
ax.bar(x, prefix15, w, label='prefix 15', color='#FFAA44', alpha=0.8, edgecolor='white')
ax.bar(x+w, prefix20, w, label='prefix 20', color='#88CC66', alpha=0.8, edgecolor='white')
ax.set_xticks(x); ax.set_xticklabels(eras)
ax.set_ylabel('Observed adoption lag (years)')
ax.set_title('S2: Adoption lag by prefix length and era')
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'figS2_prefix_robustness.png'))
plt.close()

# S3: Korea-coded stream leave-one-out
fig, ax = plt.subplots(figsize=(7, 5))
players = ['Choi Jeong','Nakamura S.','Ke Jie','Shin Jinseo','Cho Chikun',
           'Park Junghwan','Kim Eunji','Byun Sangil','Kang Dongyun','Yang Dingxin']
fi_all = +0.0330
fis = [+0.0341, +0.0337, +0.0326, +0.0330, +0.0336,
       +0.0330, +0.0340, +0.0325, +0.0325, +0.0330]
x = np.arange(len(players))
ax.bar(x, fis, color='#FF6644', alpha=0.7, edgecolor='white')
ax.axhline(y=fi_all, color='#333', linewidth=1.5, label=f'All top-10 (fi={fi_all:+.4f})')
ax.set_xticks(x); ax.set_xticklabels(players, rotation=30, ha='right', fontsize=8)
ax.set_ylabel('Fighting index (adj_opp - adj_own)')
ax.set_title('S3: Korea-coded stream — leave-one-out player control')
ax.legend(fontsize=9)
ax.set_ylim(0.030, 0.036)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'figS3_player_control.png'))
plt.close()

print("SI figures S1-S3 saved.")
