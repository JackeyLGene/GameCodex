"""Generate paper figures for PNAS submission.

Figures:
  1. Decade drift envelope with AI-era mark
  2. Fixed-horizon adoption by era (censoring-safe)
  4. Regional event-stream three-phase distance (with bootstrap CIs)
  5. Pattern adoption lag + reuse density trend
"""
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
                      'figure.dpi': 150, 'savefig.dpi': 300,
                      'savefig.bbox': 'tight'})

# ═══════════════════════════════════════════════════════════════
# Figure 1: Decade drift envelope with AI-era position
# ═══════════════════════════════════════════════════════════════

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Panel A: Decade drift timeline
decades = ['1600s','1700s','1800s','1850s','1900s','1910s','1920s','1930s',
           '1940s','1950s','1960s','1970s','1980s','1990s','2000s','2010s','2020s']
drifts = [0.024, 0.017, 0.004, 0.028, 0.016, 0.034, 0.023, 0.022, 0.008,
          0.013, 0.004, 0.004, 0.005, 0.009, 0.007, 0.0074, 0.0130]

colors = ['#CCCCCC'] * len(drifts)
# Mark pre-2016 vs AI-era
for i, d in enumerate(decades):
    if '2010' in d: colors[i] = '#FF9500'  # AI transition
    elif '2020' in d: colors[i] = '#FF4444'  # AI era

ax1.bar(range(len(drifts)), drifts, color=colors, edgecolor='white', linewidth=0.5)
ax1.axhline(y=0.0146, color='gray', linestyle='--', alpha=0.5, label='Pre-2016 mean (0.015)')
ax1.axhline(y=0.0342, color='gray', linestyle=':', alpha=0.3, label='Pre-2016 observed max')
ax1.set_xticks(range(len(decades)))
ax1.set_xticklabels(decades, rotation=45, ha='right', fontsize=8)
ax1.set_ylabel('Decade-to-decade |drift|')
ax1.set_title('A. Century-scale structural drift')
ax1.legend(fontsize=7)

# Panel B: AI-era drift position relative to historical envelope
pre_drifts = [0.024, 0.017, 0.004, 0.028, 0.016, 0.034, 0.023, 0.022, 0.008,
              0.013, 0.004, 0.004, 0.005, 0.009, 0.007]
ai_drift = 0.0130

ax2.hist(pre_drifts, bins=8, color='#CCCCCC', edgecolor='white', alpha=0.8)
ax2.axvline(x=ai_drift, color='#FF4444', linewidth=2, label=f'AI era (0.013)')
ax2.axvline(x=np.mean(pre_drifts), color='gray', linestyle='--', label=f'Pre-2016 mean (0.015)')
ax2.set_xlabel('|drift| magnitude')
ax2.set_ylabel('Count')
ax2.set_title('B. AI-era vs historical envelope')
ax2.legend(fontsize=8)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'fig1_drift_envelope.png'))
plt.close()
print("Figure 1 saved.")

# ═══════════════════════════════════════════════════════════════
# Figure 2: Fixed-horizon adoption by era
# ═══════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(8, 5))

eras = ['pre-1980', '1980-1999', '2000-2015', '2016+']
horizons = [1, 2, 3, 5]
# Data from phase5_hardening.py Task 2
adoption_data = {
    'pre-1980':    [0.31, 0.37, 0.39, 0.44],
    '1980-1999':   [0.24, 0.29, 0.36, 0.43],
    '2000-2015':   [0.47, 0.60, 0.63, 0.59],
    '2016+':       [0.57, 0.73, 0.80, 0.91],
}
colors_era = {'pre-1980': '#BBBBBB', '1980-1999': '#99AACC',
              '2000-2015': '#FFAA44', '2016+': '#FF4444'}

x = np.arange(len(horizons))
width = 0.2
for i, era in enumerate(eras):
    ax.bar(x + i*width, adoption_data[era], width,
           color=colors_era[era], alpha=0.85, label=era, edgecolor='white')

