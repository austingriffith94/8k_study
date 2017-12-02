pull = pd.read_csv('sec.csv')
for i in range(pull.shape[0]/4, 2*pull.shape[0]/4):
    form = requests.get(pull['url'][i])
    soup = beaut(form.text, 'lxml').text
    file = open('data/'+pull['cik'][i].astype(str)+' '+pull['date'][i]+'.txt','w', encoding='utf8')
    file.write(soup)
    file.close
