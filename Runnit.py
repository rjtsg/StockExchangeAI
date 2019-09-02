import requests, bs4, re
import pandas as pd
import xlrd
import os
import time
import lxml
import sys

sys.path.append('ImportFunctions')

from ImportPERData import getPER
from ImportDERData import getDER
from ImportEPSData import getEPS
from ImportDividendData import getDividend
from ImportRevenueData import getRevenue
from ImportStockData import getStock

TickerList=list(pd.read_excel('tickers.xlsx').iloc[:,0])
TickerName=list(pd.read_excel('tickers.xlsx').iloc[:,1])
DataList = ['PER','DER','EPS','Revenue','Dividend','Stock'] #make sure that these 2 are in the same order
FunctionList = [getPER,getDER,getEPS,getRevenue,getDividend,getStock]

if not os.path.exists('DataFiles'): #checks if directory DataFiles exists, if not makes a directory with that name
    os.makedirs('DataFiles')
    print('Created new DataFiles directory')


firsttime = True 
for i in range(0,len(DataList)):
    x = DataList[i]
    y = FunctionList[i]
    if firsttime: #such that when it is in the directory it does not keep wanting to go deeper
        firsttime = False
        os.chdir('DataFiles') #goes into the DataFiles directory
    path = '{}Data.xlsx'.format(x) #this is the data file

    if x == 'Stock': #Inside the Stock function the ticker needs to be placed and then the extension
        path = '{}Data'.format(x) #This does mean that stock data will always be fully updated every time

    if not os.path.exists(path):
        print('{} data does not exists, building a new file'.format(x))
        df = y(TickerList,TickerName,path)
    else:
        print('checking and updating {} data'.format(x))
        DataFrame = pd.read_excel('{}Data.xlsx'.format(x),index_col=0)
        df = y(TickerList,TickerName,path,DataFrame)

DataDirectory = os.getcwd() #remembers the path, maybe handy for alter        
os.chdir(maindirectory) #switches back to the path from which we started the run




