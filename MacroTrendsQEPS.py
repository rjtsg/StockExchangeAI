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
EPS = list()
DATE = list()
Search = re.compile(r'Q\d \d\d\d\d')
for i in range(0,len(list2)):
    mo1 = Search.search(str(list2[i])[35:42])
    #print(mo1)
    try:
        mo1.group() == str(list2[i])[35:42]
        DATE.append(str(list2[i])[35:42])
        EPS.append(str(list2[i])[79:83])
        #print('True')
    except:
        #print('False')
        pass
    
print(DATE)
print(EPS)
    

    
