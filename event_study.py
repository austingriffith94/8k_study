# Austin Griffith
# 12/3/2017
# Event Studies and Sentiment Analysis
# Python 3.6.3

from datetime import datetime as dt
import pandas as pd

# use first column of dsi as Rmt
# add 2.55*10^6 to volumes that are zero

# pull returns for a given cik
# pull market returns for the year of that cik

sec = pd.read_csv('sec.csv')
dsi = pd.read_csv('dsi.csv')
dsf = pd.read_csv('dsf.csv')

cik = sec['cik'].unique()
rit = dsf[dsf['CIK'].isin([cik[25]])]

dsf['date'] = pd.to_datetime(dsf['date']).dt.date
sec['date'] = pd.to_datetime(sec['date']).dt.date

rmt = dsi[['vwretd']]
rit = dsf[['RET']]

mergen = sm.add_constant(mergen)
est = sm.OLS(merge[yh],mergen).fit()
