"""
Created on Sun Aug 24 23:05:30 2025

@author: ga47jes
"""

# %% import packages
import opentumflex as fl
import pandas as pd
from datetime import datetime

# %% file path
df_sys = pd.read_excel(r'data/parameters.xlsx', index_col=0, usecols=range(0, 3))
df_ts = pd.read_excel(r'data/2019-09-11_timeseries_deterministic.xlsx', usecols='B:I')
df_ts_mean = pd.DataFrame()
n_sample = 10
n_datetime = datetime.now().strftime('%Y%m%d-%H%M')

#%% run loop of synthetic generation and flexibility
ems = fl.run_scenario(fl.scenario_simple_house, df_sys=df_sys, df_ts=df_ts, show_opt_balance=False)   
fig = fl.plot_power_results(ems)
# ems['flexopts']['pv'].to_excel(r'output\\' + n_datetime + '_pv_flex_offers_deterministic.xlsx')

# %%
