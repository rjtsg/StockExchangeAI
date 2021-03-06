import requests, bs4, re
import pandas as pd
import numpy as np
import yfinance as yf
import xlrd
import os
import time
import lxml
from datetime import datetime

def getPER(TickerList,TickerName,path,dataframe=None):
    if dataframe is not None:
        df = dataframe
        newFile = False
    else:
        df = pd.DataFrame()
        newFile = True
    PosCount = 0
    for i in range(0,len(TickerList)): #Fills in the EPS column for each company
        x = TickerList[i]
        y = TickerName[i]
        url = 'https://www.macrotrends.net/stocks/charts/{}/{}/pe-ratio'.format(x,y)
        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text,'lxml')
        list2 = soup.findAll('tr')
        Search1 = re.compile(r'(\d\d\d\d)-(\d\d)-(\d\d)')
        Search2 = re.compile(r'\d{1,}\.\d{2}')
        if not newFile:
            indxfir = df[x].first_valid_index()
        for j in range(0,len(list2)):
            mo1 = Search1.search(str(list2[j]))
            if mo1 != None:
                mo2 = Search2.findall(str(list2[j]))
                if mo1.group(2) == '12' or mo1.group(2) == '11':
                    quart = 'Q4 {}'.format(mo1.group(1))
                elif mo1.group(2) == '01':
                    quart = 'Q4 {}'.format(str(int(mo1.group(1))-1))
                elif mo1.group(2) == '09' or mo1.group(2) == '10'or mo1.group(2) == '08':
                    quart = 'Q3 {}'.format(mo1.group(1))
                elif mo1.group(2) == '06' or mo1.group(2) == '07'or mo1.group(2) == '05':
                    quart = 'Q2 {}'.format(mo1.group(1))
                elif mo1.group(2) == '03' or mo1.group(2) == '04'or mo1.group(2) == '02':
                    quart = 'Q1 {}'.format(mo1.group(1))
                else:
                    print(mo1.group(2))
                    print('Something has gone wrong')
                if newFile:
                    if i == 0:
                        df.loc[PosCount,'Date'] = quart
                        df.loc[PosCount,x] = mo2[-1]
                        PosCount += 1
                    else:
                        if (quart in df.loc[:,'Date'].values):
                            indx = df.index[df['Date']==quart]
                            df.loc[indx,x] = mo2[-1]
                        else:
                            df.loc[PosCount,'Date'] = quart
                            df.loc[PosCount,x] = mo2[-1]
                            PosCount += 1
                            
                            
                else:
                    if x in df.columns:
                        if int(df.loc[indxfir,'Date'][-4:]) <= int(quart[-4:]): #checks the year, if smaller or equal to year update.
                            if (quart in df.loc[:,'Date'].values):
                                indx = df.index[df['Date']==quart][0] #added zero to get the integer, otherwise it will make a new column
                                if df.loc[indx,x] != mo2[-1]:
                                    df.loc[indx,x] = mo2[-1]                
                            else:
                                lenDF = len(df) 
                                df.loc[lenDF] = 'NaN'
                                df.loc[lenDF,'Date'] = quart
                                df.loc[lenDF,x] = mo2[-1] 
                    else:
                        print('new Ticker')
                        if (quart in df.loc[:,'Date'].values):
                            indx = df.index[df['Date']==quart][0] #added zero to get the integer, otherwise it will make a new column
                            df.loc[indx,x] = mo2[-1]
                        else:
                            lenDF = len(df) 
                            df.loc[lenDF] = 'NaN'
                            df.loc[lenDF,'Date'] = quart
                            df.loc[lenDF,x] = mo2[-1]
    df = df.set_index('Date')
    df = df.reindex(sorted(df.index, key=lambda x: x.split(' ')[::-1],reverse=True)).reset_index()
    df.to_excel(path)
    return df