ax.set_xticks(x + width*1.5)
ax.set_xticklabels([f'≤{h} yr' for h in horizons])
ax.set_ylabel('Probability of adoption')
ax.set_title('Fixed-horizon adoption probability by era of first appearance')
ax.legend(fontsize=9)
ax.set_ylim(0, 1.0)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'fig2_fixed_horizon_adoption.png'))
plt.close()
print("Figure 2 saved.")

# ═══════════════════════════════════════════════════════════════
# Figure 4: Regional event-stream three-phase distance
# ═══════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(8, 5))

phases = ['Pre-AI\n(1990-2015)', 'Shock\n(2016-17)', 'Diffusion\n(2018-21)', 'Oracle\n(2022-25)']
distances = [0.0144, 0.0066, 0.0167, 0.0102]
ci_low = [0.0109, 0.0037, 0.0109, 0.0056]
ci_high = [0.0361, 0.0151, 0.0323, 0.0212]
yerr_low = [d - l for d, l in zip(distances, ci_low)]
yerr_high = [h - d for d, h in zip(distances, ci_high)]

ax.errorbar(range(len(phases)), distances, yerr=[yerr_low, yerr_high],
            fmt='o-', color='#3366CC', linewidth=2, markersize=10,
            capsize=8, capthick=2, elinewidth=1.5)

# Shade the AI-era phases
ax.axvspan(0.5, 3.5, alpha=0.06, color='orange')
ax.text(2, max(ci_high)*0.95, 'AI era', ha='center', fontsize=9, color='#CC6600', style='italic')

ax.set_xticks(range(len(phases)))
ax.set_xticklabels(phases)
ax.set_ylabel('Inter-stream 5-feature distance')
ax.set_title('Regional event-stream dynamics: three-phase response')
ax.set_ylim(0, max(ci_high)*1.1)

# Annotations
ax.annotate('convergence', xy=(1, distances[1]), xytext=(1, distances[1]+0.015),
            arrowprops=dict(arrowstyle='->', color='gray'), fontsize=8, color='gray')
ax.annotate('re-divergence', xy=(2, distances[2]), xytext=(2, distances[2]+0.015),
            arrowprops=dict(arrowstyle='->', color='gray'), fontsize=8, color='gray')
ax.annotate('re-convergence', xy=(3, distances[3]), xytext=(3, distances[3]+0.015),
            arrowprops=dict(arrowstyle='->', color='gray'), fontsize=8, color='gray')

plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'fig4_regional_three_phase.png'))
plt.close()
print("Figure 4 saved.")

# ═══════════════════════════════════════════════════════════════
# Figure 5: Pattern adoption lag + reuse density
# ═══════════════════════════════════════════════════════════════

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# Panel A: Adoption lag
eras_label = ['pre-1980', '1980-1999', '2000-2015', '2016+']
adoption_lag = [6.3, 5.7, 2.6, 1.5]
lag_ci_lo = [2.2, 2.0, 1.5, 1.0]  # approximate from bootstrap
lag_ci_hi = [7.4, 6.5, 3.3, 2.2]

ax1.bar(eras_label, adoption_lag, color=['#BBBBBB','#99AACC','#FFAA44','#FF4444'],
        edgecolor='white', alpha=0.85)
ax1.set_ylabel('Observed adoption lag (years)')
ax1.set_title('A. Pattern adoption lag by era')
ax1.set_ylim(0, 7.2)
for i, v in enumerate(adoption_lag):
    ax1.text(i, v+0.18, f'{v:.1f} yr', ha='center', fontsize=9, fontweight='bold')

# Panel B: Reuse density
reuse = [0.35, 0.37, 0.67, 0.78]
ax2.bar(eras_label, reuse, color=['#BBBBBB','#99AACC','#FFAA44','#FF4444'],
        edgecolor='white', alpha=0.85)
ax2.set_ylabel('Observed reuse density')
ax2.set_title('B. Pattern reuse density by era')
ax2.set_ylim(0, 0.9)
for i, v in enumerate(reuse):
    ax2.text(i, v+0.03, f'{v:.2f}', ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'fig5_pattern_adoption.png'))
plt.close()
print("Figure 5 saved.")

print(f"\nAll figures saved to {out_dir}/")
