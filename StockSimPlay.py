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
import random
import time

#load in the AXP data and select data from 2000 to 2001:
MainDirectory = os.getcwd()
os.chdir('DataFiles')
df = pd.read_excel('AXPData.xlsx')
os.chdir(MainDirectory)

#So now we only want to have the data of 2000-01-01 to 2000-12-31 roughly

DataPrepTimeBegin = time.time()
df1 = pd.DataFrame(data=None, columns=df.columns)
counter = 0
for i in range(len(df)):
    datecheck = str(df.Date[i])
    if datecheck[0:4] == '2000':
        df1.loc[datecheck] = df.iloc[i]
        
#now we will have to flip it in order to make it easier for ourselfs (2000-01-01 is not the start date)
df1 = df1.iloc[::-1]
DataPrepTimeEnd = time.time()
#we apperently start with 2000-01-03 I think it is because of weekends
#So from here on we will have to build some while/for loop that goes on untill the end of the data is reached
#It must containt buying and selling opertunities as described above!

States = ['Buy','Sell','Do nothing'] #These are the actions the agent has
StartingCapital = 1000 #The starting capital of the agent
AXPshares = 0 #counter of the amount of AXPshares
Cash = StartingCapital #Amount of cash, with which the agent can buy shares
#df2 is going to be the datalog file of what the agent does:
df2 = pd.DataFrame(data=None, columns = ['Day Number','Action','Cash','Stock Owned','Stock Worth','Net Worth','Closing Stock Price'])
SimulationTimeBegin = time.time()
print('The simulation Starts')
for i in range(len(df1)):
    if i == 0:
        Decision = random.randint(0,2) #This decides the action the agent takes
        Action = States[Decision] #this is the corresponding action
        if Action =='Buy' and (Cash-df1['Open'].iloc[i])>0:
            AXPshares += 1 #for now it only buys one share at a time
            Cash -= df1['Open'].iloc[i] #removing money from the cash
        elif Action == 'Sell' and AXPshares > 0:
            AXPshares -= 1 #selling 1 share
            Cash += df1['Open'].iloc[i] #adding money to cash
        else:
            pass
        
        
    else:
        Decision = random.randint(0,2) #This decides the action the agent takes
        Action = States[Decision] #this is the corresponding action
        if Action =='Buy' and (Cash-df1['Open'].iloc[i])>0:
            AXPshares += 1 #for now it only buys one share at a time
            Cash -= df1['Open'].iloc[i] #removing money from cash
        elif Action == 'Sell' and AXPshares > 0:
            AXPshares -= 1 #selling 1 share
            Cash += df1['Open'].iloc[i] #adding money to cash
        else:
            
            pass
    #save the important stuff here:
    df2 = df2.append({'Day Number':i,'Action':Action,'Cash':Cash,'Stock Owned':AXPshares,'Stock Worth':AXPshares*df1['Close'].iloc[i],'Net Worth':Cash + AXPshares*df1['Close'].iloc[i],'Closing Stock Price':df1['Close'].iloc[i]},ignore_index=True)
print('The simulation has finished')
SimulationTimeEnd = time.time()
#Saving the data on the right path:
os.chdir('DataFiles')
if not os.path.exists('SimulationTestData'):
    os.makedirs('SimulationTestData')
os.chdir('SimulationTestData')
df2.to_excel('1Stock1yearSim.xlsx') #For the user to see if everything went right
os.chdir(MainDirectory)

print('The total elapsed time for data preperation is: {}'.format(DataPrepTimeEnd - DataPrepTimeBegin))
print('The total elapsed time for the Simulation is: {}'.format( SimulationTimeEnd - SimulationTimeBegin))