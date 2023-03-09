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

leff_df
