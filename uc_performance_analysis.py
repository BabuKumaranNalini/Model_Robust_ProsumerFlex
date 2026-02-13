# generate sensitivity of MAPE to outcome

# %% load libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from functions.uncertainty_gen_pv import gaussGen as syn_pv
from functions.uncertainty_gen_load import gaussGen as syn_load

# %% file path
df_ts = pd.read_excel(r'data/2019-09-11_timeseries_deterministic.xlsx', usecols='B:I')

#%% deterministic values
# run synthetic uncertainty generator - pv
# P_pv, mape_pv, n_pv, eps, cs = syn_pv(df_ts['solar_power'], risk, 0.01)

# run synthetic uncertainty generator - load
# P_load, mape_load, n_load = syn_load(df_ts['load_elec'], risk)

# %% sensitivity analysis
risk = np.linspace(5, 50, 10)  # risk levels from 5% to 50%
iter = 100  # number of iterations per risk level
n_pv = pd.DataFrame(np.nan, index=range(iter), columns=risk)
mape_pv = pd.DataFrame(np.nan, index=range(iter), columns=risk)
mape_load = pd.DataFrame(np.nan, index=range(iter), columns=risk)
n_load = pd.DataFrame(np.nan, index=range(iter), columns=risk)

for r in risk:
    for i in range(iter):
        # run synthetic uncertainty generator - pv
        P_pv, mape_pv_i, n_pv_i, eps, cs = syn_pv(df_ts['solar_power'], r/100, 0.001)
        mape_pv.loc[i, r] = mape_pv_i * 100  # in percentage
        n_pv.loc[i, r] = n_pv_i

        # run synthetic uncertainty generator - load
        P_load, mape_load_i, n_load_i = syn_load(df_ts['load_elec'], r/100)
        mape_load.loc[i, r] = mape_load_i * 100  # in percentage
        n_load.loc[i, r] = n_load_i

# %%
# visualize results
import matplotlib.pyplot as plt
save_fig = False  # save figures as pdf in folder 'figures'

# Set Arial font globally
plt.rcParams["font.family"] = "Arial"

# Create separate plots f)or n_pv and n_load

# First plot - n_pv (limit y-axis to 1000)
plt.figure(figsize=(5, 3.5))
bp1 = plt.boxplot(n_pv.values, patch_artist=True, 
                  flierprops=dict(marker='+', markerfacecolor='indianred', markersize=8, 
                                markeredgecolor='indianred', linestyle='none'))

# Customize box plot 1
for box in bp1['boxes']:
    box.set_facecolor('none')  # No fill color
    box.set_edgecolor('blue')  # Blue border
    box.set_linewidth(1)
    box.set_alpha(0.5)  # Add transparency

for whisker in bp1['whiskers']:
    whisker.set_color('black')
    whisker.set_linestyle('--')
    whisker.set_linewidth(1)
    whisker.set_alpha(0.5)  # Add transparency

for cap in bp1['caps']:
    cap.set_color('black')
    cap.set_linewidth(1)
    cap.set_alpha(0.5)  # Add transparency

# Set median lines to indianred
for median in bp1['medians']:
    median.set_color('indianred')
    median.set_linewidth(1)

plt.xlabel('PV forecast uncertainty with target MAPE (%)', fontfamily='Arial', fontsize=9)
plt.ylabel('Number of iterations with ε = 0.1%', fontfamily='Arial', fontsize=9)
plt.gca().set_xticklabels([f'{int(x)}' for x in risk], fontfamily='Arial', fontsize=8)
plt.tick_params(axis='y', labelsize=8)
for label in plt.gca().get_yticklabels():
    label.set_fontfamily('Arial')
# plt.title('Evaluation of PV forecast uncertainty', fontfamily='Arial', fontsize=8, fontweight='bold')
plt.ylim(0, 1000)  # Limit y-axis to 1000
plt.grid(alpha=0.3)
plt.tight_layout()
if save_fig:
        plt.savefig('figures/performance_uc_pv.pdf', format='pdf', dpi=300)
plt.show()

# Second plot - n_load
plt.figure(figsize=(5, 3.5))
bp2 = plt.boxplot(n_load.values, patch_artist=True,
                  flierprops=dict(marker='+', markerfacecolor='indianred', markersize=8, 
                                markeredgecolor='indianred', linestyle='none'))

# Customize box plot 2
for box in bp2['boxes']:
    box.set_facecolor('none')  # No fill color
    box.set_edgecolor('blue')  # Blue border
    box.set_linewidth(1)
    box.set_alpha(0.5)  # Add transparency

for whisker in bp2['whiskers']:
    whisker.set_color('black')
    whisker.set_linestyle('--')
    whisker.set_linewidth(1)
    whisker.set_alpha(0.5)  # Add transparency

for cap in bp2['caps']:
    cap.set_color('black')
    cap.set_linewidth(1)
    cap.set_alpha(0.5)  # Add transparency

# Set median lines to indianred
for median in bp2['medians']:
    median.set_color('indianred')
    median.set_linewidth(1)

plt.xlabel('Demand uncertainty with target MAPE (%)', fontfamily='Arial', fontsize=9)
plt.ylabel('Number of iterations with ε = 0.1%', fontfamily='Arial', fontsize=9)
plt.gca().set_xticklabels([f'{int(x)}' for x in risk], fontfamily='Arial', fontsize=8)
plt.tick_params(axis='y', labelsize=8)
for label in plt.gca().get_yticklabels():
    label.set_fontfamily('Arial')
# plt.title('Evaluation of demand uncertainty', fontfamily='Arial', fontsize=8, fontweight='bold')
plt.ylim(bottom=0, top=1000)  # Set y-axis minimum to 0
plt.grid(alpha=0.3)
plt.tight_layout()
if save_fig:
        plt.savefig('figures/performance_uc_load.pdf', format='pdf', dpi=300)
plt.show()
# %%
