# UN DESA

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
        'China, Taiwan Province of China',
        'Thailand',
        'United States of America',
        'Viet Nam']

# All variants except 'Medium'
variant = ['High',
           'Medium',
           'Low',
           'Constant fertility',
           'Instant replacement',
           'Zero migration',
           'Constant mortality',
           'No change',
           'Momentum',
           'Instant replacement zero migration',
           'Median PI',
           'Upper 80 PI'
           'Lower 80 PI',
           'Upper 95 PI',
           'Lower 95 PI']

# Grab histroical data and medium scenario
undesa_hist = pd.read_csv("../../data/UN_DESA/WPP2022_Demographic_Indicators_Medium.csv")
undesa_hist = undesa_hist[undesa_hist['Location'].isin(APEC)].copy().reset_index(drop = True)

# Only keep variables of interest
undesa_hist = undesa_hist[['Location', 'Variant', 'Time', 'TPopulation1Jan', 'TPopulation1July', 'NetMigrations']].copy()

# Projections to 2100 from UN DESA csv
undesa_proj = pd.read_csv("../../data/UN_DESA/WPP2022_Demographic_Indicators_OtherVariants.csv")

# Subset so only APEC economies
undesa_proj = undesa_proj[undesa_proj['Location'].isin(APEC)].copy().reset_index(drop = True)
undesa_proj['Location'].unique()

# Only keep variables of interest
undesa_proj = undesa_proj[['Location', 'Variant', 'Time', 'TPopulation1Jan', 'TPopulation1July', 'NetMigrations']].copy()

# Concatenate medium scenario (including historical) with all other scenarios
undesa_apec = pd.concat([undesa_hist, undesa_proj]).copy().reset_index(drop = True)

dict_to_replace = {'China, Hong Kong SAR': 'Hong Kong, China', 
                   'Republic of Korea': 'Korea',
                   'Russian Federation': 'Russia',
                   'China, Taiwan Province of China': 'Chinese Taipei'}

undesa_apec.replace(dict_to_replace, inplace = True)

# Update APEC list
APEC = [dict_to_replace.get(e, e) for e in APEC]
APEC

# Colour palette for charts (15 categories) 
palette = sns.color_palette('rocket', 15)

# Save location for charts
population_charts = '../../results/population/'

if not os.path.isdir(population_charts):
    os.makedirs(population_charts)

for economy in APEC:
    chart_df = undesa_apec[undesa_apec['Location'] == economy].copy().reset_index(drop = True)
    chart_df['TPopulation1Jan'] = chart_df['TPopulation1Jan'] / 1000

    sizes = {a: 1 for a in chart_df['Variant'].unique()}
    med = {'Medium': 4}
    sizes.update(med)

    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')
    sns.lineplot(ax = ax,
                 data = chart_df,
                 x = 'Time',
                      y = 'TPopulation1Jan',
                      hue = 'Variant',
                      palette = palette,
                      size = 'Variant',
                      sizes = sizes)
      
    ax.set(title = economy + ' population projections to 2100 (UN DESA)', 
           xlabel = 'Year', 
           ylabel = 'Population (millions)', 
           ylim = (0, max(chart_df['TPopulation1Jan']) * 1.1),
           xlim = (min(chart_df['Time']), 2100))

    plt.legend(title = '', fontsize = 7)

    plt.tight_layout()
    fig.savefig(population_charts + economy + '_population.png')
    plt.close()

    
