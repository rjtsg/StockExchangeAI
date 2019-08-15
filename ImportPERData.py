import requests, bs4, re
import pandas as pd
import xlrd
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import time
import lxml

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

Search = re.compile(r'Q\d \d\d\d\d')
Search2 = re.compile(r'\$\-?\d{1,}.\d{2}')
TickerList=list(pd.read_excel('tickers.xlsx').iloc[:,0])
TickerName=list(pd.read_excel('tickers.xlsx').iloc[:,1])
BeginYear = 2018
EndYear = 2006
Dates = ['2019-08-14','2019-06-30','2019-03-31']
Months = ['12','09','06','03']
Days = [31,30,30,31]
TickerList=list(pd.read_excel('tickers.xlsx').iloc[:,0])
TickerName=list(pd.read_excel('tickers.xlsx').iloc[:,1])

I = 0
J = 0
jaar = BeginYear

while jaar >= EndYear:
    Dates.append('{}-{}-{}'.format(jaar,Months[J],Days[J]))
    J += 1
    if J == 4:
        jaar -= 1
        J = 0

df = pd.DataFrame({'Date':Dates})

for i in TickerList: #makes columns for the ESP input
    df['PER_{}'.format(i)] = 'NaN'

for i in range(0,len(TickerList)): #Fills in the EPS column for each company
    x = TickerList[i]
    y = TickerName[i]
    url = 'https://www.macrotrends.net/stocks/charts/{}/{}/pe-ratio'.format(x,y)
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text,'lxml')
    list2 = soup.findAll('tr')
    Search1 = re.compile(r'\d\d\d\d-\d\d-\d\d')
    Search2 = re.compile(r'\d{1,}\.\d{2}')
    for i in range(0,len(list2)):
        mo1 = Search1.search(str(list2[i]))
        if mo1 != None:
            mo2 = Search2.findall(str(list2[i]))
            dfb = next(iter(df[df['Date']== mo1.group() ].index), 'no match')
            df['PER_{}'.format(x)][dfb] = mo2[-1]


df.to_excel('PERData.xlsx')
file1 = drive.CreateFile()
file1.SetContentFile('PERData.xlsx')
file1.Upload()
os.remove('PERData.xlsx')
print('Upload to the drive is succesful')
