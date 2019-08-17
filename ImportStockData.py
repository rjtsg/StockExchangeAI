import pandas as pd 
import urllib.request, io, csv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import yfinance as yf

tickers=list(pd.read_excel('tickers.xlsx').iloc[:,0])



def getStockInfo(x): #Needs to be a string
        tickr = yf.Ticker(x)
        df = tickr.history(period="max")
        df = df.sort_index(axis=0, ascending=False)
        return df

def saveStockInfo(TickerList): #Needs to be a list
    for x in TickerList:
        tickr = yf.Ticker(x)
        df = tickr.history(period="max")
        df = df.sort_index(axis=0, ascending=False)
        df.to_excel('StockData_{}.xlsx'.format(x))
        print(x)
        return 'Saved to local folder'

def saveStockToDrive(TickerList): #Needs to be a list
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    for x in TickerList:
        tickr = yf.Ticker(x)
        df = tickr.history(period="max")
        df = df.sort_index(axis=0, ascending=False)
        df.to_excel('StockData_{}.xlsx'.format(x))
        
        file1 = drive.CreateFile()
        file1.SetContentFile('StockData_{}.xlsx'.format(x))
        file1.Upload()
        print('upload {} succesvol'.format(x))
        os.remove('StockData_{}.xlsx'.format(x))
    
    return 'Saved to Google Drive'

#Example how the functiones can be called for APPLE stocks
#print(getStockInfo('V'))
#print(saveStockInfo(['AAPL']))
#print(saveStockToDrive(['V']))
