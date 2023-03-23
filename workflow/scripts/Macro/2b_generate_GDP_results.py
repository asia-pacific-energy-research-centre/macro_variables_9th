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
aperc_gdp_model(economy = '05_PRC')

# 06_HKC
aperc_gdp_model(economy = '06_HKC')

# 07_INA
aperc_gdp_model(economy = '07_INA')

# 08_JPN
aperc_gdp_model(economy = '08_JPN')

# 09_ROK
aperc_gdp_model(economy = '09_ROK')

# 10_MAS
aperc_gdp_model(economy = '10_MAS')

# 11_MEX
aperc_gdp_model(economy = '11_MEX')

# 12_NZ
aperc_gdp_model(economy = '12_NZ')

# 13_PNG
aperc_gdp_model(economy = '13_PNG')

# 14_PE
aperc_gdp_model(economy = '14_PE')

# 15_RP
aperc_gdp_model(economy = '15_RP')

# 16_RUS
aperc_gdp_model(economy = '16_RUS')

# 17_SIN
aperc_gdp_model(economy = '17_SIN')

# 18_CT
aperc_gdp_model(economy = '18_CT')

# 19_THA
aperc_gdp_model(economy = '19_THA')

# 20_USA
aperc_gdp_model(economy = '20_USA')

# 21_VN
aperc_gdp_model(economy = '21_VN')

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
