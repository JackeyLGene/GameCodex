"""Figure: 1910s→1920s overlap-player decomposition."""
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Panel A: Drift decomposition
categories = ['Full\ndrift', 'Overlap\nplayers', 'Non-overlap\nplayers']
values = [0.0342, 0.0291, 0.0292]
colors = ['#555555', '#3388CC', '#FFAA44']

bars = ax1.bar(categories, values, color=colors, edgecolor='white', width=0.5)
ax1.set_ylabel('|drift| magnitude')
ax1.set_title('A. 1910s→1920s drift decomposition')
for bar, val in zip(bars, values):
    ax1.text(bar.get_x()+bar.get_width()/2, val+0.001, f'{val:.4f}',
             ha='center', fontsize=10, fontweight='bold')

# Add reference line for AI-era drift
ax1.axhline(y=0.0130, color='#FF4444', linestyle='--', linewidth=1.5, label='AI-era drift (0.013)')
ax1.legend(fontsize=9)

# Panel B: Two revolutions comparison
eras_labels = ['1910s→1920s\nInstitutional\nRevolution', '2010s→2020s\nOracle-Speed\nRevolution']
drift_vals = [0.034, 0.013]
pattern_lag = [None, 4.2]  # adoption lag ratio only meaningful for AI era

x = np.arange(len(eras_labels))
width = 0.35

bars_d = ax2.bar(x - width/2, drift_vals, width, color=['#555555','#FF4444'],
                  edgecolor='white', label='Structural drift')
ax2.set_ylabel('|drift| magnitude', color='#333')
ax2.set_ylim(0, 0.04)
for i, (bar, val) in enumerate(zip(bars_d, drift_vals)):
    ax2.text(bar.get_x()+bar.get_width()/2, val+0.001, f'{val:.3f}',
             ha='center', fontsize=10, fontweight='bold')

ax3 = ax2.twinx()
ax3.set_ylabel('Adoption speed ratio', color='#FF4444')
ax3.bar(x[-1] + width/2, 4.2, width, color='#FF664488', edgecolor='#FF4444',
        label='Adoption acceleration')
ax3.text(x[-1] + width/2, 4.4, '4.2×', ha='center', fontsize=10, fontweight='bold', color='#CC0000')
ax3.set_ylim(0, 5.5)

ax2.set_xticks(x)
ax2.set_xticklabels(eras_labels)
ax2.set_title('B. Two revolutions: structural vs speed', fontsize=11)

# Legends
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax3.get_legend_handles_labels()
ax2.legend(lines1+lines2, labels1+labels2, loc='upper right', fontsize=8)

ax1.annotate('85% of drift\nfrom same players', xy=(1, 0.0291),
             xytext=(0.35, 0.021), fontsize=9, ha='center',
             arrowprops=dict(arrowstyle='->', color='#3388CC', lw=1.2),
             color='#3388CC', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                       edgecolor='none', alpha=0.85))

plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'fig3_1910s_decomposition.png'))
plt.close()
print("Fig 3 saved.")
