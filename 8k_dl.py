# Austin Griffith
# 11/30/2017
# Event Studies and Sentiment Analysis
# Python 3.6.3

import requests
import time
import pandas as pd
import numpy as np
import random
import zipfile
from shutil import move
import os
import io
from bs4 import BeautifulSoup as beaut
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

# create directory for data files
if os.path.exists('data') == False:
    os.makedirs('data')

# class for reading files from sec website
class sec:
    def __init__(self,t0,t1,n,x):
        self.x = x
        self.n = n
        self.Q = ['QTR1','QTR2','QTR3','QTR4']
        self.T = list(map(str,list(range(t0,t1+1))))

    def pull_index(self):
        idx_url = 'data/master.idx'
        for t in self.T:
            for q in self.Q:
                url = 'https://www.sec.gov/Archives/edgar/full-index/'+t+'/'+q+'/master.zip'
                index = 'data/master'+t+q+'.idx'
                req = requests.get(url, stream=True)
                z = zipfile.ZipFile(io.BytesIO(req.content))
                z.extractall('data')
                move(idx_url, index)
                print(url, 'downloaded')

    def del_index(self):
        for t in self.T:
            for q in self.Q:
                index = 'data/master'+t+q+'.idx'
                os.remove(index)
                print(index, 'removed')

    def clean_index(self):
        for t in self.T:
            for q in self.Q:
                index = 'data/master'+t+q+'.idx'
                keep = []
                # read all lines in .idx for 8-K
                with open(index, "r") as f:
                    for line in f.readlines():
                        if '8-K' in line:
                            keep.append(line)

                # write all the links in list to the file
                with open(index, "w") as f:
                    for link in keep:
                        f.write(link)
                print(index, 'cleaned')

    def read_index(self):
        random.seed(903353429)
        rows_list = []
        for t in self.T:
            for q in self.Q:
                index = 'data/master'+t+q+'.idx'
                raw = "https://www.sec.gov/Archives/"

                with open(index) as f:
                    line = random.sample(f.readlines(),self.n)

                for i in range(0,self.n):
                    s = line[i].split('|')
                    cik = s[0]
                    date = s[3]
                    name = s[1]
                    url = raw+s[4].rstrip('\n')
                    row = {'cik':cik,'date':date,
                        'name':name,'url':url}
                    rows_list.append(row)

        res = pd.DataFrame(rows_list)
        res.to_csv('sec.csv')

    def dl_forms(self,y=0):
        pull = pd.read_csv('sec.csv')
        size = pull.shape[0]
        for i in range(int(y*size/self.x), int((y+1)*size/self.x)):
            form = requests.get(pull['url'][i])
            soup = beaut(form.text, 'lxml').text
            file = open('data/'+pull['cik'][i].astype(str)+' '+pull['date'][i]+'.txt','w', encoding='utf8')
            file.write(soup)
            file.close
            print(pull['url'][i], 'downloaded')

    def del_dl_forms(self):
        pull = pd.read_csv('sec.csv')
        for i in range(1, pull.shape[0]):
            file = 'data/'+pull['cik'][i].astype(str)+' '+pull['date'][i]+'.txt'
            if os.path.exists(file) == True:
                os.remove(file)
            print(file, 'removed')


# years to look at
t0 = 1995
t1 = 2016
n = 100
x = 4
y = list(range(0,x))

# reads index data, creates csv directory
gov = sec(t0,t1,n,x)
gov.pull_index()
gov.clean_index()
gov.read_index()
gov.del_index()

# pauses code
time.sleep(5)

# pulls 8-k data
pool = ThreadPool(x)
pool.map(gov.dl_forms,y)
# gov.del_dl_forms()
