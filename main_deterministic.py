"""
Created on Sun Aug 24 23:05:30 2025

@author: ga47jes
"""

# %% import packages
import opentumflex as fl
import pandas as pd
from datetime import datetime
from functions.consolidate_flex import get_flex_envelope_dataframe
from functions.plot_flex_ems import plot_flex_duration_with_timestamps

# %% file path
df_sys = pd.read_excel(r'data/parameters.xlsx', index_col=0, usecols=range(0, 3))
df_ts = pd.read_excel(r'data/2019-09-11_timeseries_deterministic.xlsx', usecols='B:I')

#%% run loop of synthetic generation and flexibility
ems = fl.run_scenario(fl.scenario_simple_house, df_sys=df_sys, df_ts=df_ts, show_opt_balance=False)   
fig_ems = fl.plot_power_results(ems, save_fig=True)

# %% Extract flexibility envelope DataFrame
flex_ems = get_flex_envelope_dataframe(ems)

# %%
fig_flex = plot_flex_duration_with_timestamps(flex_ems, timestamps=pd.to_datetime(ems['time_data']['time_slots']), save_fig=True)
