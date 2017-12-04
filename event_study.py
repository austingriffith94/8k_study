# Austin Griffith
# 12/3/2017
# Event Studies and Sentiment Analysis
# Python 3.6.3

from datetime import datetime as dt
import pandas as pd
import time

# use first column of dsi as Rmt
# add 2.55*10^6 to volumes that are zero

# pull returns for a given cik
# pull market returns for the year of that cik

sec = pd.read_csv('sec.csv')
dsi = pd.read_csv('dsi.csv')
dsf = pd.read_csv('dsf.csv')
dsf['date'] = pd.to_datetime(dsf['date']).dt.date
sec['date'] = pd.to_datetime(sec['date']).dt.date
dsi['DATE'] = pd.to_datetime(dsi['DATE'], format='%Y%m%d').dt.date

cik = sec['cik'].unique()

for i in cik:
    rit = dsf[dsf['CIK'].isin([i])]
    if rit.empty == False:
        year = rit['obs_year'].iloc[0]

i = cik[43]
rit = dsf[dsf['CIK'].isin([i])]
# if statement to check rit
year_v = rit['dsf_year'].iloc[0]
market = dsi.loc[dsi['year'] == year_v]
x = pd.DataFrame(market[['vwretd','DATE']])
x = x.reset_index(drop=True)
x = x.set_index('DATE')
y = pd.DataFrame(rit[['RET','date']])
y = y.reset_index(drop=True)
y = y.set_index('date')
merge = pd.merge(x, y, how='inner', left_index=True, right_index=True)




