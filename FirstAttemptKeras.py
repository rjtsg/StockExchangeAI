""" 
So here I try to build the StockSimPlay.py for-loop into a function, which should give outputs like
gym.openai.com environments does. Then implement the greedy epsilon deep Q learning from RLtutMLadventuries.py
to see if anything interesting happens. We still use 1 stock for 1 year.
"""

#Import packages:
import numpy as np 
import pandas as pd 
import sys 
import os
import random
import time
from keras.models import Sequential
from keras.layers import Dense, InputLayer
import matplotlib.pylab as plt

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

"""
Built here below the function that mimics the N-chain game and give the observation, reward, step?/done?
Define the reward table as a 3x3 matrix where State 1 is having no shares, state 2 is having shares and state 3 is not
being able to buy anymore shares. The reward should be something like the Net worth (cash+shares).
Further build it like the q_learning_keras function in RLtutMLadventuries.py
"""
