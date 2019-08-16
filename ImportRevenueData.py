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

#Search = re.compile(r'Q\d \d\d\d\d')
#Search2 = re.compile(r'\$\-?\d{1,}.\d{1,}')
df1 = pd.read_excel('Quarters.xlsx')
TickerList=list(pd.read_excel('tickers.xlsx').iloc[:,0])
TickerName=list(pd.read_excel('tickers.xlsx').iloc[:,1])

for i in TickerList: #makes columns for the ESP input
    df1['Rev_{}'.format(i)] = 'NaN'

for i in range(0,len(TickerList)): #Fills in the EPS column for each company
    x = TickerList[i]
    y = TickerName[i]
    url1 = 'https://www.macrotrends.net/stocks/charts/{}/{}/revenue'.format(x,y)
    res = requests.get(url1)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text,'lxml')
    list2 = soup.findAll('tr')
    Search = re.compile(r'Q\d \d\d\d\d') #Search regex for Quarters
    Search2 = re.compile(r'\$\-?\d{1,},\d{0,}') #Search regex for EPS
    for i in range(0,len(list2)):
        mo1 = Search.search(str(list2[i])[35:42])
        if mo1 != None:
            mo2 = Search2.search(str(list2[i]))
            if mo2 != None:
                dfb = next(iter(df1[df1['Quarter']== mo1.group() ].index), 'no match') #Searches for the matching Quarter, this is untested
                df1['Rev_{}'.format(x)][dfb] = mo2.group() #Places it at the right place
        
df1.to_excel('RevenueDATA.xlsx')
file1 = drive.CreateFile()
file1.SetContentFile('RevenueDATA.xlsx')
file1.Upload()
print('Upload to the drive is succesful')
file1 = drive.CreateFile() #can be commented if it works without for you
os.remove('RevenueData.xlsx')
