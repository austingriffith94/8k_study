# Austin Griffith
# 11/30/2017
# Event Studies and Sentiment Analysis
# Python 3.6.3

import re
import requests
import pandas as pd
import numpy as np
import random
import fileinput
import zipfile
import datetime
from shutil import move
import fileinput
import os
import io

# create directory for data files
if os.path.exists('data') == False:
    os.makedirs('data')

# class for reading files from sec website
class sec:
    def __init__(self,t0,t1,n):
        self.t0 = t0
        self.t1 = t1
        self.n = n


    def pull_index(self):
        Q = ['QTR1','QTR2','QTR3','QTR4']
        T = list(map(str,list(range(self.t0,self.t1+1))))
        idx_url = 'data/master.idx'

        for t in T:
            for q in Q:
                url = 'https://www.sec.gov/Archives/edgar/full-index/'+t+'/'+q+'/master.zip'
                index = 'data/master'+t+q+'.idx'
                req = requests.get(url, stream=True)
                z = zipfile.ZipFile(io.BytesIO(req.content))
                z.extractall('data')
                move(idx_url, index)
                print(url, 'downloaded')

    def del_index(self):
        Q = ['QTR1','QTR2','QTR3','QTR4']
        T = list(map(str,list(range(self.t0,self.t1+1))))

        for t in T:
            for q in Q:
                index = 'data/master'+t+q+'.idx'
                os.remove(index)
                print(index, 'removed')


    def clean_index(self):
        Q = ['QTR1','QTR2','QTR3','QTR4']
        T = list(map(str,list(range(self.t0,self.t1+1))))

        for t in T:
            for q in Q:
                index = 'data/master'+t+q+'.idx'
                links_to_keep = []
                # read all lines in .idx for 8-K
                with open(index, "r") as f:
                    for line in f.readlines():
                        if '8-K' in line:
                            links_to_keep.append(line)

                # write all the links in list to the file
                with open(index, "w") as f:
                    for link in links_to_keep:
                        f.write(link)


    def read_index(self):
        Q = ['QTR1','QTR2','QTR3','QTR4']
        T = list(map(str,list(range(self.t0,self.t1+1))))
        raw = "https://www.sec.gov/Archives/"

        for t in T:
            for q in Q:
                index = 'data/master'+t+q+'.idx'

                with open(index) as f:
                    line = random.sample(f.readlines(),self.n)

                for i in range(0,self.n):
                    s = line[i].split('|')
                    file = open('data/sec.csv','ab')
                    cik = s[0]
                    date = s[3]
                    dr = s[4].split('/')
                    name = dr[3].rstrip('\n')









# years to look at
t0 = 1995
t1 = 1995
n = 100
gov = sec(t0,t1,n)
gov.pull_index()
gov.clean_index()

