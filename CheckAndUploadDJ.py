import requests, bs4, re
import pandas as pd
import xlrd
import win32com.client as win32
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import time

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
xls_path = r'C:\Users\Roy\AppData\Local\Programs\Python\Python37\AIstockexchange\StockExchangeAI\Financial_Report.xls'
deleting = 0
DriveTitles = list()

def del_file(x2,third2):
    os.remove('Financial_Report{}_{}.xlsx'.format(x2,third2))

def xls_2_xlsx(xls_path, xlsx_path):
    # Create temp xlsx-File
    if os.path.exists(xlsx_path): os.remove(xlsx_path)

    excel = win32.DispatchEx("Excel.Application")
    excel.Visible = 0
    wb = excel.Workbooks.Open(xls_path)

    wb.SaveAs(xlsx_path, FileFormat = 51)    #FileFormat = 51 is for .xlsx extension
    wb.Close()


CikList = {'MMM':'0000066740', #Companies you want to include in your investigation
'AXP':'0000004962',
'AAPL':'0000320193',
'BA':'0000012927',
'CAT':'0000018230',
'CVX':'0000093410',
'CSCO':'0000858877',
'KO':'0000021344',
'DOW':'0001751788',
'XOM':'0000034088',
'GS':'0000886982',
'HD':'0000354950',
'IBM':'0000051143',
'INTC':'0000050863',
'JNJ':'0000200406',
'JPM':'0000019617',
'MCD':'0000063908',
'MRK':'0000310158',
'MSFT':'0000789019',
'NKE':'0000320187',
'PFE':'0000078003',
'PG':'0000080424',
'TRV':'0000086312',
'UNH':'0000731766',
'UTX':'0000101829',
'VZ':'0000732712',
'V':'0001403161',
'WMT':'0000104169',
'WBA':'0001618921',
'DIS':'0001744489'
        }
for x in CikList: #runs through the CikList

    CIK = CikList[x]
    res = requests.get('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=10-Q&dateb=&owner=exclude&count=40'.format(CIK)) #downloads html page
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text) #reads html page of the quartlerly reports

    list2 = soup.findAll(string=re.compile(r'\d\d\d\d-\d\d-\d\d'))
        
    for i in range(0,len(list2)):
        if (str(CIK[3]) == '0'): 
            first = str(CIK[5:10])
        else: 
            first = str(CIK[4:10])
        
        if list2[0][0:6] != 'Acc-no':
            #print('ok')
            if i == 0:
                pass
            elif i % 2 ==0:
                third = list2[i]
                #print('third = '+third)
            elif i % 1 == 0:
                second = str(list2[i][8:18]+ list2[i][19:21] + list2[i][22:28])
                #print(second)
                try: 
                    url = 'https://www.sec.gov/Archives/edgar/data/{}/{}/Financial_Report.xlsx'.format(first,second)
                    sheet = pd.read_excel(url)
                    print('File can be accessed from the SEC site')
                except:
                    UploadFile = 'Financial_Report{}_{}.xlsx'.format(x,third)
                    for file1 in file_list:
                        DriveTitles.append(file1['title'])
                    if UploadFile in DriveTitles:
                        print('This file is already on the drive')
                    else:
                        xlsx_path = r'C:\Users\Roy\AppData\Local\Programs\Python\Python37\AIstockexchange\StockExchangeAI\Financial_Report{}_{}.xlsx'.format(x,third)
                        url = 'https://www.sec.gov/Archives/edgar/data/{}/{}/Financial_Report.xls'.format(first,second)
                        r = requests.get(url, allow_redirects=True)
                        open('Financial_Report.xls','wb').write(r.content) #saves the temporary file on your computer
                        xls_2_xlsx(xls_path,xlsx_path) #converts the .xls file to a .xlsx file
                        os.remove('Financial_Report.xls') #removes the temporary file from your computer
                        file1 = drive.CreateFile()
                        file1.SetContentFile('Financial_Report{}_{}.xlsx'.format(x,third))
                        file1.Upload()
                        print('File uploaded to drive succesfully')
                        if deleting == 0:
                            x2 = x
                            third2 = third
                            deleting += 1
                        else:
                            del_file(x2,third2)
                            x2 = x
                            third2 = third
                            deleting += 1
        else:
            if i == 0:
                second = str(list2[i][8:18]+ list2[i][19:21] + list2[i][22:28])
                #print(second)
            elif i % 2 == 0:
                second = str(list2[i][8:18]+ list2[i][19:21] + list2[i][22:28])
                #print(second)
            elif i % 1 == 0:
                third = list2[i]
                #print('third = '+third)
            
                #print('out of except')
                #WorkHorse(x,first,second,third)
                try: 
                    url = 'https://www.sec.gov/Archives/edgar/data/{}/{}/Financial_Report.xlsx'.format(first,second)
                    sheet = pd.read_excel(url)
                    print('File can be accessed from the SEC site')
                except:
                    UploadFile = 'Financial_Report{}_{}.xlsx'.format(x,third)
                    for file1 in file_list:
                        DriveTitles.append(file1['title'])
                    if UploadFile in DriveTitles:
                        print('This file is already on the drive')
                    else:
                        xlsx_path = r'C:\Users\Roy\AppData\Local\Programs\Python\Python37\AIstockexchange\StockExchangeAI\Financial_Report{}_{}.xlsx'.format(x,third)
                        url = 'https://www.sec.gov/Archives/edgar/data/{}/{}/Financial_Report.xls'.format(first,second)
                        r = requests.get(url, allow_redirects=True)
                        open('Financial_Report.xls','wb').write(r.content) #saves the temporary file on your computer
                        xls_2_xlsx(xls_path,xlsx_path) #converts the .xls file to a .xlsx file
                        os.remove('Financial_Report.xls') #removes the temporary file from your computer
                        file1 = drive.CreateFile()
                        file1.SetContentFile('Financial_Report{}_{}.xlsx'.format(x,third))
                        file1.Upload()
                        print('File uploaded to drive succesfully')
                        if deleting == 0:
                            x2 = x
                            third2 = third
                            deleting += 1
                        else:
                            del_file(x2,third2)
                            x2 = x
                            third2 = third
                            deleting += 1
            

