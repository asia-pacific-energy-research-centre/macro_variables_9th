# IMF data sources:
gdp_current.xls - https://www.imf.org/external/datamapper/NGDPD@WEO/OEMDC/ADVEC/WEOWORLD
ppp.xls - https://www.imf.org/external/datamapper/PPPEX@WEO/OEMDC/ADVEC/WEOWORLD
gdp_ppp.xls - https://www.imf.org/external/datamapper/PPPGDP@WEO/OEMDC/ADVEC/WEOWORLD

# UN data sources:
WPP2022_TotalPopulationBySex.csv - https://population.un.org/wpp/Download/Standard/CSV/
> this is found in the table where the following details are around about: 
| Sub Group | Files (click to download) | Description |
| --- | --- | --- |
| Population | 1950-2100, all scenarios (ZIP, 10.52 MB) | Total Population on 01 July. |
# OECD data sources (only for OECD economys)
GDPLTFORECAST.csv - https://data.oecd.org/gdp/real-gdp-long-term-forecast.htm
PPP.csv - https://data.oecd.org/conversion/purchasing-power-parities-ppp.htm
real_gdp_growth_short_term_forecast.csv - https://data.oecd.org/gdp/real-gdp-forecast.htm#indicator-chart
nominal_gdp_growth_short_term_forecast.csv - https://data.oecd.org/gdp/nominal-gdp-forecast.htm#indicator-chart

# World bank data sources (Doesnt include taiwan)
Why use dec_alternative_LCU_to_USD_conversion_factor instead of exchange rates to convert local currency GDP to USD GDP: https://datahelpdesk.worldbank.org/knowledgebase/articles/77935-what-is-the-dec-conversion-factor
- although they are basically the same from analysis

dec_alternative_LCU_to_USD_conversion_factor.csv - https://data.worldbank.org/indicator/PA.NUS.ATLS?view=map&year=2021
LCU_to_USD_exchange_rate.csv - https://data.worldbank.org/indicator/PA.NUS.FCRF?view=map&year=2021

# Now that we have scripts to clean this data it is easy to get more