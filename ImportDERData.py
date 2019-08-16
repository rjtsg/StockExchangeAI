import requests, bs4, re
import pandas as pd
import xlrd
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import time
import lxml

#gauth = GoogleAuth()
#gauth.LocalWebserverAuth()
#drive = GoogleDrive(gauth)

BeginYear = 2019
TickerList=list(pd.read_excel('tickers.xlsx').iloc[:,0])
TickerName=list(pd.read_excel('tickers.xlsx').iloc[:,1])

def getDER(TickerList,TickerName,BeginYear,drive):

    Dates = list()
    EndYear = 2005
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
        url = 'https://www.macrotrends.net/stocks/charts/{}/{}/debt-equity-ratio'.format(x,y)
        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text,'lxml')
        list2 = soup.findAll('tr')
        Search1 = re.compile(r'(\d\d\d\d)-(\d\d)-(\d\d)')
        Search2 = re.compile(r'\d{1,}\.\d{2}')
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
                dfb = next(iter(df[df['Date']== quart].index), 'no match')
                df['DER_{}'.format(x)][dfb] = mo2[-1]
                

    df.to_excel('DERData.xlsx')
    file1 = drive.CreateFile()
    file1.SetContentFile('DERData.xlsx')
    file1.Upload()
    print('Upload to the drive is succesful')
    file1 = drive.CreateFile()#can be commented if it works without for you
    os.remove('DERData.xlsx')

#getDER(TickerList,TickerName,BeginYear)
