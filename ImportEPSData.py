import requests, bs4, re
import pandas as pd
import xlrd
import os
#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive
import time
import lxml

#gauth = GoogleAuth()
#gauth.LocalWebserverAuth()
#drive = GoogleDrive(gauth)

TickerList=list(pd.read_excel('tickers.xlsx').iloc[:,0])
TickerName=list(pd.read_excel('tickers.xlsx').iloc[:,1])

def getEPS(TickerList,TickerName,dataframe=None):

    if dataframe is not None:
        df = dataframe
        newFile = False
    else:
        df = pd.DataFrame()
        newFile = True
    k = 0
    
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
                        df.loc[k,'Date'] = quart
                        df.loc[k,x] = mo2.group()
                        #print(quart)
                        #print(mo2.group())
                        k+=1
                    else:
                        if (quart in df.loc[:,'Date'].values):
                            indx = df.index[df['Date']==quart]
                            df.loc[indx,x] = mo2.group()
                        else:
                            lenDF = len(df) 
                            df.loc[lenDF] = 'NaN'
                            df.loc[lenDF,'Date'] = quart
                            df.loc[lenDF,x] = mo2.group()
                            #print(mo2.group())
                            #print(quart)
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
    df.to_excel('EPSDATA.xlsx')
    #file1 = drive.CreateFile()
    #file1.SetContentFile('EPSDATA.xlsx')
    #file1.Upload()
    #print('Upload to the drive is succesful')
    #file1 = drive.CreateFile() #can be commented if it works without for you
    #os.remove('EPSData.xlsx')
    return df
#df = getEPS(TickerList,TickerName)