def getRevenue(TickerList,TickerName,path,dataframe=None):

    if dataframe is not None:
        df = dataframe
        newFile = False
    else:
        df = pd.DataFrame()
        newFile = True
    PosCount = 0
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
        if not newFile:
            indxfir = df[x].first_valid_index()
        for j in range(0,len(list2)):
            mo1 = Search.search(str(list2[j])[35:42])
            if mo1 != None:
                quart = mo1.group()
                mo2 = Search2.search(str(list2[j]))
                if mo2 != None:
                    if newFile:
                        if i == 0:
                            df.loc[PosCount,'Date'] = quart
                            df.loc[PosCount,x] = mo2.group()
                            PosCount += 1
                        else:
                            if (quart in df.loc[:,'Date'].values):
                                indx = df.index[df['Date']==quart][0]
                                df.loc[indx,x] = mo2.group()
                            else:
                                df.loc[PosCount,'Date'] = quart
                                df.loc[PosCount,x] = mo2.group()
                                PosCount += 1
                                
                    else:
                        if x in df.columns:
                            if int(df.loc[indxfir,'Date'][-4:]) <= int(quart[-4:]):
                                if (quart in df.loc[:,'Date'].values):
                                    indx = df.index[df['Date']==quart]
                                    if df.loc[indx,x].values != mo2.group():
                                        df.loc[indx,x] = mo2.group()               
                                else:
                                    lenDF = len(df)
                                    df.loc[lenDF] = 'NaN'
                                    df.loc[lenDF,'Date'] = quart
                                    df.loc[lenDF,x] = mo2.group()
                        else:
                            if (quart in df.loc[:,'Date'].values):
                                indx = df.index[df['Date']==quart]
                                df.loc[indx,x] = mo2.group()
                            else:
                                lenDF = len(df) 
                                df.loc[lenDF] = 'NaN'
                                df.loc[lenDF,'Date'] = quart
                                df.loc[lenDF,x] = mo2.group()
    df = df.set_index('Date')
    df = df.reindex(sorted(df.index, key=lambda x: x.split(' ')[::-1],reverse=True)).reset_index()
    df.to_excel(path)
    return df

def getEPS(TickerList,TickerName,path,dataframe=None):

    if dataframe is not None:
        df = dataframe
        newFile = False
    else:
        df = pd.DataFrame()
        newFile = True
    PosCount = 0
    for i in range(0,len(TickerList)): #Fills in the EPS column for each company
        x = TickerList[i]
        y = TickerName[i]
        url1 = 'https://www.macrotrends.net/stocks/charts/{}/{}/eps-earnings-per-share-diluted'.format(x,y)
        res = requests.get(url1)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text,'lxml')
        list2 = soup.findAll('tr')
        Search = re.compile(r'Q\d \d\d\d\d') #Search regex for Quarters
        Search2 = re.compile(r'\$\-?\d{1,}.\d{2}') #Search regex for EPS
        if not newFile:
            indxfir = df[x].first_valid_index()
        for j in range(0,len(list2)):
            mo1 = Search.search(str(list2[j])[35:42])
            if mo1 != None:
                mo2 = Search2.search(str(list2[j]))
                quart = mo1.group()
                if newFile:
                    if i == 0:
                        df.loc[PosCount,'Date'] = quart
                        df.loc[PosCount,x] = mo2.group()
                        #print(quart)
                        #print(mo2.group())
                        PosCount+=1
                    else:
                        if (quart in df.loc[:,'Date'].values):
                            indx = df.index[df['Date']==quart]
                            df.loc[indx,x] = mo2.group()
                        else:
                            df.loc[PosCount,'Date'] = quart
                            df.loc[PosCount,x] = mo2.group()
                            PosCount += 1
                else:
                    if x in df.columns:
                        if int(df.loc[indxfir,'Date'][-4:]) <= int(quart[-4:]):
                            if (quart in df.loc[:,'Date'].values):
                                indx = df.index[df['Date']==quart]
                                if df.loc[indx,x].values != mo2.group():
                                    df.loc[indx,x] = mo2.group()               
                            else:
                                lenDF = len(df) 
                                df.loc[lenDF] = 'NaN'
                                df.loc[lenDF,'Date'] = quart
                                df.loc[lenDF,x] = mo2.group()
                    else:
                        if (quart in df.loc[:,'Date'].values):
                            indx = df.index[df['Date']==quart]
                            df.loc[indx,x] = mo2.group()
                        else:
                            lenDF = len(df) 
                            df.loc[lenDF] = 'NaN'
                            df.loc[lenDF,'Date'] = quart
                            df.loc[lenDF,x] = mo2.group()
    df = df.set_index('Date')
    df = df.reindex(sorted(df.index, key=lambda x: x.split(' ')[::-1],reverse=True)).reset_index()
    df.to_excel(path)
    return df

