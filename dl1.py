import requests
import pandas as pd
from bs4 import BeautifulSoup as beaut
import csv

pull = pd.read_csv('sec.csv')
for i in range(1, int(pull.shape[0]/4)):
    form = requests.get(pull['url'][i])
    soup = beaut(form.text, 'lxml').text
    file = open('data/'+pull['cik'][i].astype(str)+' '+pull['date'][i]+'.txt','w', encoding='utf8')
    file.write(soup)
    file.close
