# Austin Griffith
# 12/3/2017
# Event Studies and Sentiment Analysis
# Python 3.6.3

import statsmodels.api as sm
from datetime import datetime as dt
import pandas as pd
import numpy as np
import time
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.stats import norm

# use first column of dsi as Rmt
# add 2.55*10^6 to volumes that are zero
# log(vol/shrout + c)

# pull returns for a given cik
# pull market returns for the year of that cik
# log of day i - average of window (11 - 71) divided by std dev of window (11-71)
# pandas.describe to get descriptive stats

# abnormal class
class abnormal:
    def __init__(self,sec,dsf,dsi):
        self.sec = sec
        self.dsf = dsf
        self.dsi = dsi

    # models alpha and beta values from previous year returns
    def ret_model(self):
        ciks = self.sec.drop_duplicates(subset='cik')
        ciks = ciks.reset_index(drop=True)
        coef = pd.DataFrame([])

        for i in range(0,ciks.shape[0]):
            rit = self.dsf[self.dsf['CIK'].isin([ciks['cik'][i]])]
            if rit.empty == False:
                year_v = rit['dsf_year'].iloc[0]
                market = self.dsi.loc[self.dsi['year'] == year_v]
                x = pd.DataFrame(market[['vwretd','DATE']])
                x = x.reset_index(drop=True)
                x = x.set_index('DATE')
                y = pd.DataFrame(rit[['RET','date']])
                y = y.reset_index(drop=True)
                y = y.set_index('date')
                merge = pd.merge(x, y, how='inner', left_index=True, right_index=True)
                merge.dropna(inplace=True)
                x = pd.DataFrame(merge['vwretd'])
                x = sm.add_constant(x)
                y = pd.DataFrame(merge['RET'])
                model = sm.OLS(y.astype(float),x.astype(float)).fit()
                # model.summary()
                # model.params
                par = model.params.to_frame().transpose()
                ind = pd.DataFrame([{'cik':ciks['cik'][i]}])
                final = pd.concat([par,ind], axis=1)
                coef = coef.append(final)
        coef = coef.reset_index(drop=True)
        return(coef)

    # calculates abnormal returns around 8-k filing dates using alpha and beta coefficients
    def abret(self,coef):
        ciks = self.sec.drop_duplicates(subset='cik')
        ciks = ciks.reset_index(drop=True)
        ciks['YEAR'] = pd.to_datetime(ciks['date']).dt.year

        # limit to 2015 and earlier due to limits on dsi market data
        dsf0 = self.dsf[self.dsf['obs_year']<2016]
        ciks = ciks[ciks['YEAR']<2016]
        cars = pd.DataFrame([])

        for j in range(0,ciks.shape[0]):
            c = ciks.iloc[j][2]
            rit = dsf0[dsf0['CIK'].isin([ciks['cik'][j]])]
            rit = rit.reset_index(drop=True)
            if rit.empty == False:
                locr = rit.loc[rit['date'] == c]
                if  locr.empty == False:
                    locr = locr.index[0]
                    loc = self.dsi.loc[self.dsi['DATE'] == c].index[0] - 5

                    if(locr+5 >= rit.shape[0]):
                        window = []
                    elif(locr-5 <= 0):
                        window = []
                    else:
                        window = list(range(locr-5,locr+5))

                    alpha = coef[coef['cik'] == ciks['cik'][j]]['const']
                    beta = coef[coef['cik'] == ciks['cik'][j]]['vwretd']

                    if not window == False:
                        if alpha.empty == False:
                            ars = pd.DataFrame([])
                            alpha = alpha.reset_index(drop=True)[0]
                            beta = beta.reset_index(drop=True)[0]
                            for i in range(0,len(window)):
                                market = self.dsi.iloc[loc+i].transpose()['vwretd']
                                ret = rit.iloc[window[i]].transpose()['RET']
                                ar = ret - (alpha + beta*market)
                                ar = {'ar':ar}
                                ars = ars.append([ar])
                            if ars.empty == False:
                                final_car = {'car':ars['ar'].sum(),'cik':ciks['cik'][j],'date':c}
                                cars = cars.append([final_car])
        cars = cars.reset_index(drop=True)
        return(cars)

    # calculates the volj for each date
    def cav_clean(self):
        const = 2.55*10**(-6)
        var = self.dsf[['VOL','SHROUT','date','CIK','dsf_year']]
        var = var.reset_index(drop=True)
        var['cav'] = np.log(const + var['VOL']/(var['SHROUT']*1000))
        return(var)

    # calculates the abnormal volume in window around 8-k filing dates
    def abvol(self,var):
        ciks = self.sec.drop_duplicates(subset='cik')
        ciks = ciks.reset_index(drop=True)
        cavs = pd.DataFrame([])

        for j in range(0,ciks.shape[0]):
            c = ciks.iloc[j][2]
            vol = var[var['CIK'].isin([ciks['cik'][j]])]
            vol = vol.reset_index(drop=True)

            if vol.empty == False:
                vol = vol.reset_index(drop=True)
                loc = vol['date'][vol['date'] == c]

                if loc.empty == False:
                    loc = loc.index.tolist()[0]

                    if(loc + 5 >= vol.shape[0]):
                        window = list(range(loc-5,vol.shape[0]))
                    else:
                        window = list(range(loc-5,loc+6))

                    avs = pd.DataFrame([])
                    for d in window:
                        if(d-71 < 0):
                            x = 0
                            y = d-11
                        else:
                            x = d-71
                            y = d-11

                        if(d-11 < 0):
                            avs = pd.DataFrame([])
                        else:
                            win_cav = vol.loc[range(x,y)]['cav']
                            win_avg = win_cav.mean()
                            win_std = win_cav.std()
                            volj = vol['cav'][d]
                            avj = (volj-win_avg)/win_std
                            avj = {'av':avj}
                            avs = avs.append([avj])
                    if avs.empty == False:
                        final_cav = {'cav':avs['av'].sum(),'cik':ciks['cik'][j],'date':c}
                        cavs = cavs.append([final_cav])
        cavs = cavs.reset_index(drop=True)
        return(cavs)



