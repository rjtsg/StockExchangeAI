import requests, bs4, re
import pandas as pd
import xlrd
import os
import time
import lxml

from ImportPERData import getPER
from ImportDERData import getDER
from ImportRevenueData import getRev
from ImportEPSData import getEPS

TickerList=list(pd.read_excel('tickers.xlsx').iloc[:,0])
TickerName=list(pd.read_excel('tickers.xlsx').iloc[:,1])

PERFile = os.path.isfile('PERData.xlsx')
if PERFile == False:
    print('PE-ratios data does not exist, building a new file')
    df = getPER(TickerList,TickerName)
elif PERFile == True:
    PERData = pd.read_excel('PERData.xlsx',index_col=0)
    print('checking and updating PE-ratios')
    df = getPER(TickerList,TickerName,PERData)
    
    


#print('getting debt/equity ratios')
#getDER(TickerList,TickerName)
#print('getting revenues')
#getRev(TickerList,TickerName)
#print('getting earnings-per-share')
#df = getEPS(TickerList,TickerName)
#print('succes')


