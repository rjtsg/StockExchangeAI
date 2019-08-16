import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


def getFileDrive(filename):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    filename = '{}.xlsx'.format(filename)
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        if file1['title']==filename:
            file2 = drive.CreateFile({'id':file1['id']})
            file2.GetContentFile(filename)
            df = pd.read_excel(filename, index_col=0)
            os.remove(filename)
            return df

def delFileDrive(filename):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    filename = '{}.xlsx'.format(filename)
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        if file1['title']==filename:
            file2 = drive.CreateFile({'id':file1['id']})
            file2.Delete()
            return 'Done'


def getDataFrameStock(ticker):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    filename = 'StockData_{}.xlsx'.format(ticker)
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        if file1['title']==filename:
            file2 = drive.CreateFile({'id':file1['id']})
            file2.GetContentFile(filename)
            df = pd.read_excel(filename, index_col=1).iloc[:,1:]
            df['close/open'] = df.loc[:,'close']/df.loc[:,'open']
            df['open/close'] = df.loc[:,'open']/df.loc[:,'close'].shift(1)
            os.remove(filename)
            return df

#printData = getDataFrameStock('V')

# print(printData.head())
# print('--------------------')            
# print(printData.iloc[-5:-1,:])

# dfDiv = getFileDrive('dividends')
# print(dfDiv.head())