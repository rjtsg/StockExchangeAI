import requests, bs4, re
import pandas as pd
import xlrd
import os
import time
import lxml

#gauth = GoogleAuth()
#gauth.LocalWebserverAuth()
#drive = GoogleDrive(gauth)

TickerList=list(pd.read_excel('tickers.xlsx').iloc[:,0])
TickerName=list(pd.read_excel('tickers.xlsx').iloc[:,1])

def getRev(TickerList,TickerName,dataframe=None):

    if dataframe is not None:
        df = dataframe
        newFile = False
    else:
        df = pd.DataFrame()
        newFile = True

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
                            df.loc[j,'Date'] = quart
                            df.loc[j,x] = mo2.group()
                        else:
                            if (quart in df.loc[:,'Date'].values):
                                indx = df.index[df['Date']==quart]
                                df.loc[indx,x] = mo2.group()
                            else:
                                lenDF = len(df) 
                                df.loc[lenDF] = 'NaN'
                                df.loc[lenDF,'Date'] = quart
                                df.loc[lenDF,x] = mo2.group() 
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
    df.to_excel('RevenueDATA.xlsx')
    #file1 = drive.CreateFile()
    #file1.SetContentFile('RevenueDATA.xlsx')
    #file1.Upload()
    #print('Upload to the drive is succesful')
    #file1 = drive.CreateFile() #can be commented if it works without for you
    #os.remove('RevenueData.xlsx')
           
#getRev(TickerList,TickerName)
