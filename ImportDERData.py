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
BeginYear = 2019
EndYear = 2006
Dates = list()
Months = ['12','09','06','03']
Days = [31,30,30,31]
TickerList=list(pd.read_excel('tickers.xlsx').iloc[:,0])
TickerName=list(pd.read_excel('tickers.xlsx').iloc[:,1])

I = 0
J = 4
jaar = BeginYear

while jaar >= EndYear:
    Dates.append('Q{} {}'.format(J,jaar))
    J -= 1
    if J == 0:
        jaar -= 1
        J = 4

df = pd.DataFrame({'Date':Dates})

for i in TickerList: #makes columns for the ESP input
    df['DER_{}'.format(i)] = 'NaN'

for i in range(0,len(TickerList)): #Fills in the EPS column for each company
    x = TickerList[i]
    y = TickerName[i]
    quart = 0
    url = 'https://www.macrotrends.net/stocks/charts/{}/{}/debt-equity-ratio'.format(x,y)
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text,'lxml')
    list2 = soup.findAll('tr')
    Search1 = re.compile(r'\d\d\d\d-\d\d-\d\d')
    Search2 = re.compile(r'\d{1,}\.\d{2}')
    for j in range(0,len(list2)):
        mo1 = Search1.search(str(list2[j]))
        if mo1 != None:
            mo2 = Search2.findall(str(list2[j]))
            #dfb = next(iter(df[df['Date']== Dates[quart]].index), 'no match')
            df['DER_{}'.format(x)][quart] = mo2[-1]
            quart += 1


df.to_excel('DERData.xlsx')
file1 = drive.CreateFile()
file1.SetContentFile('DERData.xlsx')
file1.Upload()
print('Upload to the drive is succesful')
file1 = drive.CreateFile()#can be commented if it works without for you
os.remove('DERData.xlsx')
