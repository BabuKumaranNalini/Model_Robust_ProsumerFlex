# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 00:47:41 2025

@author: babuk
"""

import pandas as pd

def get_flex_envelope_dataframe(ems):
    nsteps = ems['time_data']['nsteps']
    
    # Initialize lists to store max values
    cols = ['Sch_P', 'Neg_P', 'Pos_P', 'Neg_E', 'Pos_E', 'Neg_Pr', 'Pos_Pr']
    df_flex_envelope = pd.DataFrame(data=0.00, index=list(range(nsteps)),columns=cols)
    
    # Extract flexopts data
    flex_opts = ems['flexopts']
    
    # Iterate through each timestamp
    for i in range(nsteps):
        # scheduled power
        df_flex_envelope.loc[i,'Sch_P'] += ems['optplan']['grid_export'][i]- ems['optplan']['grid_import'][i]
        for device in list(flex_opts.keys()):
            # Negative flex
            if flex_opts[device].loc[i,'Neg_P'] <= df_flex_envelope.loc[i,'Neg_P']:
                df_flex_envelope.loc[i,'Neg_P'] = flex_opts[device].loc[i,'Neg_P']
                df_flex_envelope.loc[i,'Neg_E'] = flex_opts[device].loc[i,'Neg_E']
                df_flex_envelope.loc[i,'Neg_Pr'] = flex_opts[device].loc[i,'Neg_Pr']
                
            # Positive flex
            if  flex_opts[device].loc[i,'Pos_P'] >= df_flex_envelope.loc[i,'Pos_P']: 
                df_flex_envelope.loc[i,'Pos_P'] = flex_opts[device].loc[i,'Pos_P']
                df_flex_envelope.loc[i,'Pos_E'] = flex_opts[device].loc[i,'Pos_E']
                df_flex_envelope.loc[i,'Pos_Pr'] = flex_opts[device].loc[i,'Pos_Pr']
            
    return df_flex_envelope