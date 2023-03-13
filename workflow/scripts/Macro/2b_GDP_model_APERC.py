# Solow Swan Growth estimates for APEC economies

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
import openpyxl

# Change the working drive
wanted_wd = 'macro_variables_9th'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

APEC_econcode = pd.read_csv('./data/APEC_economy_code.csv', header = None, index_col = 0)\
    .squeeze().to_dict()

# Estimates begin from 2028:
# GDP output estimates to 2027 are from the IMF

# To estimate GDP after 2027, the main inputs are:  
# 1. UN DESA population data out to 2100 (this is the labour input in the cobb douglas function)
# 2. Capital stock estimates to 2019 from PWT, that are then estimated to 2027 using an output to capital stock ratio from 2019
# 3. Derived labour efficiency estimate to 2027 (assumed to grow at a growth rate chosen) 

# Import required dataframes

UN_df = pd.read_csv('./data/UN_DESA/undesa_pop_to2100.csv')
IMF_df = pd.read_csv('./data/IMF/IMF_to2027.csv')
leff_df = pd.read_csv('./data/labour_efficiency_estimate_to2027.csv')
cap_df = pd.read_csv('./data/capital_stock.csv')

input_df = pd.concat([UN_df, IMF_df, leff_df, cap_df]).reset_index(drop = True)

input_df = input_df[(input_df['variable']\
                          .isin(['population_1jan', 'Real GDP PPP 2017 USD', 
                                 'Labour efficiency', 'Capital stock'])) &
                     (input_df['year'] >= 1980)].copy()\
                                 .reset_index(drop = True)

# Specify some parameters needed for the model

ALPHA = 0.4

# For the model

# L is given from UN_DESA
# E (derived), grow at constant rate?
# K[i+1] = K[i] - K[i] * delta + (Y[i] * s)
# Y[i+1] = K[i+1]**alpha * (L[i+1] * E[i+1])**(1-alpha))

GDP_df1 = pd.DataFrame()

for economy in APEC_econcode.values():
    pop_df1 = input_df[(input_df['economy_code'] == economy) &
                           (input_df['variable'] == 'population_1jan')].copy()\
                            [['economy_code', 'economy', 'year', 'value']]\
                                .rename(columns = {'value': 'labour'}).reset_index(drop = True)
    
    eff_df1 = input_df[(input_df['economy_code'] == economy) &
                       (input_df['variable'] == 'Labour efficiency')].copy()\
                        [['year', 'value']]\
                            .rename(columns = {'value': 'efficiency'}).reset_index(drop = True)
    
    interim_df1 = pop_df1.merge(eff_df1, 
                                how = 'left', 
                                on = 'year').copy()
    
    cap_df1 = input_df[(input_df['economy_code'] == economy) &
                       (input_df['variable'] == 'Capital stock')].copy()\
                        [['year', 'value']]\
                            .rename(columns = {'value': 'capital'}).reset_index(drop = True)
    
    interim_df2 = interim_df1.merge(cap_df1,
                                    how = 'left',
                                    on = 'year').copy()
    
    y_df1 = input_df[(input_df['economy_code'] == economy) &
                     (input_df['variable'] == 'Real GDP PPP 2017 USD')].copy()\
                        [['year', 'value']]\
                            .rename(columns = {'value': 'real_output'}).reset_index(drop = True)
    
    interim_df3 = interim_df2.merge(y_df1,
                                    how = 'left',
                                    on = 'year').copy()

    GDP_df1 = pd.concat([GDP_df1, interim_df3]).reset_index(drop = True)

GDP_df1 = GDP_df1.set_index('year', drop = True)

# Labour efficiency estimates
lab_eff = pd.read_csv('./data/labour_efficiency_estimate_to2027.csv')
lab_eff_periods = 10

GDP_df2 = pd.DataFrame()

