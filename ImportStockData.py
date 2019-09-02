import pandas as pd 
import urllib.request, io, csv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import yfinance as yf
from datetime import datetime

def saveStockToDrive(TickerList,TickerName,path,dataframe =None): #TickerListNeeds to be a list
    newFile=True
    if dataframe is not None:
        df = dataframe
        newFile = False
        lastDate = df.index[0]
    for x in TickerList:
        tickr = yf.Ticker(x)
        if newFile:
                df = tickr.history(period="max")
                df = df.sort_index(axis=0, ascending=False)
        else:
                today = datetime.today().strftime('%Y-%m-%d')
                df1 = tickr.history(start=lastDate, end=today)
                df1 = df1.sort_index(axis=0, ascending=False)
                df1 = df1.append(df)
                df = df1
        df.to_excel(path+'_{}.xlsx'.format(x))
        return df
