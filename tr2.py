import requests, bs4, re
import pandas as pd
import xlrd
import win32com.client as win32
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import time

url = 'https://www.macrotrends.net/stocks/charts/AMZN/amazon/eps-earnings-per-share-diluted'
res = requests.get(url)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text)
list2 = soup.findAll('tr')
Search = re.compile(r'Q\d \d\d\d\d')
Search2 = re.compile(r'\$\-?\d{1,}.\d{2}')
DATE = list()
df1 = pd.DataFrame(columns=['Quarter'],index=range(0,58))
Counter = 0

for i in TickerList:
    df1['ESP_{}'.format(i)] = 'NaN'

for i in range(0,len(list2)): #This for-loop retrieves the good Quarters
    mo1 = Search.search(str(list2[i])[35:42])
    try:
        mo1.group() == str(list2[i])[35:42]
        DATE.append(str(list2[i])[35:42])
        df1.Quarter[Counter] = mo1.group()
        Counter +=1
    except:
        pass
    
for i in range(0,len(TickerList)):
    x = TickerList[i]
    y = TickerName[i]
    url1 = 'https://www.macrotrends.net/stocks/charts/{}/{}/eps-earnings-per-share-diluted'.format(x,y)
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text)
    list2 = soup.findAll('tr')
    Search = re.compile(r'Q\d \d\d\d\d')
    Search2 = re.compile(r'\$\-?\d{1,}.\d{2}')
    for i in range(0,len(list2)):
        mo1 = Search.search(str(list2[i])[35:42])
        b = False
        try:
            mo1.group() == str(list2[i])[35:42]
            b = True
            if b == True:
                mo2 = Search2.search(str(list2[i]))
                dfb = next(iter(df1[df1['Quarter']== mo1.group() ].index), 'no match')
                df1['ESP_AMZN'][dfb] = mo2.group()
        except:
            pass
print(df1)
