import pandas as pd 
import urllib.request, io, csv
import os
import yfinance as yf
from datetime import datetime

def getStock(TickerList,TickerName,path,dataframe =None): #TickerListNeeds to be a list
    newFile=True
    if dataframe is not None:
        df = dataframe
        newFile = False
        lastDate = df.index[0]
    for x in TickerList:
        tickr = yf.Ticker(x)
        if newFile:
                print('Stock data does not exist, building a new file')
                df = tickr.history(period="max")
                df = df.sort_index(axis=0, ascending=False)
        else:
                print('checking and updating stock data')
                today = datetime.today().strftime('%Y-%m-%d')
                df1 = tickr.history(start=lastDate, end=today)
                df1 = df1.sort_index(axis=0, ascending=False)
                df1 = df1.append(df)
                df = df1
        df.to_excel(path+'_{}.xlsx'.format(x))
        return df
