import requests, bs4, re
import pandas as pd
import xlrd
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
import numpy as np

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

TickerList=list(pd.read_excel('tickers.xlsx').iloc[:,0])

def getDividend(TickerList):
        df = pd.DataFrame()
        print(df)
        for i in range(0,len(TickerList)):
                x = TickerList[i]
                url = 'https://query1.finance.yahoo.com/v8/finance/chart/{}?symbol={}&period1=0&period2=9999999999&interval=1mo&events=div'.format(x,x)
                res = requests.get(url)
                res.raise_for_status()
                soup = bs4.BeautifulSoup(res.text)
                soupList = re.findall(r'{"amount.*?}', str(soup))
                searchDiv = re.compile(r':.*?,')
                searchDat = re.compile(r'e":.*?}')
                for j in range(0,len(soupList)):
                        divi = searchDiv.search(str(soupList[j])).group()[1:-1]
                        datum = searchDat.search(str(soupList[j])).group()[3:-1]
                        datum = datetime.fromtimestamp(int(datum))
                        if (int(datum.strftime("%m")) in range(2,5)): 
                                datum = 'Q1 ' + str(int(datum.strftime("%Y")))
                        elif (int(datum.strftime("%m")) in range(5,8)): 
                                if x == 'PFE' and int(datum.strftime("%m")) == 7:
                                        datum = 'Q3 ' + str(int(datum.strftime("%Y")))
                                else:
                                        datum = 'Q2 ' + str(int(datum.strftime("%Y")))
                        elif (int(datum.strftime("%m")) in range(8,11)): 
                                datum = 'Q3 ' + str(int(datum.strftime("%Y")))
                        else:
                                if int(datum.strftime("%m")) == 1:
                                        if x == 'PFE':
                                                datum = 'Q1 ' + str(int(datum.strftime("%Y")))
                                        else:
                                                datum = 'Q4 ' + str(int(datum.strftime("%Y"))-1)
                                else:
                                        datum = 'Q4 ' + str(int(datum.strftime("%Y")))


                        if i==0:
                                df.loc[j,'date'] = datum
                                df.loc[j,x] = float(divi)
                        else:
                                if (datum in df.loc[:,'date'].values):
                                        indx = df.index[df['date']==datum]
                                        df.loc[indx,x] = float(divi)
                                        
                                else:
                                       lenDF = len(df) 
                                       df.loc[lenDF] = 'NaN'
                                       df.loc[lenDF,'date'] = datum
                                       df.loc[lenDF,x] = float(divi)                           
        duplicates = df[df.duplicated(['date'])]
        for z in range(0,len(duplicates)): 
                indx1 = df.index[df['date']==duplicates.iloc[z,0]]   
                df.loc[indx1[0],'AXP'] = df.loc[indx1[0],'AXP'] + df.loc[indx1[1],'AXP']
                df = df.drop(indx1[1])
                                  
        df = df.set_index('date')
        df = df.reindex(sorted(df.index, key=lambda x: x.split(' ')[::-1],reverse=True)).reset_index()
        print(df.head())
        df.to_excel('dividends.xlsx')   
        file = drive.CreateFile()
        file.SetContentFile('dividends.xlsx')
        file.Upload()
        os.remove('dividends.xlsx')     
        return 'Upload to Google Drive COMPLETE'

print(getDividend(TickerList))