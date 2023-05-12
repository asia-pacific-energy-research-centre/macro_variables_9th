# Solow Swan Growth estimates for APEC economies

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
import openpyxl

# FOR NOW: Run 2a GDP_model_APERC prior to executing this script
# Import function from prior script
# from GDP_model_APERC import aperc_gdp_model

# Change the working drive
wanted_wd = 'macro_variables_9th'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# APEC economy codes
APEC_econcode = pd.read_csv('./data/APEC_economy_code.csv', header = None, index_col = 0)\
    .squeeze().to_dict()

# Generate economy specific results using the aperc_gdp_model function
# 01_AUS
aperc_gdp_model(economy = '01_AUS')

# 02_BD
aperc_gdp_model(economy = '02_BD')

# 03_CDA
aperc_gdp_model(economy = '03_CDA')

# 04_CHL
aperc_gdp_model(economy = '04_CHL')

# 05_PRC
aperc_gdp_model(economy = '05_PRC', change_sav = 0.01, change_eff = 0.004)

# 06_HKC
aperc_gdp_model(economy = '06_HKC', low_sav = 0.24, change_sav = 0.01)

# 07_INA
aperc_gdp_model(economy = '07_INA', lab_eff_periods = 5, high_eff = 0.03, low_delta = 0.04)

# 08_JPN
aperc_gdp_model(economy = '08_JPN')

# 09_ROK
aperc_gdp_model(economy = '09_ROK', low_eff = 0.010, high_eff = 0.0125)

# 10_MAS
aperc_gdp_model(economy = '10_MAS', high_eff = 0.025)

# 11_MEX
aperc_gdp_model(economy = '11_MEX', low_sav = 0.24)

# 12_NZ
aperc_gdp_model(economy = '12_NZ')

# 13_PNG
aperc_gdp_model(economy = '13_PNG', lab_eff_periods = 5, low_eff = 0.035, high_eff = 0.04, low_sav = 0.29, high_sav = 0.3)

# 14_PE
aperc_gdp_model(economy = '14_PE')

# 15_RP
aperc_gdp_model(economy = '15_RP')

# 16_RUS
aperc_gdp_model(economy = '16_RUS')

# 17_SIN
aperc_gdp_model(economy = '17_SIN', high_eff = 0.01, low_eff = 0.007)

# 18_CT
aperc_gdp_model(economy = '18_CT', lab_eff_periods = 5, high_eff = 0.012, low_eff = 0.01)

# 19_THA
aperc_gdp_model(economy = '19_THA', high_eff = 0.025)

# 20_USA
aperc_gdp_model(economy = '20_USA')

# 21_VN
aperc_gdp_model(economy = '21_VN', change_sav = 0.01, low_eff = 0.01, change_eff = 0.005)

# Run all economies with defaults aperc_gdp_model settings 
# for economy in APEC_econcode.values():
#     aperc_gdp_model(economy = economy)

# Data location
GDP_data = './results/GDP_estimates/data/'

if not os.path.isdir(GDP_data):
    os.makedirs(GDP_data)

# Save a combined dataframe from the results generated above
combined_df = pd.DataFrame()

for economy in APEC_econcode.values():
    # Path to file
    if os.path.exists(GDP_data + '{}_GDP_estimate.csv'.format(economy)) == True:

        # Read data
        individual_df = pd.read_csv(GDP_data + '{}_GDP_estimate.csv'.format(economy))
        combined_df = pd.concat([combined_df, individual_df]).reset_index(drop = True)

    else:
        pass

# Write combined data frame
combined_df.to_csv(GDP_data + 'combined_GDP_estimate.csv', index = False)

# Generate some quick GDP per capita charts
APEC_gdp_pop = combined_df.pivot(columns = 'variable', 
                                 values = 'value', 
                                 index = ['economy_code', 'economy', 'year']).copy()\
                                    .reset_index(drop = False)

