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
import matplotlib.pyplot as plt
import RoyStates
import SvenStates

#load in the AXP data and select data from 2000 to 2001:
MainDirectory = os.getcwd()
os.chdir('DataFiles')
df = pd.read_excel('AXPData.xlsx')
os.chdir(MainDirectory)

#So now we only want to have the data of 2000-01-01 to 2000-12-31 roughly
num_states = 3
df1 = pd.DataFrame(data=None, columns=df.columns)
counter = 0
for i in range(len(df)):
    datecheck = str(df.Date[i])
    for j in range(2001,2002):
        if datecheck[0:4] == str(j):
            df1.loc[datecheck] = df.iloc[i]
        
#now we will have to flip it in order to make it easier for ourselfs (2000-01-01 is not the start date)
df1 = df1.iloc[::-1]


"""
Built here below the function that mimics the N-chain game and give the observation, reward, step?/done?
Define the reward table as a 3x3 matrix where State 1 is 2nd day ago closing price is higher,
state 2 is yesterdays closing price is higher and state 3 they are equal
being able to buy anymore shares. The reward should be something like the Net worth (cash+shares).
Further build it like the q_learning_keras function in RLtutMLadventuries.py
"""
# create the keras model


def q_learning_keras(num_episodes=100): #Number of training runs
    
    
    # now execute the q learning
    y = 0.25 
    eps = 0.5
    decay_factor = 0.999
    r_avg_list = []
    NumberSharesList = []
    NetWorthList = []
    CashList = []
    for i in range(num_episodes): #start the training
        eps *= decay_factor
        s = 0 #always start from state 0 (no shares)
        days = 0 #keeps track of the days
        Storage = {'AXPShares': 0, #Storage for other stuff
            'Cash': 1000,
            'Old_NetWorth': 1000}
        if i == 0:
            start = time.time()    #start timer on first run
        if i % 10 == 0:
            end = time.time()
            TimeLeft = ((num_episodes-i)/10)*(end-start) #Calculates the estimated time until completion
            hours, rem = divmod(TimeLeft, 3600)
            minutes, seconds = divmod(rem, 60)
            print("Episode {} of {}. Estimated time left {:0>2}:{:0>2}:{:0>2}".format(i + 1, num_episodes, int(hours),int(minutes),int(seconds)))
            start = time.time()
        done = False
        r_sum = 0 #total reward for 1 training
        while not done: #This plays the game untill it is done
            if np.random.random() < eps: #this decides the action
                a = np.random.randint(0, 3) #random action
            else:
                a = np.argmax(model.predict(np.identity(num_states)[s:s + 1]))
            new_s, r, Storage = TradeAction(a,Storage,days,df1) #This does the action So here the function must be called 
            target = r + y * np.max(model.predict(np.identity(num_states)[new_s:new_s + 1]))
            target_vec = model.predict(np.identity(num_states)[s:s + 1])[0]
            target_vec[a] = target
            model.fit(np.identity(num_states)[s:s + 1], target_vec.reshape(-1, 3), epochs=1, verbose=0)
            s = new_s
            r_sum += r
            days += 1 
            if days == len(df1): #This stops the While loop
                done = True
        #From here we save end values to plot and visualize:
        r_avg_list.append(r_sum)
        NumberSharesList.append(Storage['AXPShares'])
        NetWorthList.append(Storage['Old_NetWorth'])
        CashList.append(Storage['Cash'])
    return r_avg_list    
    
    
def TradeAction(action,Storage,days,DataFrame): #action is the action the agent chooses, while Storage is a dictionary which stores Trading process?
    #action 0 is buying
    #action 1 is selling
    #action 2 is holding on

    if action == 0 and (Storage['Cash']-DataFrame['Close'].iloc[days])>0:
            Storage['AXPShares'] += 1 #for now it only buys one share at a time
            Storage['Cash'] -= DataFrame['Close'].iloc[days] #removing money from cash
            exreward = 0
    elif action == 1 and Storage['AXPShares'] > 0:
            Storage['AXPShares'] -= 1 #selling 1 share
            Storage['Cash'] += DataFrame['Close'].iloc[days] #adding money to cash
            exreward = 0
    else:
        if action == 0 or action == 1:
            exreward = -10 #stops it from trading with no cash???
        if action == 2:
            exreward = 0

    
    state = RoyStates.Example(Storage,days,DataFrame)
    NetWorth = Storage['Cash'] + Storage['AXPShares']*DataFrame['Close'].iloc[days]
    reward = NetWorth - Storage['Old_NetWorth'] #+ exreward
    Storage['Old_NetWorth'] = NetWorth

    return state, reward, Storage

for i in range(1,3):
    model = Sequential()
    model.add(InputLayer(batch_input_shape=(1, num_states))) #should thus be the 3x1 vector (1,0,0) state0 state1 = (0,1,0) ...
    for j in range(1,i+1):
        model.add(Dense(150, activation='relu'))
    model.add(Dense(3, activation='linear')) #3 possible actions to be taken
    model.compile(loss='mse', optimizer='adam', metrics=['mae'])
    if i == 1:
        Rewards = q_learning_keras()
        RewardsB = Rewards
    else:
        Rewards = q_learning_keras()
        RewardsB = np.vstack((RewardsB,Rewards))

for k in range(0,i):
    plt.plot(RewardsB[k])

#add a legend!
plt.show()
        
