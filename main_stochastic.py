"""
Created on Sun Aug 24 23:05:30 2025

@author: ga47jes
"""

import opentumflex as fl
import pandas as pd
from functions.synthetic_generator import *
from datetime import datetime

# %% file path
df_sys = pd.read_excel(r'data/parameters.xlsx', index_col=0, usecols=range(0, 3))
df_ts = pd.read_excel(r'data/timeseries.xlsx', usecols='B:I')
df_ts_mean = pd.DataFrame()
n_sample = 10
n_datetime = datetime.now().strftime('%Y%m%d-%H%M')

#%% run loop of synthetic generation and flexibility
for n in range(0,n_sample):
    print('Optimizing sample:', n)
    # run synthetic uncertainty generator
    df_ts_new = ug_pvload(df_ts)
    df_ts_new.to_excel(r'output\samples\timeseries_'+str(n)+'s.xlsx')
    
    # run opentumflex
    ems = fl.run_scenario(fl.scenario_pv, df_sys=df_sys, df_ts=df_ts_new)   
    # ems['flexopts']['pv'].to_excel(r'output\pv_flex_offers_'+str(n)+'s.xlsx')
    
    if n==0:
        df_ts_mean = ems['flexopts']['pv']
    else:
        df_ts_mean = df_ts_mean + ems['flexopts']['pv']
                     
df_ts_mean = df_ts_mean/n_sample
df_ts_mean.to_excel(r'output\\' + n_datetime +'_pv_flex_offers_stochastic_mean.xlsx')

ems = fl.run_scenario(fl.scenario_pv, df_sys=df_sys, df_ts=df_ts)   
ems['flexopts']['pv'].to_excel(r'output\\' + n_datetime + '_pv_flex_offers_deterministic.xlsx')