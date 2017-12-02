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


t0 = 1995
t1 = 1995

def pull_index(t0,t1):
    Q = ['QTR1','QTR2','QTR3','QTR4']
    T = list(map(str,list(range(t0,t1+1))))
    idx_url = 'data/master.idx'

    for t in T:
        for q in Q:
            url = 'https://www.sec.gov/Archives/edgar/full-index/'+t+'/'+q+'/master.zip'
            m_url = 'data/master'+t+q+'.idx'
            req = requests.get(url, stream=True)
            z = zipfile.ZipFile(io.BytesIO(req.content))
            z.extractall('data')
            move(idx_url, m_url)
            print(url, 'downloaded')

def read_index(t0,t1)
    Q = ['QTR1','QTR2','QTR3','QTR4']
    T = list(map(str,list(range(t0,t1+1))))

pull_index(t0,t1)
