import pandas as pd 
import urllib.request, io, csv

ticker = 'V'
url = urllib.request.urlopen('http://download.macrotrends.net/assets/php/stock_data_export.php?t={}'.format(ticker)) 
datareader = csv.reader(io.TextIOWrapper(url))
df = pd.DataFrame(list(datareader)[15:], columns=['date','open','high','low','close','volume'])

print(df.head())