############ MAIN CODE ############
# path of data files
path = "C:/Users/Austin/GIT_profile/8k_study/"

# pulls data from csvs
dsf = pd.read_csv(path+'dsf.csv')
sec = pd.read_csv(path+'sec.csv')
dsi = pd.read_csv(path+'dsi.csv')

# puts dates into date time format for easier comparison
dsf['date'] = pd.to_datetime(dsf['date']).dt.date
sec['date'] = pd.to_datetime(sec['date']).dt.date
dsi['DATE'] = pd.to_datetime(dsi['DATE'], format='%Y%m%d').dt.date

# run class and its functions
ab = abnormal(sec,dsf,dsi)
coef = ab.ret_model()
var = ab.cav_clean()
car = ab.abret(coef)
cav = ab.abvol(var)

# get descriptive stats for cav and car
cav_stats = cav['cav'].describe()
car_stats = car['car'].describe()

# write car and cav dataframes to csv
car.to_csv(path+'CAR.csv')
cav.to_csv(path+'CAV.csv')
cav_stats.to_csv(path+'CAV_stats.csv')
car_stats.to_csv(path+'CAR_stats.csv')

# read in car and cav csv
# car = pd.read_csv(path+'CAR.csv')
# cav = pd.read_csv(path+'CAR.csv')

# histogram plots of cav and car
# CAR
var = car['car']
num_bins = 20
mu, std = norm.fit(var)
n, bins, patches = plt.hist(var, num_bins, normed=True, color='green', alpha=0.5)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, var.shape[0])
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=1.5)
title = 'CAR Data Distribution: mean=%.4f, std=%.4f' %(mu,std)
plt.ylabel('Normalized Obs')
plt.xlabel('CAR')
plt.title(title)
plt.savefig(path+'CAR_plot.pdf')
# reset figure for next plot
plt.clf()

#CAV
var = cav['cav']
num_bins = 20
mu, std = norm.fit(var)
n, bins, patches = plt.hist(var, num_bins, normed=True, color='blue', alpha=0.5)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, var.shape[0])
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=1.5)
title = 'CAV Data Distribution: mean=%.4f, std=%.4f' %(mu,std)
plt.ylabel('Normalized Obs')
plt.xlabel('CAV')
plt.title(title)
plt.savefig(path+'CAV_plot.pdf')