APEC_gdp_pop['real_GDP'] = np.where(APEC_gdp_pop['year'] <= 2027, 
                                    APEC_gdp_pop['IMF GDP projections to 2027'],
                                    APEC_gdp_pop['APERC real GDP projections from 2027'])

APEC_gdp_pop = APEC_gdp_pop[['economy_code', 'economy', 'year', 'real_GDP', 
                             'Population', 'Labour efficiency', 'Depreciation',
                             'Savings', 'Capital stock']].copy()\
                                .rename(columns = {'Population': 'population',
                                                   'Labour efficiency': 'lab_eff',
                                                   'Depreciation': 'depreciation',
                                                   'Savings': 'savings',
                                                   'Capital stock': 'k_stock'})

APEC_gdp_pop['GDP_per_capita'] = APEC_gdp_pop['real_GDP'] / APEC_gdp_pop['population'] * 1000

APEC_gdp_pop = APEC_gdp_pop.melt(id_vars = ['economy_code', 'economy', 'year']).copy()
APEC_gdp_pop.to_csv(GDP_data + 'APEC_GDP_data.csv', index = False)

# Save space for GDP per capita charts
GDP_pc = './results/GDP_estimates/per_capita/'

if not os.path.isdir(GDP_pc):
    os.makedirs(GDP_pc)

# Generate a dataframe that is only gdp and population
for economy in APEC_econcode.values():
    chart_df = APEC_gdp_pop[(APEC_gdp_pop['economy_code'] == economy) &
                            (APEC_gdp_pop['variable'] == 'GDP_per_capita')]\
        .copy().reset_index(drop = True)
    
    fig, ax = plt.subplots()
    
    sns.set_theme(style = 'ticks')

    # Capital stock
    sns.lineplot(ax = ax,
                 data = chart_df,
                 x = 'year',
                 y = 'value')
    
    ax.set(title = economy + ' real GDP per capita', 
                xlabel = 'Year', 
                ylabel = 'GDP per capita (USD 2017 PPP)',
                xlim = (1980, 2070),
                ylim = (0))
    
    plt.tight_layout()
    fig.savefig(GDP_pc + economy + '_gdp_pc.png')
    plt.close()

# APEC GDP per capita
palette = sns.color_palette('rocket', 21)
fig, ax = plt.subplots()

sns.set_theme(style = 'ticks')

sns.lineplot(ax = ax,
             data = APEC_gdp_pop[APEC_gdp_pop['variable'] == 'GDP_per_capita'],
             x = 'year',
             y = 'value', 
             hue = 'economy', 
             palette = palette)

ax.set(title = 'GDP per capita (USD 2017 PPP)',
       xlabel = 'Year',
       ylabel = 'GDP per capita',
       xlim = (1980, 2070),
       ylim = (0))

plt.legend(title = '',
           fontsize = 7)

plt.tight_layout()
fig.savefig(GDP_pc + 'APEC_gdp_pc.png')
plt.close()

# Create charts for all relevant results people want to see
GDP_results = './results/GDP_estimates/input_data/'

if not os.path.isdir(GDP_results):
    os.makedirs(GDP_results)

