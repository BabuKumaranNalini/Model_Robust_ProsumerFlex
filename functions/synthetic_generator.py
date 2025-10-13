# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 00:40:02 2025

@author: babuk
"""

from functions.uncertainty_gen_pv import gaussGen as syn_pv
from functions.uncertainty_gen_load import gaussGen as syn_load
import matplotlib.pyplot as plt

#%% uncertainty generation
def ug_pv(df_ts, risk=0.1):
    df_ts_pv = df_ts.copy()
    P_pv, mape_fb, n_pv, eps, cs = syn_pv(df_ts['solar_power'], risk, 0.01)
    # plt.plot(P_pv)
    # plt.plot(df_ts['solar_power'])
    # plt.show()
    df_ts_pv['solar_power'] = P_pv
    return df_ts_pv

def ug_load(df_ts, risk=0.1):
    df_ts_load = df_ts.copy()
    P_load, fb, n_load = syn_load(df_ts['load_elec'], risk)
    df_ts_load['load_elec'] = P_load
    return df_ts_load
    
def ug_pvload(df_ts, risk=0.1):
    df_ts_pvload = df_ts.copy()
    P_pv, mape_fb, n_pv, eps, cs = syn_pv(df_ts['solar_power'], risk, 0.01)
    P_load, fb, n_load = syn_load(df_ts['load_elec'], risk)
    df_ts_pvload['solar_power'] = P_pv
    df_ts_pvload['load_elec'] = P_load
    return df_ts_pvload