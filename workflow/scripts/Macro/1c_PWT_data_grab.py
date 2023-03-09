# PWT data grab

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

# APEC in PWT

APEC = ['Australia',
        'Brunei Darussalam',
        'Canada',
        'Chile',
        'China',
        'China, Hong Kong SAR',
        'Indonesia',
        'Japan',
        'Republic of Korea',
        'Malaysia',
        'Mexico',
        'New Zealand',
        'Papua New Guinea',
        'Peru',
        'Philippines',
        'Russian Federation',
        'Singapore',
        'Taiwan',
        'Thailand',
        'United States',
        'Viet Nam']

PWT_df = pd.read_excel('./data/PWT/pwt1001.xlsx', sheet_name = 'Data')
PWT_df

PWT_df = PWT_df[PWT_df['country'].isin(APEC)].copy().reset_index(drop = True)
PWT_df = PWT_df.loc[:, ['country', 'year', 'pop', 'emp', 'avh', 'rgdpna', 'rnna', 'rtfpna', 'delta']]\
    .copy().reset_index(drop = True)

PWT_df = PWT_df.rename(columns = {'country': 'economy',
                                  'pop': 'population',
                                  'emp': 'employed',
                                  'avh': 'avg_hours'})

# Update economy names

dict_to_replace = {'China, Hong Kong SAR': 'Hong Kong, China', 
                   'Republic of Korea': 'Korea',
                   'Russian Federation': 'Russia',
                   'Taiwan': 'Chinese Taipei',
                   'United States': 'United States of America'}

PWT_df.replace(dict_to_replace, inplace = True)

# Update APEC list
APEC = [dict_to_replace.get(e, e) for e in APEC]
APEC

# Create new variable

PWT_df['output_to_kstock'] = PWT_df['rgdpna'] / PWT_df['rnna']

# Colour palette for charts (15 categories) 
palette = sns.color_palette('rocket', 15)

# Save location for charts
cap_labour_charts = './results/PWT_data/'

if not os.path.isdir(cap_labour_charts):
    os.makedirs(cap_labour_charts)

for economy in APEC:
    chart_df = PWT_df[PWT_df['economy'] == economy].copy().reset_index(drop = True)

    fig, axs = plt.subplots(2, 2)

    sns.set_theme(style = 'ticks')

    # Population
    sns.lineplot(ax = axs[0, 0],
                 data = chart_df,
                 x = 'year',
                 y = 'population')
      
    axs[0, 0].set(title = economy + ' PWT population', 
                  xlabel = 'Year', 
                  ylabel = 'Population (millions)')
    
    # Capital stock
    sns.lineplot(ax = axs[0, 1],
                 data = chart_df,
                 x = 'year',
                 y = 'rnna')
      
    axs[0, 1].set(title = economy + ' PWT capital stock', 
                  xlabel = 'Year', 
                  ylabel = 'Real capital stock')
    
    # GDP
    sns.lineplot(ax = axs[1, 0],
                 data = chart_df,
                 x = 'year',
                 y = 'rgdpna')
      
    axs[1, 0].set(title = economy + ' PWT real GDP', 
                  xlabel = 'Year', 
                  ylabel = 'Real GDP (millions)')
    
    # Depreciation
    sns.lineplot(ax = axs[1, 1],
                 data = chart_df,
                 x = 'year',
                 y = 'delta')
      
    axs[1, 1].set(title = economy + ' PWT depreciation', 
                  xlabel = 'Year', 
                  ylabel = 'Depreciation')


    plt.tight_layout()
    fig.savefig(cap_labour_charts + economy + '_PWT_data.png')
    plt.close()

for economy in APEC:
    chart_df = PWT_df[PWT_df['economy'] == economy].copy().reset_index(drop = True)
    chart_df['output_to_cap'] = chart_df['rgdpna'] / chart_df['rnna']

    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    # Population
    sns.lineplot(ax = ax,
                 data = chart_df,
                 x = 'year',
                 y = 'output_to_cap')
      
    ax.set(title = economy + ' PWT output to capital stock', 
                  xlabel = 'Year', 
                  ylabel = 'Output to capital ratio')
    
    plt.tight_layout()
    fig.savefig(cap_labour_charts + economy + '_output_cap.png')
    plt.close()


# Create long dataframe
# Add in economy code

APEC_econcode = pd.read_csv('./data/APEC_economy_code.csv', header = None, index_col = 0)\
    .squeeze().to_dict()

APEC_econcode

PWT_df['economy_code'] = PWT_df['economy'].map(APEC_econcode)
PWT_df['economy'].unique()

PWT_df = PWT_df.melt(id_vars = ['economy_code', 'economy', 'year'],
                     value_vars = ['employed', 'avg_hours', 'rgdpna', 'rnna', 'rtfpna', 'delta', 'output_to_kstock'])\
                        .reset_index(drop = True)

# Now add percent change column
PWT_df['percent'] = PWT_df.groupby(['economy', 'variable'], 
                                   group_keys = False)\
                                    ['value'].apply(pd.Series.pct_change)

PWT_df = PWT_df.sort_values(['economy_code', 'year']).copy().reset_index(drop = True)

PWT_df['source'] = 'PWT'

PWT_df.to_csv('./data/PWT/PWT_cap_labour_to2019.csv', index = False)
