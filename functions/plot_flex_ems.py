import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_flex_ems(flex_ems, figsize=(4, 3.5), save_fig=False):
    """
    Plot flexibility EMS data with 3 subplots:
    1. Power flexibility: Neg_P, Pos_P as bars with Sch_P as line
    2. Energy flexibility: Neg_E, Pos_E as bars
    3. Price flexibility: Neg_Pr, Pos_Pr as bars
    
    Args:
        flex_ems: DataFrame or dict containing flexibility data
        figsize: Figure size (width, height) in inches
    """
    
    # Convert to DataFrame if it's a dict
    if isinstance(flex_ems, dict):
        df = pd.DataFrame(flex_ems)
    else:
        df = flex_ems.copy()
    
    # Create time index for x-axis
    N = len(df)
    ind = np.arange(N)
    width = 0.8  # Bar width
    
    # Create subplots with 3:1:1 height ratio
    fig, axs = plt.subplots(3, 1, figsize=figsize, gridspec_kw={'height_ratios': [3, 1, 1]})
    plt.rcParams["font.family"] = "Arial"
    
    # Define colors
    neg_color = 'lightcoral'
    pos_color = 'lightblue'
    sch_color = 'darkgreen'
    
    # ================ SUBPLOT 1: POWER FLEXIBILITY ================
    ax1 = axs[0]
    
    # Plot negative and positive power as bars
    if 'Neg_P' in df.columns:
        p1 = ax1.bar(ind, df['Neg_P'], width, color=neg_color, alpha=0.8, label='Neg_P', align='center')
    if 'Pos_P' in df.columns:
        p2 = ax1.bar(ind, df['Pos_P'], width, color=pos_color, alpha=0.8, label='Pos_P', align='center')
    
    # Plot scheduled power as line
    if 'Sch_P' in df.columns:
        p3 = ax1.plot(ind, df['Sch_P'], color=sch_color, linewidth=2, marker='o', markersize=3, label='Sch_P')
    
    # Formatting for subplot 1
    ax1.axhline(y=0, color='black', linewidth=1, alpha=0.5)
    ax1.set_ylabel('Power [kW]', fontfamily='Arial', fontsize=9, labelpad=2)
    ax1.tick_params(axis="x", labelsize=8)
    ax1.tick_params(axis="y", labelsize=8)
    ax1.grid(alpha=0.3)
    ax1.legend(prop={'family': 'Arial', 'size': 8}, loc='upper right', frameon=True,
               fancybox=True, shadow=False, facecolor='white', edgecolor='lightgray')
    
    # Hide x-axis labels for top subplot
    plt.setp(ax1.get_xticklabels(), visible=False)
    
    # ================ SUBPLOT 2: ENERGY FLEXIBILITY ================
    ax2 = axs[1]
    
    # Plot negative and positive energy as bars
    if 'Neg_E' in df.columns:
        p4 = ax2.bar(ind, df['Neg_E'], width, color=neg_color, alpha=0.8, label='Neg_E', align='center')
    if 'Pos_E' in df.columns:
        p5 = ax2.bar(ind, df['Pos_E'], width, color=pos_color, alpha=0.8, label='Pos_E', align='center')
    
    # Formatting for subplot 2
    ax2.axhline(y=0, color='black', linewidth=1, alpha=0.5)
    ax2.set_ylabel('Energy [kWh]', fontfamily='Arial', fontsize=9, labelpad=2)
    ax2.tick_params(axis="x", labelsize=8)
    ax2.tick_params(axis="y", labelsize=8)
    ax2.grid(alpha=0.3)
    ax2.legend(prop={'family': 'Arial', 'size': 8}, loc='upper right', frameon=True,
               fancybox=True, shadow=False, facecolor='white', edgecolor='lightgray')
    
    # Hide x-axis labels for middle subplot
    plt.setp(ax2.get_xticklabels(), visible=False)
    
    # ================ SUBPLOT 3: PRICE FLEXIBILITY ================
    ax3 = axs[2]
    
    # Plot negative and positive price as bars
    if 'Neg_Pr' in df.columns:
        p6 = ax3.bar(ind, df['Neg_Pr'], width, color=neg_color, alpha=0.8, label='Neg_Pr', align='center')
    if 'Pos_Pr' in df.columns:
        p7 = ax3.bar(ind, df['Pos_Pr'], width, color=pos_color, alpha=0.8, label='Pos_Pr', align='center')
    
    # Formatting for subplot 3
    ax3.axhline(y=0, color='black', linewidth=1, alpha=0.5)
    ax3.set_ylabel('Price[€/kWh]', fontfamily='Arial', fontsize=9, labelpad=2)
    ax3.set_xlabel('Time Steps', fontfamily='Arial', fontsize=9, labelpad=2)
    ax3.tick_params(axis="x", labelsize=8)
    ax3.tick_params(axis="y", labelsize=8)
    ax3.grid(alpha=0.3)
    ax3.legend(prop={'family': 'Arial', 'size': 8}, loc='upper right', frameon=True,
               fancybox=True, shadow=False, facecolor='white', edgecolor='lightgray')
    
    # Set x-axis ticks and labels for bottom subplot
    if N > 16:
        tick_indices = np.arange(0, N, max(1, N//8))  # Show approximately 8 ticks
    else:
        tick_indices = np.arange(0, N, max(1, N//4))  # Show approximately 4 ticks
    
    ax3.set_xticks(tick_indices)
    ax3.set_xticklabels([str(i) for i in tick_indices], fontfamily='Arial', fontsize=8)
    
    # Set x-axis limits for all subplots
    for ax in axs:
        ax.set_xlim(-0.5, N-0.5)
        ax.margins(x=0)
    
    # Final formatting
    fig.align_ylabels(axs[:])
    plt.tight_layout(pad=0.5)
    if save_fig:
        plt.savefig('figures/flex_ems_deterministic.pdf', format='pdf', dpi=300)
    plt.show()
    
    return fig


def plot_flex_ems_with_timestamps(flex_ems, timestamps=None, figsize=(4, 3.5), save_fig=False):
    """
    Plot flexibility EMS data with time-based x-axis labels
    
    Args:
        flex_ems: DataFrame or dict containing flexibility data
        timestamps: Optional list/array of timestamp labels
        figsize: Figure size (width, height) in inches
    """
    
    # Convert to DataFrame if it's a dict
    if isinstance(flex_ems, dict):
        df = pd.DataFrame(flex_ems)
    else:
        df = flex_ems.copy()
    
    # Create time index for x-axis
    N = len(df)
    ind = np.arange(N)
    width = 0.8  # Bar width
    
    # Create subplots with 3:1:1 height ratio
    fig, axs = plt.subplots(3, 1, figsize=figsize, gridspec_kw={'height_ratios': [3, 1, 1]})
    plt.rcParams["font.family"] = "Arial"
    
    # Define colors
    neg_color = 'lightcoral'
    pos_color = 'lightblue'
    sch_color = 'darkgreen'
    
    # ================ SUBPLOT 1: POWER FLEXIBILITY ================
    ax1 = axs[0]
    
    # Plot negative and positive power as bars
    if 'Neg_P' in df.columns:
        p1 = ax1.bar(ind, df['Neg_P'], width, color=neg_color, alpha=0.8, label='Neg_P', align='center')
    if 'Pos_P' in df.columns:
        p2 = ax1.bar(ind, df['Pos_P'], width, color=pos_color, alpha=0.8, label='Pos_P', align='center')
    
    # Plot scheduled power as line
    if 'Sch_P' in df.columns:
        p3 = ax1.plot(ind, df['Sch_P'], color=sch_color, linewidth=2, marker='o', markersize=3, label='Sch_P')
    
    # Formatting for subplot 1
    ax1.axhline(y=0, color='black', linewidth=1, alpha=0.5)
    ax1.set_ylabel('Power [kW]', fontfamily='Arial', fontsize=9, labelpad=2)
    ax1.tick_params(axis="x", labelsize=8)
    ax1.tick_params(axis="y", labelsize=8)
    ax1.grid(alpha=0.3)
    ax1.legend(prop={'family': 'Arial', 'size': 8}, loc='upper right', frameon=True,
               fancybox=True, shadow=False, facecolor='white', edgecolor='lightgray')
    
    # Hide x-axis labels for top subplot
    plt.setp(ax1.get_xticklabels(), visible=False)
    
    # ================ SUBPLOT 2: ENERGY FLEXIBILITY ================
    ax2 = axs[1]
    
    # Plot negative and positive energy as bars
    if 'Neg_E' in df.columns:
        p4 = ax2.bar(ind, df['Neg_E'], width, color=neg_color, alpha=0.8, label='Neg_E', align='center')
    if 'Pos_E' in df.columns:
        p5 = ax2.bar(ind, df['Pos_E'], width, color=pos_color, alpha=0.8, label='Pos_E', align='center')
    
    # Formatting for subplot 2
    ax2.axhline(y=0, color='black', linewidth=1, alpha=0.5)
    ax2.set_ylabel('Energy [kWh]', fontfamily='Arial', fontsize=9, labelpad=2)
    ax2.tick_params(axis="x", labelsize=8)
    ax2.tick_params(axis="y", labelsize=8)
    ax2.grid(alpha=0.3)
    ax2.legend(prop={'family': 'Arial', 'size': 8}, loc='upper right', frameon=True,
               fancybox=True, shadow=False, facecolor='white', edgecolor='lightgray')
    
    # Hide x-axis labels for middle subplot
    plt.setp(ax2.get_xticklabels(), visible=False)
    
    # ================ SUBPLOT 3: PRICE FLEXIBILITY ================
    ax3 = axs[2]
    
    # Plot negative and positive price as bars
    if 'Neg_Pr' in df.columns:
        p6 = ax3.bar(ind, df['Neg_Pr'], width, color=neg_color, alpha=0.8, label='Neg_Pr', align='center')
    if 'Pos_Pr' in df.columns:
        p7 = ax3.bar(ind, df['Pos_Pr'], width, color=pos_color, alpha=0.8, label='Pos_Pr', align='center')
    
    # Formatting for subplot 3
    ax3.axhline(y=0, color='black', linewidth=1, alpha=0.5)
    ax3.set_ylabel('Price [€/kWh]', fontfamily='Arial', fontsize=9, labelpad=2)
    ax3.set_xlabel('Time', fontfamily='Arial', fontsize=9, labelpad=2)
    ax3.tick_params(axis="x", labelsize=8)
    ax3.tick_params(axis="y", labelsize=8)
    ax3.grid(alpha=0.3)
    ax3.legend(prop={'family': 'Arial', 'size': 8}, loc='upper right', frameon=True,
               fancybox=True, shadow=False, facecolor='white', edgecolor='lightgray')
    
    # Set x-axis ticks and labels for bottom subplot using consistent indexing
    idx_plt = np.arange(0, 97, 16)
    idx_plt = idx_plt[idx_plt < N]  # Ensure indices are within bounds
    if len(idx_plt) > 0 and idx_plt[-1] == N - 1:  # Remove last value if it's the final index
        idx_plt = idx_plt[:-1]
    
    if timestamps is not None and len(timestamps) > 0:
        # Use provided timestamps with consistent indexing
        idx_plt = idx_plt[idx_plt < len(timestamps)]  # Ensure indices are within timestamp bounds
        
        if hasattr(timestamps[0], 'strftime'):  # If timestamps are datetime objects
            tick_labels = [timestamps[i].strftime('%H:%M') for i in idx_plt]
        else:
            tick_labels = [str(timestamps[i]) for i in idx_plt]
            
        ax3.set_xticks(idx_plt)
        ax3.set_xticklabels(tick_labels, fontfamily='Arial', fontsize=8)
    else:
        # Use step numbers with consistent indexing
        ax3.set_xticks(idx_plt)
        ax3.set_xticklabels([str(i) for i in idx_plt], fontfamily='Arial', fontsize=8)
    
    # Set x-axis limits for all subplots
    for ax in axs:
        ax.set_xlim(-0.5, N-0.5)
        ax.margins(x=0)
    
    # Final formatting
    fig.align_ylabels(axs[:])
    plt.tight_layout(pad=0.5)
    if save_fig:
        plt.savefig('figures/flex_ems_deterministic.pdf', format='pdf', dpi=300)
    plt.show()
    
    return fig


def plot_flex_duration_with_timestamps(flex_ems, timestamps=None, figsize=(4, 3.5), save_fig=False):
    """
    Plot flexibility EMS data with 2 subplots:
    1. Power flexibility: Neg_P, Pos_P as bars with Sch_P as line (same as original)
    2. Duration flexibility: Calculated duration (Energy/Power) for Neg_E/Neg_P and Pos_E/Pos_P
    
    Args:
        flex_ems: DataFrame or dict containing flexibility data
        timestamps: Optional list/array of timestamp labels
        figsize: Figure size (width, height) in inches
        save_fig: Whether to save the figure
    """
    
    # Convert to DataFrame if it's a dict
    if isinstance(flex_ems, dict):
        df = pd.DataFrame(flex_ems)
    else:
        df = flex_ems.copy()
    
    # Create time index for x-axis
    N = len(df)
    ind = np.arange(N)
    width = 0.6  # Bar width
    
    # Create subplots with 3:1 height ratio (2 subplots instead of 3)
    fig, axs = plt.subplots(2, 1, figsize=figsize, gridspec_kw={'height_ratios': [3, 1]})
    plt.rcParams["font.family"] = "Arial"
    
    # Define colors
    neg_color = 'lightcoral'
    pos_color = 'lightblue'
    sch_color = 'darkgreen'
    
    # ================ SUBPLOT 1: POWER FLEXIBILITY (SAME AS ORIGINAL) ================
    ax1 = axs[0]
    
    # Plot negative and positive power as bars
    if 'Neg_P' in df.columns:
        p1 = ax1.bar(ind, df['Neg_P'], width, color=neg_color, alpha=0.8, label='Negative flexibility power', align='center')
    if 'Pos_P' in df.columns:
        p2 = ax1.bar(ind, df['Pos_P'], width, color=pos_color, alpha=0.8, label='Positive flexibility power', align='center')

    # Plot scheduled power as line

    if 'Sch_P' in df.columns:
        p3 = ax1.plot(ind, df['Sch_P'], color=sch_color, linewidth=1, marker='o', markersize=3, label='Scheduled grid exchange')
    # if 'Sch_P' in df.columns:
    #     p3 = ax1.bar(ind, df['Sch_P'], width, color='none', edgecolor=sch_color, linewidth=1, label='Scheduled grid exchange', align='center')
    
    # Formatting for subplot 1
    ax1.axhline(y=0, color='black', linewidth=1, alpha=0.5)
    ax1.set_ylabel('Power [kW]', fontfamily='Arial', fontsize=9, labelpad=2)
    ax1.tick_params(axis="x", labelsize=8)
    ax1.tick_params(axis="y", labelsize=8)
    ax1.grid(alpha=0.3)
    ax1.legend(prop={'family': 'Arial', 'size': 8}, loc='upper right', frameon=True,
               fancybox=True, shadow=False, facecolor='white', edgecolor='lightgray')
    
    # Hide x-axis labels for top subplot
    plt.setp(ax1.get_xticklabels(), visible=False)
    
    # ================ SUBPLOT 2: DURATION FLEXIBILITY ================
    ax2 = axs[1]
    
    # Calculate duration as Energy/Power (with safety check for division by zero)
    neg_duration = np.zeros(N)
    pos_duration = np.zeros(N)
    
    if 'Neg_E' in df.columns and 'Neg_P' in df.columns:
        # Calculate negative duration: Neg_E / abs(Neg_P)
        neg_p_safe = np.where(np.abs(df['Neg_P']) > 1e-6, np.abs(df['Neg_P']), np.nan)
        neg_duration = np.where(~np.isnan(neg_p_safe), np.abs(df['Neg_E']) / neg_p_safe, 0)
        neg_duration = np.nan_to_num(neg_duration, nan=0.0, posinf=0.0, neginf=0.0)
        
    if 'Pos_E' in df.columns and 'Pos_P' in df.columns:
        # Calculate positive duration: Pos_E / Pos_P
        pos_p_safe = np.where(np.abs(df['Pos_P']) > 1e-6, np.abs(df['Pos_P']), np.nan)
        pos_duration = np.where(~np.isnan(pos_p_safe), np.abs(df['Pos_E']) / pos_p_safe, 0)
        pos_duration = np.nan_to_num(pos_duration, nan=0.0, posinf=0.0, neginf=0.0)
    
    # Plot negative and positive duration as bars
    if np.any(neg_duration > 0):
        p4 = ax2.bar(ind, neg_duration, width, color=neg_color, alpha=0.8, label='Negative flexibility duration', align='center')
    if np.any(pos_duration > 0):
        p5 = ax2.bar(ind, pos_duration, width, color=pos_color, alpha=0.8, label='Positive flexibility duration', align='center')

    # Formatting for subplot 2
    ax2.axhline(y=0, color='black', linewidth=1, alpha=0.5)
    ax2.set_ylabel('Duration [hours]', fontfamily='Arial', fontsize=9, labelpad=2)
    ax2.tick_params(axis="x", labelsize=8)
    ax2.tick_params(axis="y", labelsize=8)
    ax2.grid(alpha=0.3)
    ax2.legend(prop={'family': 'Arial', 'size': 7}, loc='upper right', frameon=True,
               fancybox=True, shadow=False, facecolor='white', edgecolor='lightgray')
    
    # Set x-axis ticks and labels for bottom subplot using consistent indexing
    idx_plt = np.arange(0, 97, 16)
    idx_plt = idx_plt[idx_plt < N]  # Ensure indices are within bounds
    if len(idx_plt) > 0 and idx_plt[-1] == N - 1:  # Remove last value if it's the final index
        idx_plt = idx_plt[:-1]
    
    if timestamps is not None and len(timestamps) > 0:
        # Use provided timestamps with consistent indexing
        idx_plt = idx_plt[idx_plt < len(timestamps)]  # Ensure indices are within timestamp bounds
        
        if hasattr(timestamps[0], 'strftime'):  # If timestamps are datetime objects
            tick_labels = [timestamps[i].strftime('%H:%M') for i in idx_plt]
        else:
            tick_labels = [str(timestamps[i]) for i in idx_plt]
            
        ax2.set_xticks(idx_plt)
        ax2.set_xticklabels(tick_labels, fontfamily='Arial', fontsize=8)
    else:
        # Use step numbers with consistent indexing
        ax2.set_xticks(idx_plt)
        ax2.set_xticklabels([str(i) for i in idx_plt], fontfamily='Arial', fontsize=8)
    
    # Set x-axis limits for all subplots
    for ax in axs:
        ax.set_xlim(-0.5, N-0.5)
        ax.margins(x=0)
    
    # Final formatting
    fig.align_ylabels(axs[:])
    plt.tight_layout(pad=0.5)
    if save_fig:
        plt.savefig('figures/flex_duration.pdf', format='pdf', dpi=300)
    plt.show()
    
    return fig


if __name__ == "__main__":
    # Example usage with sample data
    import numpy as np
    
    # Create sample flex_ems data
    n_steps = 24
    sample_flex_ems = {
        'Neg_P': np.random.uniform(0, 5, n_steps),
        'Pos_P': np.random.uniform(0, 5, n_steps),
        'Sch_P': np.random.uniform(-2, 3, n_steps),
        'Neg_E': np.random.uniform(0, 10, n_steps),
        'Pos_E': np.random.uniform(0, 10, n_steps),
        'Neg_Pr': np.random.uniform(0, 0.5, n_steps),
        'Pos_Pr': np.random.uniform(0, 0.5, n_steps)
    }
    
    # Plot the sample data
    print("Plotting sample flex_ems data...")
    fig = plot_flex_ems(sample_flex_ems, figsize=(4, 3.5))