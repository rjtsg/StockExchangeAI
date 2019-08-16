import requests, bs4, re
import pandas as pd
import xlrd
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import time
import lxml

from ImportPERData import getPER
from ImportDERData import getDER
from ImportRevenueData import getRev
from ImportEPSData import getEPS

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)


BeginYear = 2019
TickerList=list(pd.read_excel('tickers.xlsx').iloc[:,0])
TickerName=list(pd.read_excel('tickers.xlsx').iloc[:,1])

print('getting PE-ratios')
getPER(TickerList,TickerName,BeginYear,drive)
print('getting debt/equity ratios')
getDER(TickerList,TickerName,BeginYear,drive)
print('getting revenues')
getRev(TickerList,TickerName,BeginYear,drive)
print('getting earnings-per-share')
getEPS(TickerList,TickerName,BeginYear,drive)
print('succes')