for economy in APEC_econcode.values(): 
    # Labour efficiency calculation
    eff_df = lab_eff[lab_eff['economy_code'] == economy][['year', 'percent']]\
        .set_index('year', drop = True).iloc[-lab_eff_periods:]
    
    lab_eff_improvement = eff_df['percent'].sum() / lab_eff_periods

    # Update labour efficiency
    for year in range(2028, 2101, 1):
        if eff_df.iloc[-lab_eff_periods:].sum()[0] / lab_eff_periods > 0.013:
            eff_df.loc[year, 'percent'] = eff_df.iloc[-lab_eff_periods:].sum()[0] / lab_eff_periods - 0.002

        elif eff_df.iloc[-lab_eff_periods:].sum()[0] / lab_eff_periods < 0.01:
            eff_df.loc[year, 'percent'] = eff_df.iloc[-lab_eff_periods:].sum()[0] / lab_eff_periods + 0.001

        else: 
            eff_df.loc[year, 'percent'] = lab_eff_improvement

    # Labour efficiency
    interim_df1 = GDP_df1[GDP_df1['economy_code'] == economy].copy()
    
    for year in range (2028, 2101, 1):
        interim_df1.at[year, 'efficiency'] = interim_df1.loc[year - 1, 'efficiency'] * \
            (1 + eff_df.loc[year, 'percent'])

    GDP_df2 = pd.concat([GDP_df2, interim_df1])

GDP_df2 

# Capital and output

delta_df = pd.read_csv('./data/PWT_delta_2019.csv')
delta_df = pd.concat([delta_df, pd.DataFrame({'economy_code': '13_PNG', 'year': 2019}, index = [0])])\
    .sort_values('economy_code').reset_index(drop = True)
savings_df = pd.read_csv('./data/IMF_savings_2027.csv')

GDP_df3 = pd.DataFrame()

for economy in APEC_econcode.values():
    delta = delta_df[delta_df['economy_code'] == economy]['value'].values[0]
    savings = savings_df[savings_df['economy_code'] == economy]['value'].values[0] / 100

    interim_df1 = GDP_df2[GDP_df2['economy_code'] == economy].copy()

    # Create savings data frame
    dyn_savings = pd.DataFrame(index = range(2028, 2101, 1), columns = ['savings'])
    dyn_savings.loc[2028, 'savings'] = savings

    for year in range(2028, 2101, 1):
        if dyn_savings.loc[year, 'savings'] > 0.25:
            dyn_savings.loc[year + 1, 'savings'] = dyn_savings.loc[year, 'savings'] - 0.01
        else:
            dyn_savings.loc[year + 1, 'savings'] = dyn_savings.loc[year, 'savings']

        # Capital
        interim_df1.at[year, 'capital'] = interim_df1.loc[year - 1, 'capital']\
            - interim_df1.loc[year - 1, 'capital'] * delta\
                + interim_df1.loc[year - 1, 'real_output'] * dyn_savings.loc[year, 'savings'] 
        # Output
        interim_df1.at[year, 'real_output'] = (interim_df1.loc[year, 'capital']) ** ALPHA\
            * ((interim_df1.loc[year, 'labour'] * interim_df1.loc[year, 'efficiency']) ** (1 - ALPHA))      

    GDP_df3 = pd.concat([GDP_df3, interim_df1]) 

GDP_estimates = GDP_df3.reset_index()

# Save location for charts
GDP_est = './results/GDP_estimates/'

if not os.path.isdir(GDP_est):
    os.makedirs(GDP_est)

# GDP charts
for economy in APEC_econcode.values():
    chart_df = GDP_estimates[GDP_estimates['economy_code'] == economy]\
        .copy().reset_index(drop = True)

    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    # Population
    sns.lineplot(ax = ax,
                 data = chart_df,
                 x = 'year',
                 y = 'real_output')
      
    ax.set(title = economy + ' real GDP (PPP 2017 USD)', 
                  xlabel = 'Year', 
                  ylabel = 'Real output (millions)')
    
    plt.tight_layout()
    fig.savefig(GDP_est + economy + '_GDP_estimates.png')
    plt.close()

