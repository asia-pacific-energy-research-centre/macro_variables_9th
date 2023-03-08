# Building combined data frame to generate capital, labour, depreciation, savings, etc to 2027
# Run a, b, and c script before this one.

# Change the working drive
wanted_wd = 'macro_variables_9th'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

APEC_econcode = pd.read_csv('./data/APEC_economy_code.csv', header = None, index_col = 0)\
    .squeeze().to_dict()

UN_df_long = pd.read_csv('./data/UN_DESA/undesa_pop_to2100.csv')
IMF_df_long = pd.read_csv('./data/IMF/IMF_to2027.csv')
PWT_df_long = pd.read_csv('./data/PWT/PWT_cap_labour_to2019.csv')


# Use output to capital stock from PWT_df to generate capital variable in IMF data 

capital_df = pd.DataFrame(columns = IMF_df_long.columns)

for economy in APEC_econcode.values():
    IMF_temp = IMF_df_long[(IMF_df_long['economy_code'] == economy) & 
                           (IMF_df_long['variable'] == 'Real GDP PPP 2017 USD')]\
                            .copy().set_index('year')
    
    PWT_temp = PWT_df_long[(PWT_df_long['economy_code'] == economy) & 
                           (PWT_df_long['variable'] == 'output_to_kstock')]\
                            .copy().set_index('year')[['value']].rename(columns = {'value': 'ratio'})
    
    capital_stock = pd.concat([IMF_temp, PWT_temp], axis = 1).loc[1980: 2027, :]

    for i in range(2020, 2028, 1):
        capital_stock.loc[i, 'ratio'] = capital_stock.loc[i - 1, 'ratio']

    capital_stock['capital'] = capital_stock['value'] / capital_stock['ratio']
    capital_stock['variable'] = 'Capital stock'
    capital_stock['source'] = 'IMF and PWT calculation'

    capital_stock = capital_stock.reset_index(drop = False)\
        [['economy_code', 'economy', 'year', 'variable', 'capital', 'source']]\
            .rename(columns = {'capital': 'value'})
    
    capital_stock['percent'] = capital_stock.groupby(['economy', 'variable'],
                                                     group_keys = False)\
                                                        ['value'].apply(pd.Series.pct_change)
    
    capital_df = pd.concat([capital_df, capital_stock], axis = 0).reset_index(drop = True)

# Estimating efficiency of Labour, E

ALPHA = 0.4

# Create Dataframe that has labour (UN population), capital and GDP (real GDP PPP 2017 USD)

IMF_subset = IMF_df_long[IMF_df_long['variable'] == 'Real GDP PPP 2017 USD'].copy().reset_index(drop = True)
UN_subset = UN_df_long[(UN_df_long['variable'] == 'population_1jan') &
                       (UN_df_long['year'].isin(range(1980, 2028, 1)))].copy().reset_index(drop = True)

E_calc_df = pd.concat([IMF_subset.copy(), 
                       UN_subset.copy(), 
                       capital_df.copy()]).reset_index(drop = True)

# Combined dataframe for Labour efficiency calculation

E_estimate = pd.DataFrame()

for economy in APEC_econcode.values():
    labour_df = E_calc_df[(E_calc_df['economy_code'] == economy) &
                          (E_calc_df['variable'] == 'population_1jan')]\
                            .copy().set_index('year')

    labour_df['L^1-alpha'] = labour_df['value'] ** (1 - ALPHA)
    labour_df = labour_df[['economy_code', 'economy', 'L^1-alpha']]

    k_df = E_calc_df[(E_calc_df['economy_code'] == economy) &
                     (E_calc_df['variable'] == 'Capital stock')]\
                        .copy().set_index('year') 
    
    k_df['K^alpha'] = k_df['value'] ** ALPHA
    k_df = k_df[['K^alpha']]

    y_df = E_calc_df[(E_calc_df['economy_code'] == economy) &
                     (E_calc_df['variable'] == 'Real GDP PPP 2017 USD')]\
                        .copy().set_index('year')[['value']].rename(columns = {'value': 'Output_y'})

    eqn_df = pd.concat([y_df, labour_df, k_df], axis = 1)

    eqn_df['E'] = (eqn_df['Output_y'] / (eqn_df['L^1-alpha'] * eqn_df['K^alpha'])) ** (1/ (1 - ALPHA))
    eqn_df = eqn_df.reset_index(drop = False)\
        [['year', 'economy_code', 'economy', 'Output_y', 'L^1-alpha', 'K^alpha', 'E']]

    E_estimate = pd.concat([E_estimate, eqn_df]).reset_index(drop = True)

E_estimate



E_calc_df

UN_df_long
IMF_df_long.variable.unique()
PWT_df_long.variable.unique()

IMF_data_long.variable.unique()



IMF_data_long.variable.unique()

# Projecting K PWT from 2019 to 2027

# Requirements:
# Y = f(K, L)
# K[i + 1] = K[i] - (K[i] * delta) + (Y[i] * s)
# Y[i] = K[i]^0.4 * L[i] * 0.6 * E 