# Generate a dataframe that is only gdp and population
for economy in APEC_econcode.values():
    rGDP_df = APEC_gdp_pop[(APEC_gdp_pop['economy_code'] == economy) &
                            (APEC_gdp_pop['variable'] == 'real_GDP') &
                            (APEC_gdp_pop['year'] <= 2070)]\
                                .copy().reset_index(drop = True)
    
    rGDPpc_df = APEC_gdp_pop[(APEC_gdp_pop['economy_code'] == economy) &
                            (APEC_gdp_pop['variable'] == 'GDP_per_capita')]\
                                .copy().reset_index(drop = True)
    
    leff_df = APEC_gdp_pop[(APEC_gdp_pop['economy_code'] == economy) &
                            (APEC_gdp_pop['variable'] == 'lab_eff') &
                            (APEC_gdp_pop['year'] <= 2070)]\
                                .copy().reset_index(drop = True)
    
    # Grab growth in labour efficiency
    leff_growth = leff_df.copy()
    
    leff_growth['percent'] = leff_growth.groupby(['economy', 'variable'], 
                                                 group_keys = False)\
                                                    ['value'].apply(pd.Series.pct_change)
    
    dep_df = APEC_gdp_pop[(APEC_gdp_pop['economy_code'] == economy) &
                            (APEC_gdp_pop['variable'] == 'depreciation') &
                            (APEC_gdp_pop['year'] <= 2070)]\
                                .copy().reset_index(drop = True)
    
    sav_df = APEC_gdp_pop[(APEC_gdp_pop['economy_code'] == economy) &
                            (APEC_gdp_pop['variable'] == 'savings') &
                            (APEC_gdp_pop['year'] <= 2070)]\
                                .copy().reset_index(drop = True)
    
    k_df = APEC_gdp_pop[(APEC_gdp_pop['economy_code'] == economy) &
                            (APEC_gdp_pop['variable'] == 'k_stock') &
                            (APEC_gdp_pop['year'] <= 2070)]\
                                .copy().reset_index(drop = True)
    
    pop_df = APEC_gdp_pop[(APEC_gdp_pop['economy_code'] == economy) &
                            (APEC_gdp_pop['variable'] == 'population') &
                            (APEC_gdp_pop['year'] <= 2070)]\
                                .copy().reset_index(drop = True)
    
    fig, ax = plt.subplots(2, 3)
    
    sns.set_theme(style = 'ticks')

    # GDP
    sns.lineplot(ax = ax[0, 0],
                 data = rGDP_df,
                 x = 'year',
                 y = 'value')
    
    ax[0, 0].set(title = economy + ' real GDP', 
                xlabel = 'Year', 
                ylabel = 'GDP (USD 2017 PPP)',
                xlim = (1980, 2070),
                ylim = (0))
    
    # leff
    sns.lineplot(ax = ax[0, 1],
                 data = leff_growth,
                 x = 'year',
                 y = 'percent')
    
    ax[0, 1].set(title = economy + ' labour efficiency', 
                xlabel = 'Year', 
                ylabel = 'Labour efficiency',
                xlim = (1980, 2070),
                ylim = (np.nanmin(leff_growth['percent']) * 1.1, np.nanmax(leff_growth['percent']) * 1.1))
    
    # depreciation
    sns.lineplot(ax = ax[0, 2],
                 data = dep_df,
                 x = 'year',
                 y = 'value')
    
    ax[0, 2].set(title = economy + ' depreciation', 
                xlabel = 'Year', 
                ylabel = 'Depreciation',
                xlim = (1980, 2070),
                ylim = (0, np.nanmax(dep_df['value']) * 1.1))
    
    # savings
    sns.lineplot(ax = ax[1, 0],
                 data = sav_df,
                 x = 'year',
                 y = 'value')
    
    ax[1, 0].set(title = economy + ' savings (% GDP)', 
                xlabel = 'Year', 
                ylabel = 'Savings',
                xlim = (1980, 2070),
                ylim = (0, np.nanmax(sav_df['value']) * 1.1))
    
    # K stock
    sns.lineplot(ax = ax[1, 1],
                 data = k_df,
                 x = 'year',
                 y = 'value')
    
    ax[1, 1].set(title = economy + ' capital stock', 
                xlabel = 'Year', 
                ylabel = 'Capital stock',
                xlim = (1980, 2070),
                ylim = (0, np.nanmax(k_df['value']) * 1.1))
    
    # Population
    sns.lineplot(ax = ax[1, 2],
                 data = pop_df,
                 x = 'year',
                 y = 'value')
    
    ax[1, 2].set(title = economy + ' population', 
                xlabel = 'Year', 
                ylabel = 'Population',
                xlim = (1980, 2070),
                ylim = (0, np.nanmax(pop_df['value']) * 1.1))
    
    plt.tight_layout()
    fig.savefig(GDP_results + economy + '_gdp_results.png')
    plt.close()