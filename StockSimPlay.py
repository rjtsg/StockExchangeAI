""" 
This file should let us choose a decision of buying, holding, selling a stock (if available).
It will load in the close data from the AXP stock data. The game will take us from 2000 to 20001.
Which means it simulates 1 year of stock trading. The user will start with an amount of cash of 
$10,000. He will see the first starting price for day 1, he can than decide to trade or not. After that
he will see the closing price of that day and on wards will only see closing prices of the following days.
After each trading day the user will see the following outputs: day number, cash money, stock owned, stock worth and total money.
If the trading day is done the closing price will be presented. 

A good idea is to save trading dates, money gotten from trades, buying prices, selling prices. 
Calculate annual return of trader and that of the stock. It would be nice if some plot would be made.
"""

#To start of import the needed packages:
import numpy as np 
import pandas as pd 
import sys 
import os

#load in the AXP data and select data from 2000 to 2001:
MainDirectory = os.getcwd()
os.chdir('DataFiles')
df = pd.read_excel('AXPData.xlsx')
os.chdir(MainDirectory)

#So now we only want to have the data of 2000-01-01 to 2000-12-31 roughly
df1 = pd.DataFrame(data=None, columns=df.columns)
counter = 0
for i in range(len(df)):
    datecheck = str(df.Date[i])
    if datecheck[0:4] == '2000':
        df1.loc[datecheck] = df.iloc[i]
        
#now we will have to flip it in order to make it easier for ourselfs (2000-01-01 is not the start date)
df1 = df1.iloc[::-1]
#we apperently start with 2000-01-03, which is probably due to missing data.
#So from here on we will have to build some while loop that goes on untill the end of the data is reached
#It must containt buying and selling opertunities as described above!
