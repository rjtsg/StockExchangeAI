import pandas as pd 
import urllib.request, io, csv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

TickerList = ['MMM', #Companies you want to include in your investigation, currently Dow Jones
'AXP',
'AAPL',
'BA',
'CAT',
'CVX',
'CSCO',
'KO',
'DOW',
'XOM',
'GS',
'HD',
'IBM',
'INTC',
'JNJ',
'JPM',
'MCD',
'MRK',
'MSFT',
'NKE',
'PFE',
'PG',
'TRV',
'UNH',
'UTX',
'VZ',
'V',
'WMT',
'WBA',
'DIS']

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