def getDER(TickerList,TickerName,path,dataframe=None):
    if dataframe is not None:
        df = dataframe
        newFile = False
    else:
        df = pd.DataFrame()
        newFile = True
    PosCount = 0
    for i in range(0,len(TickerList)): #Fills in the EPS column for each company
        x = TickerList[i]
        y = TickerName[i]
        url = 'https://www.macrotrends.net/stocks/charts/{}/{}/debt-equity-ratio'.format(x,y)
        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text,'lxml')
        list2 = soup.findAll('tr')
        Search1 = re.compile(r'(\d\d\d\d)-(\d\d)-(\d\d)')
        Search2 = re.compile(r'-?\d{1,}\.\d{2}')
        if not newFile:
            indxfir = df[x].first_valid_index()
        for j in range(0,len(list2)):
            mo1 = Search1.search(str(list2[j]))
            if mo1 != None:
                mo2 = Search2.findall(str(list2[j]))
                if mo1.group(2) == '12' or mo1.group(2) == '11':
                    quart = 'Q4 {}'.format(mo1.group(1))
                elif mo1.group(2) == '01':
                    quart = 'Q4 {}'.format(str(int(mo1.group(1))-1))
                elif mo1.group(2) == '09' or mo1.group(2) == '10'or mo1.group(2) == '08':
                    quart = 'Q3 {}'.format(mo1.group(1))
                elif mo1.group(2) == '06' or mo1.group(2) == '07'or mo1.group(2) == '05':
                    quart = 'Q2 {}'.format(mo1.group(1))
                elif mo1.group(2) == '03' or mo1.group(2) == '04'or mo1.group(2) == '02':
                    quart = 'Q1 {}'.format(mo1.group(1))
                else:
                    print(mo1.group(2))
                    print('Something has gone wrong')
                if newFile:
                    if i == 0:
                        df.loc[PosCount,'Date'] = quart
                        df.loc[PosCount,x] = mo2[-1]
                        PosCount += 1
                    else:
                        if (quart in df.loc[:,'Date'].values):
                            indx = df.index[df['Date']==quart][0]
                            df.loc[indx,x] = mo2[-1]
                        else:
                            df.loc[PosCount,'Date'] = quart
                            df.loc[PosCount,x] = mo2[-1]
                            PosCount += 1
                else:
                    if x in df.columns:
                        if int(df.loc[indxfir,'Date'][-4:]) <= int(quart[-4:]):
                            if (quart in df.loc[:,'Date'].values):
                                indx = df.index[df['Date']==quart][0]
                                if df.loc[indx,x] != mo2[-1]:
                                    #print(indx[0])
                                    df.loc[indx,x] = mo2[-1]                
                            else:
                                lenDF = len(df) 
                                df.loc[lenDF] = 'NaN'
                                df.loc[lenDF,'Date'] = quart
                                df.loc[lenDF,x] = mo2[-1] 
                    else:
                        if (quart in df.loc[:,'Date']):
                            indx = df.index[df['Date']==quart][0]
                            df.loc[indx,x] = mo2[-1]
                        else:
                            lenDF = len(df) 
                            df.loc[lenDF] = 'NaN'
                            df.loc[lenDF,'Date'] = quart
                            df.loc[lenDF,x] = mo2[-1]
                    
    df = df.set_index('Date')
    df = df.reindex(sorted(df.index, key=lambda x: x.split(' ')[::-1],reverse=True)).reset_index()
    df.to_excel(path)
    return df

def getDividend(TickerList,TickerName,path,dataframe=None): #it does not need a tickername, but otherwise the loops fails
    if dataframe is not None:
            df = dataframe
            newFile = False
    else:
            df = pd.DataFrame()
            newFile = True
    for i in range(0,len(TickerList)):
            x = TickerList[i]
            url = 'https://query1.finance.yahoo.com/v8/finance/chart/{}?symbol={}&period1=0&period2=9999999999&interval=1mo&events=div'.format(x,x)
            res = requests.get(url)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text,'lxml')
            soupList = re.findall(r'{"amount.*?}', str(soup))
            searchDiv = re.compile(r':.*?,')
            searchDat = re.compile(r'e":.*?}')
            if not newFile:
                    indxfir = df[x].first_valid_index()
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

                    if newFile:
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
                    else:
                            if x in df.columns:
                                    if int(df.loc[indxfir,'date'][-4:]) <= int(datum[-4:]):
                                            if (datum in df.loc[:,'date'].values):
                                                    indx = df.index[df['date']==datum]

                                                    if df.loc[indx,x].values != float(divi):
                                                            df.loc[indx,x] = float(divi)                
                                            else:
                                                    lenDF = len(df) 
                                                    df.loc[lenDF] = 'NaN'
                                                    df.loc[lenDF,'date'] = datum
                                                    df.loc[lenDF,x] = float(divi) 
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
    df.to_excel(path)
    return df

def getStock(TickerList,TickerName,path,dataframe=None): #Needs to be a list
    for x in TickerList:
        tickr = yf.Ticker(x)
        df = tickr.history(period="max")
        df = df.sort_index(axis=0, ascending=False)
        df.to_excel(path+'_{}.xlsx'.format(x))
    return df



