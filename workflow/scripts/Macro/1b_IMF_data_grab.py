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

    PPP_GDP = PPP_GDP.append([ppp_df]).reset_index(drop = True)
    
PPP_GDP_long = PPP_GDP.melt(id_vars = ['Country', 'Subject Descriptor'], 
                            value_vars = list(range(1980, 2028, 1)), 
                            var_name = 'Year')

PPP_GDP_long['percent change'] = PPP_GDP_long.groupby(['Country'], 
                                                      group_keys = False)\
                                                        ['value']\
                                                            .apply(pd.Series.pct_change)

PPP_GDP_long[PPP_GDP_long['Year'] == 2020]