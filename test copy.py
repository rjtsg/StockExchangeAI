import requests, bs4, re
import pandas as pd

CikList = {'MMM':'0000066740',
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
for x in CikList:

    CIK = CikList[x]
    res = requests.get('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=10-Q&dateb=&owner=exclude&count=40'.format(CIK))
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text)

    zoeken = str(soup.find(string=re.compile('Acc-no')))
    if (str(CIK[3]) == '0'): 
        first = str(CIK[4:10])
    else: 
        first = str(CIK[3:10])

    second = str(zoeken[8:18]+ zoeken[19:21] + zoeken[22:28])

    url = 'https://www.sec.gov/Archives/edgar/data/{}/{}/Financial_Report.xlsx'.format(first,second)
    print(url)
    sheet = pd.read_excel(url)

    print(sheet)
