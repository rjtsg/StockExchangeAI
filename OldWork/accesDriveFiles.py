import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
import os
import pytz

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)


def getFileDrive(filename,drive):
    filename = '{}.xlsx'.format(filename)
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        if file1['title']==filename:
            file2 = drive.CreateFile({'id':file1['id']})
            file2.GetContentFile(filename)
            df = pd.read_excel(filename, index_col=0)
            os.remove(filename)
            return df

def delAllFileDrive(filename,drive):
    filename = '{}.xlsx'.format(filename)
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        if file1['originalFilename']==filename:
            file2 = drive.CreateFile({'id':file1['id']})
            file2.Delete()
    return '{} deleted'.format(filename)

def delOldFileDrive(filename,drive):
    filename = '{}.xlsx'.format(filename)
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    now = datetime.now(pytz.timezone('GMT'))
    for file1 in file_list:
        print(file1['createdDate'][:19],now.strftime("%Y/%m/%dT%H:%M:%S"))
        if file1['originalFilename']==filename and file1['createdDate'][:19] < now.strftime("%Y/%m/%dT%H:%M:%S"):
            file2 = drive.CreateFile({'id':file1['id']})
            file2.Delete()
    return '{} deleted'.format(filename)



def getDataFrameStock(ticker,drive):
    filename = 'StockData_{}.xlsx'.format(ticker)
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        if file1['title']==filename:
            file2 = drive.CreateFile({'id':file1['id']})
            file2.GetContentFile(filename)
            df = pd.read_excel(filename, index_col=0)
            print(df)
            df['Close/Open'] = df.loc[:,'Close']/df.loc[:,'Open']
            df['Open/Close'] = df.loc[:,'Open']/df.loc[:,'Close'].shift(1)
            os.remove(filename)
            return df

#printData = getDataFrameStock('V')

#print(printData.head())
# print('--------------------')            
# print(printData.iloc[-5:-1,:])

# dfDiv = getFileDrive('dividends')
# print(dfDiv.head())

# print(delOldFileDrive('dividends'))