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
aperc_gdp_model(economy = '04_CHL', lab_eff_periods = 5, low_eff = 0.017, high_eff = 0.024, low_sav = 0.25, high_delta = 0.04, low_delta = 0.039)

# 05_PRC
aperc_gdp_model(economy = '05_PRC', high_sav = 0.27, change_sav = 0.01)

# 06_HKC
aperc_gdp_model(economy = '06_HKC', high_eff = 0.02)

# 07_INA
aperc_gdp_model(economy = '07_INA', lab_eff_periods = 5, high_eff = 0.03, low_delta = 0.04)

# 08_JPN
aperc_gdp_model(economy = '08_JPN', lab_eff_periods = 5)

# 09_ROK
aperc_gdp_model(economy = '09_ROK', low_eff = 0.011, high_eff = 0.0125, high_sav = 0.25)

# 10_MAS
aperc_gdp_model(economy = '10_MAS')

# 11_MEX
aperc_gdp_model(economy = '11_MEX', lab_eff_periods = 3, low_sav = 0.25)

# 12_NZ
aperc_gdp_model(economy = '12_NZ', low_eff = 0.012)

# 13_PNG
aperc_gdp_model(economy = '13_PNG', lab_eff_periods = 5, low_eff = 0.035, high_eff = 0.04, low_sav = 0.29)

# 14_PE
aperc_gdp_model(economy = '14_PE', lab_eff_periods = 5, low_eff = 0.025, high_eff = 0.0275)

# 15_RP
aperc_gdp_model(economy = '15_RP', lab_eff_periods = 5, low_eff = 0.02, high_eff = 0.023)

# 16_RUS
aperc_gdp_model(economy = '16_RUS')

# 17_SIN
aperc_gdp_model(economy = '17_SIN', high_eff = 0.009, low_eff = 0.008)

# 18_CT
aperc_gdp_model(economy = '18_CT', lab_eff_periods = 5, high_eff = 0.011, low_eff = 0.01, 
                change_eff = 0.005, high_sav = 0.25, change_sav = 0.02)

# 19_THA
aperc_gdp_model(economy = '19_THA', lab_eff_periods = 5, high_eff = 0.025)

# 20_USA
aperc_gdp_model(economy = '20_USA', lab_eff_periods = 5)

# 21_VN
aperc_gdp_model(economy = '21_VN', lab_eff_periods = 5)

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
# combined_df.to_csv(GDP_data + 'combined_GDP_estimate.csv', index = False)

# Generate some quick GDP per capita charts
APEC_gdp_pop = combined_df.pivot(columns = 'variable', 
                                 values = 'value', 
                                 index = ['economy_code', 'economy', 'year']).copy()\
                                    .reset_index(drop = False)

APEC_gdp_pop['real_GDP'] = np.where(APEC_gdp_pop['year'] <= 2027, 
                                    APEC_gdp_pop['IMF GDP projections to 2027'],
                                    APEC_gdp_pop['APERC real GDP projections from 2027'])

APEC_gdp_pop = APEC_gdp_pop[['economy_code', 'economy', 'year', 'real_GDP', 'Population']].copy().rename(columns = {'Population': 'population'})
APEC_gdp_pop['GDP_per_capita'] = APEC_gdp_pop['real_GDP'] / APEC_gdp_pop['population'] * 1000

APEC_gdp_pop = APEC_gdp_pop.melt(id_vars = ['economy_code', 'economy', 'year']).copy()
APEC_gdp_pop.to_csv(GDP_data + 'APEC_GDP_population.csv', index = False)

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