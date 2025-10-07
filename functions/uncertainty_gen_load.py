# -*- coding: utf-8 -*-
"""
Created on Sat Aug 23 12:18:10 2025

@author: Babu Kumaran Nalini, M.Sc. 
@email: babu.kumaran-nalini@tum.de
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% functions
def mape(a, g):
    return np.nansum(np.abs((g - a) / a)) / np.size(a)  # Mean Absolute Percentage Error, MAPE

def gaussGen(x_a, E_s):
    x_a = x_a.where(x_a > 0, 0)
    x_g = np.zeros_like(x_a)  # Initialize generated array
    n = 0  # Number of iterations

    while True:
        for i in range(len(x_a)):
            x_g[i] = x_a[i] + np.random.normal(0, E_s * np.mean(x_a))  # Generate Gaussian noise

            if x_g[i] < 0:
                x_g[i] = 0  # Limiting loads: P(t) >= 0
                
        n += 1

        current_mape = mape(x_a, x_g)
        
        if abs(current_mape - E_s) <= 0.001:
            break  # Break the loop if the gap is less than 0.001

    feedback = abs(current_mape - E_s)  # Solution gap feedback
    return x_g, feedback, n

#%% 
if __name__ == '__main__':
    profiles = pd.read_csv('data/load.csv')
    
    d = 40  # Day of the Year
    t = np.arange(1, 97)  # 1-96th 15-min of day 'd'
    
    P_a = profiles.iloc[0:96, 0].values  # actual load profile import
    
    # Uncertain load profile generation
    P_g, fb, n = gaussGen(P_a, 0.1)
    
    # Checking results
    print(f"Feedback: {fb}, Iterations: {n}")  # Feedback from the gaussGen function
    error = mape(P_a, P_g)  # MAPE of the original and the generated time series
    print(f"MAPE: {error:.2f}%")
    
    # Plotting data
    plt.step(t, P_g, color='red', label='Generated Load')
    plt.step(t, P_a, color='black', label='Actual Load')
    plt.xlim([0, 96])
    plt.grid(True)
    plt.title('Uncertain Load Profile Generation')
    plt.xlabel('Time [15-min]')
    plt.ylabel('Load [W]')
    plt.legend()
    plt.show()
