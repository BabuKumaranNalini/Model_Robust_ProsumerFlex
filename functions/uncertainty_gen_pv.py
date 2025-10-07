# -*- coding: utf-8 -*-
"""
Created on Sat Aug 23 14:55:08 2025

@author: Babu Kumaran Nalini, M.Sc. 
@email: babu.kumaran-nalini@tum.de
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pvlib import location

#%% functions
def mape(a, g):
    return np.nansum(np.abs((g - a) / a)) / np.size(a)  # Mean Absolute Percentage Error, MAPE

def gaussGen(x_a, E_s, s):
    x_a = x_a.where(x_a > 0, 0)
    x_g = np.zeros_like(x_a)  # Initialize generated array
    
    # clear sky value from pvlib
    times = pd.date_range('2017-06-01', '2017-06-02', freq='15min', tz='UTC')[:-1]
    loc = location.Location(latitude=47.677950, longitude=-9.17323, altitude=100, tz=times.tz)
    x_g_max = loc.get_clearsky(times, model='haurwitz')['ghi']
    x_g_max = x_g_max / np.max(x_g_max)
    x_g_max[x_g_max < 0.1] = 0.1    
    x_g_max = x_g_max.to_numpy()
    
    n = 0  # Number of iterations
    alpha = 1

    while True:
        for i in range(len(x_a)):
            x_g[i] = x_a[i] + np.random.normal(0, alpha * E_s * np.mean(x_a))  # Generate Gaussian noise

            if x_g[i] < 0:
                x_g[i] = 0  # Limiting loads: P(t) >= 0
                
            if x_g[i] > x_g_max[i]:
                x_g[i] = x_g_max[i]  # Limiting power: P(t) <= P_max
                
            if x_a[i] == 0:
                x_g[i] = 0
                
        n += 1

        current_mape = mape(x_a, x_g)
        alpha = E_s / current_mape
        
        if abs(current_mape - E_s) <= s:
            break  # Break the loop if the gap is less than 0.001
        
    mape_fb = mape(x_a, x_g)
    eps = abs(current_mape - E_s)  # Solution gap feedback
    return x_g, mape_fb, n, eps, x_g_max

#%% run independently
if __name__ == '__main__':
    profiles = pd.read_csv('data/pv.csv')
    P_a = profiles['solar']
    
    # Uncertain load profile generation
    P_g, mape_fb, n, eps, cs = gaussGen(P_a, 0.1, 0.01)
    
    # Print MAPE, number of iterations, and epsilon
    print("MAPE:", mape_fb)
    print("Number of iterations:", n)
    print("Epsilon:", eps)
    
    # Plotting
    plt.figure()
    plt.step(range(1, 97), P_g, 'r-', label='Generated Power (P_g)')
    plt.step(range(1, 97), P_a, 'b-', label='Input Power (P_s)')
    plt.step(range(1, 97), cs, 'k-', label='Clear Sky (cs)')
    plt.xlim([1, 96])
    plt.grid(True)
    plt.legend()
    plt.show()