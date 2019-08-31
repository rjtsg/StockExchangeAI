import requests, bs4, re
import pandas as pd
import xlrd
import os
import time
import lxml

#from ImportPERData import getPER
#from ImportDERData import getDER
#from ImportRevenueData import getRev
#from ImportEPSData import getEPS

import ImportFile

TickerList=list(pd.read_excel('tickers.xlsx').iloc[:,0])
TickerName=list(pd.read_excel('tickers.xlsx').iloc[:,1])
#DataList = ['PERData.xlsx','DERData.xlsx','EPSData.xlsx','RevenueData.xlsx']
DataList = ['PER','DER','EPS','Revenue','Dividend','Stock']

if not os.path.exists('DataFiles'): #checks if directory DataFiles exists, if not makes a directory with that name
    os.makedirs('DataFiles')
    print('Created new DataFiles directory')

maindirectory = os.getcwd() #remembers the path from which the file is run
firsttime = True 
for x in DataList:
    if firsttime: #such that when it is in the directory it does not keep wanting to go deeper
        firsttime = False
        os.chdir('DataFiles') #goes into the DataFiles directory
    path = '{}Data.xlsx'.format(x) #this is the data file

    if x == 'Stock': #Inside the Stock function the ticker needs to be placed and then the extension
        path = '{}Data'.format(x) #This does mean that stock data will always be fully updated every time

    if not os.path.exists(path):
        print('{} data does not exists, building a new file'.format(x))
        df = getattr(ImportFile, 'get{}'.format(x))(TickerList,TickerName,path)
    else:
        print('checking and updating {} data'.format(x))
        DataFrame = pd.read_excel('{}Data.xlsx'.format(x),index_col=0)
        df = getattr(ImportFile, 'get{}'.format(x))(TickerList,TickerName,path,DataFrame)
        
        
os.chdir(maindirectory) #switches back to the path from which we started the run


#PERFile = os.path.isfile('PERData.xlsx')
#if PERFile == False:
#    print('PE-ratios data does not exist, building a new file')
#    df = getPER(TickerList,TickerName)
#elif PERFile == True:
#    PERData = pd.read_excel('PERData.xlsx',index_col=0)
#    print('checking and updating PE-ratios')
#    df = getPER(TickerList,TickerName,PERData)
    
    


#print('getting debt/equity ratios')
#getDER(TickerList,TickerName)
#print('getting revenues')
#getRev(TickerList,TickerName)
#print('getting earnings-per-share')
#df = getEPS(TickerList,TickerName)
#print('succes')


