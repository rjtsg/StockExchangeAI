import requests, bs4, re
import pandas as pd
import xlrd
import os
import time
import lxml

def getDER(TickerList,TickerName,path,dataframe=None):
    if dataframe is not None: #loads in the existing file
        df = dataframe
        newFile = False
    else: #builds new Dataframe
        df = pd.DataFrame()
        newFile = True
    PosCount = 0 #Keeps track of real index position in the dataframe, because length is taken over all year finds in bs4.
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
