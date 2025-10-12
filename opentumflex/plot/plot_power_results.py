import matplotlib.pyplot as plt
import numpy as np
import datetime
import pandas as pd
import math


def plot_power_results(ems):
    """ visualize only electricity balance and battery SOC results based on ems dict
    Args:
        - ems: ems dict with optimization results
    """
    # plot electricity balance and battery SOC
    isteps = ems['time_data']['isteps']
    nsteps = ems['time_data']['nsteps']
    timesteps = np.arange(ems['time_data']['isteps'], ems['time_data']['nsteps'])
    N = len(timesteps)
    ind = np.arange(N)  # the x locations for the groups
    indplus1 = np.arange(N+1)  # extra index series for step plot
    ts_raw = ems['time_data']['time_slots'][isteps:nsteps]
    ts = pd.to_datetime(ts_raw).strftime('%H:%M')
    ts_date = pd.to_datetime(ts_raw).strftime('%d %b %Y')

    width = 1  # the width of the bars

    # obtain the optimization results from ems dict
    opt_res = ems['optplan']
    for param in opt_res:
        opt_res[param] = np.array(opt_res[param])

    # figure properties - optimized for LaTeX two-column documents
    # Use (3.5, 4.0) for single column or (7.0, 3.5) for two-column span
    fig, axs = plt.subplots(2, 1, figsize=(4, 3.5), gridspec_kw={'height_ratios': [4, 1]})
    plt.rcParams["font.family"] = "Arial"

    # ================ ELECTRICITY BALANCE PLOT ================
    ax1 = axs[0]
    p1 = ax1.bar(ind, opt_res['CHP_elec_pow'], width, bottom=opt_res['bat_output_power'],
            color='skyblue', align='edge')
    p2 = ax1.bar(ind, opt_res['PV_power'], width, bottom=opt_res['bat_output_power'] + opt_res['CHP_elec_pow'],
            color='goldenrod', align='edge')
    p3 = ax1.bar(ind, opt_res['bat_output_power'], width, color='indianred', align='edge')
    p4 = ax1.bar(ind, -opt_res['bat_input_power'], width, color='indianred', align='edge')
    p5 = ax1.bar(ind, opt_res['grid_import'], width,
            bottom=opt_res['bat_output_power'] + opt_res['CHP_elec_pow'] + opt_res['PV_power'],
            color='grey', align='edge')
    p6 = ax1.bar(ind, -opt_res['grid_export'], width, bottom=-opt_res['bat_input_power'],
            color='darkseagreen', align='edge')
    p7 = ax1.bar(ind, -opt_res['EV_power'], width, bottom=-opt_res['bat_input_power'] - opt_res['grid_export'],
            color='plum', align='edge')
    p8 = ax1.bar(ind, -opt_res['HP_elec_power'], width,
            bottom=-opt_res['bat_input_power'] - opt_res['grid_export'] - np.array(opt_res['EV_power']),
            color='wheat', align='edge')
    p9 = ax1.step(indplus1, np.append(opt_res['Last_elec'], 0), linewidth=1, where='post', color='k')

    # xticks and formatting
    ax1.axhline(linewidth=1, color="black")
    idx_plt = np.arange(0, 97, 16)
    idx_plt = idx_plt[idx_plt < len(ts)]  # Ensure indices are within bounds
    if len(idx_plt) > 0 and idx_plt[-1] == len(ts) - 1:  # Remove last value if it's the final index
        idx_plt = idx_plt[:-1]

    # labels and ticks
    ax1.tick_params(axis="x", labelsize=8)
    ax1.tick_params(axis="y", labelsize=8)
    ax1.set_ylabel('Power demand [kW]', fontfamily='Arial', fontsize=8, labelpad=2)
    # ax1.set_title('Electricity Balance', fontfamily='Arial')
    ax1.set_xticks(idx_plt)
    ax1.set_xticklabels(ts[idx_plt], fontfamily='Arial', fontsize=8)
    plt.setp(ax1.get_xticklabels(), visible=False)
    # Set Arial font for y-axis tick labels
    for label in ax1.get_yticklabels():
        label.set_fontfamily('Arial')
    
    # select which legends are to be shown
    selector = {np.count_nonzero(opt_res['CHP_elec_pow']): [p1[0], 'CHP'],
                np.count_nonzero(opt_res['PV_power']): [p2[0], 'PV'],
                np.count_nonzero(opt_res['bat_output_power'] + opt_res['bat_input_power']): [p3[0], 'Battery'],
                np.count_nonzero(opt_res['grid_import']): [p5[0], 'Grid import'],
                np.count_nonzero(opt_res['grid_export']): [p6[0], 'Grid export'],
                np.count_nonzero(opt_res['EV_power']): [p7[0], 'EV'],
                np.count_nonzero(opt_res['HP_elec_power']): [p8[0], 'HP'],
                }
    legend_entries = [p9[0]]
    labels_entries = ['Power demand']
    for count_nonzero, legend_entry in selector.items():
        if count_nonzero > 0:
            legend_entries.append(legend_entry[0])
            labels_entries.append(legend_entry[1])
    ax1.legend(legend_entries, labels_entries,
               prop={'family': 'Arial', 'size': 7}, 
               loc='lower center', 
               ncol=3, frameon=True, 
               fancybox=True, shadow=False, facecolor='white', edgecolor='lightgray',
               columnspacing=0.5, handletextpad=0.3, handlelength=1.0)
    
    # plot properties
    ax1.grid(alpha=0.3)
    # adjust the y-axis limit
    bottom, top = ax1.get_ylim()
    if top >= abs(bottom):
        ax1.set_ylim(-(top + 0.5), top + 0.5)
    else:
        ax1.set_ylim(bottom - 0.5, -(bottom - 0.5))
    ax1.margins(x=0)

    # ================ BATTERY SOC PLOT ================
    ax2 = axs[1]
    p_soc = ax2.step(indplus1, np.append(opt_res['SOC_elec'], 0), linewidth=1, color='indianred', where='post', label='Battery SoC')
    
    # Create secondary y-axis for electricity price
    ax2_price = ax2.twinx()
    
    # Get electricity price data and plot it
    ele_price = np.array(ems['fcst']['ele_price_in'][isteps:nsteps])
    p_price = ax2_price.step(indplus1, np.append(ele_price, ele_price[-1]), linewidth=1, color='grey', where='post', label='Electricity Price', alpha=0.5)
    
    # formatting for SOC axis (left)
    ax2.tick_params(axis="x", labelsize=8)
    ax2.tick_params(axis="y", labelsize=8)
    ax2.set_ylabel('SoC [%]', fontfamily='Arial', fontsize=8, labelpad=2)
    ax2.set_xticks(idx_plt)
    ax2.set_xticklabels(ts[idx_plt], fontfamily='Arial', fontsize=8)
    for label in ax2.get_xticklabels():
        label.set_fontfamily('Arial')
    for label in ax2.get_yticklabels():
        label.set_fontfamily('Arial')
        # label.set_color('indianred')
    ax2.set_ylim(0, 100)
    ax2.set_xlim(0, N)
    ax2.grid(alpha=0.3)
    ax2.margins(x=0)
    
    # formatting for price axis (right)
    ax2_price.tick_params(axis="y", labelsize=8)
    ax2_price.set_ylabel('Price [€/kWh]', fontfamily='Arial', fontsize=8, labelpad=2)
    for label in ax2_price.get_yticklabels():
        label.set_fontfamily('Arial')
        # label.set_color('blue')
    ax2_price.set_xlim(0, N)
    
    # Final formatting
    fig.align_ylabels(axs[:])
    plt.tight_layout()
    plt.savefig('figures/power_balance.pdf', format='pdf', dpi=300)
    plt.show()

    return fig