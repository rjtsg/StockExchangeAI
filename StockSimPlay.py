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

#load in the AXP data and select data from 2000 to 2001:
sys.path.append('DataFiles')