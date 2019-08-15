import pandas as pd 
import urllib.request, io, csv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

tickers=list(pd.read_excel('tickers.xlsx').iloc[:,0])


def getStockInfo(x): #Needs to be a string
        url = urllib.request.urlopen('http://download.macrotrends.net/assets/php/stock_data_export.php?t={}'.format(x)) 
        datareader = csv.reader(io.TextIOWrapper(url))
        df = pd.DataFrame(list(datareader)[15:], columns=['date','open','high','low','close','volume'])
        return df

def saveStockInfo(TickerList): #Needs to be a list
    for x in TickerList:
        url = urllib.request.urlopen('http://download.macrotrends.net/assets/php/stock_data_export.php?t={}'.format(x)) 
        datareader = csv.reader(io.TextIOWrapper(url))
        df = pd.DataFrame(list(datareader)[15:], columns=['date','open','high','low','close','volume'])
        df.to_excel('StockData_{}.xlsx'.format(x))
        print(x)
        return 'Saved to local folder'



def saveStockToDrive(TickerList): #Needs to be a list
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    for x in TickerList:
        url = urllib.request.urlopen('http://download.macrotrends.net/assets/php/stock_data_export.php?t={}'.format(x)) 
        datareader = csv.reader(io.TextIOWrapper(url))
        df = pd.DataFrame(list(datareader)[15:], columns=['date','open','high','low','close','volume'])
        df.to_excel('StockData_{}.xlsx'.format(x))
        
        file1 = drive.CreateFile()
        file1.SetContentFile('StockData_{}.xlsx'.format(x))
        file1.Upload()
        print('upload {} succesvol'.format(x))
        os.remove('StockData_{}.xlsx'.format(x))
    
    return 'Saved to Google Drive'

#Example how the functiones can be called for APPLE stocks
# print(getStockInfo('AAPL'))
# print(saveStockInfo(['AAPL']))
# print(saveStockToDrive(['AAPL']))
