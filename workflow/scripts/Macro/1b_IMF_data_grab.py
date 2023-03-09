# IMF data

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

# APEC in IMF daa

APEC = ['Australia',
        'Brunei Darussalam',
        'Canada',
        'Chile',
        'China',
        'Hong Kong SAR',
        'Indonesia',
        'Japan',
        'Korea',
        'Malaysia',
        'Mexico',
        'New Zealand',
        'Papua New Guinea',
        'Peru',
        'Philippines',
        'Russia',
        'Singapore',
        'Taiwan Province of China',
        'Thailand',
        'United States',
        'Vietnam']

IMF_df = pd.read_excel('./data/IMF/WEOOct2022all.xlsx')
IMF_df = IMF_df[IMF_df['Country'].isin(APEC)].copy().reset_index(drop = True)

# Variables required are ('Subject Descriptor'):
# Constant real GDP per capita PPP 2017 USD: NGDPRPPPPC
# Population: LP
# Total investment: NID_NGDP
# Gross national savings: NGSD_NGDP

variables = ['NGDPRPPPPC', 'LP', 'NID_NGDP', 'NGSD_NGDP']

IMF_df = IMF_df[IMF_df['WEO Subject Code'].isin(variables)].copy().reset_index(drop = True)

# Now replace economy names
dict_to_replace = {'Hong Kong SAR': 'Hong Kong, China', 
                   'Taiwan Province of China': 'Chinese Taipei',
                   'United States': 'United States of America',
                   'Vietnam': 'Viet Nam'}

IMF_df.replace(dict_to_replace, inplace = True)
IMF_df

# Update APEC list
APEC = [dict_to_replace.get(e, e) for e in APEC]
APEC

# Now calculate PPP 2017 USD for all economies (multiply real PPP GDP per capita by population)

PPP_GDP = pd.DataFrame(columns = IMF_df.columns)

for economy in APEC:
    temp_df = IMF_df[(IMF_df['Country'] == economy) &
                     (IMF_df['WEO Subject Code'].isin(variables[:2]))]\
                        .copy().reset_index(drop = True)
    
    ppp_df = temp_df[range(1980, 2028, 1)].iloc[0] * temp_df[range(1980, 2028, 1)].iloc[1]
    ppp_df['Country'] = economy
    ppp_df['Subject Descriptor'] = 'Real GDP PPP 2017 USD'

    PPP_GDP = pd.concat([PPP_GDP, pd.DataFrame(ppp_df).transpose()], axis = 0).reset_index(drop = True)
    
PPP_GDP_long = PPP_GDP.melt(id_vars = ['Country', 'Subject Descriptor'], 
                            value_vars = list(range(1980, 2028, 1)), 
                            var_name = 'Year')

# Now reshape population, investment and gross national savings

IMF_data_long = IMF_df.melt(id_vars = ['Country', 'Subject Descriptor'],
                            value_vars = list(range(1980, 2028, 1)),
                            var_name = 'Year')

# Concat the real GDP with original IMF data to create new long data frame
IMF_data_long = pd.concat([IMF_data_long, PPP_GDP_long]).reset_index(drop = True)

# Now add percent change column
IMF_data_long['percent'] = IMF_data_long.groupby(['Country', 'Subject Descriptor'], 
                                                 group_keys = False)\
                                                    ['value'].apply(pd.Series.pct_change)

IMF_data_long = IMF_data_long.rename(columns = {'Country': 'economy',
                                                'Subject Descriptor': 'variable',
                                                'Year': 'year'})

# Add in economy code

APEC_econcode = pd.read_csv('./data/APEC_economy_code.csv', header = None, index_col = 0)\
    .squeeze().to_dict()

IMF_data_long['economy_code'] = IMF_data_long['economy'].map(APEC_econcode)

IMF_data_long = IMF_data_long[['economy_code', 'economy', 'variable', 'year', 'value', 'percent']]

IMF_data_long = IMF_data_long.sort_values(['economy_code', 'variable', 'year']).copy().reset_index(drop = True)

IMF_data_long['source'] = 'IMF'

# Save csv
IMF_data_long.to_csv('./data/IMF/IMF_to2027.csv', index = False)
