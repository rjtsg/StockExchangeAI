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
def q_learning_keras(num_episodes=100): #Number of training runs
    # create the keras model
    model = Sequential()
    model.add(InputLayer(batch_input_shape=(1, 3))) #should thus be the 3x1 vector (1,0,0) state0 state1 = (0,1,0) ...
    model.add(Dense(10, activation='sigmoid'))
    model.add(Dense(3, activation='linear')) #3 possible actions to be taken
    model.compile(loss='mse', optimizer='adam', metrics=['mae'])
    # now execute the q learning
    y = 0.95
    eps = 0.5
    decay_factor = 0.999
    r_avg_list = []
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
            TimeLeft = (num_episodes-i)*(end-start) #Calculates the estimated time until completion
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
                a = np.argmax(model.predict(np.identity(3)[s:s + 1]))
            new_s, r, Storage = TradeAction(a,Storage,days) #This does the action So here the function must be called 
            target = r + y * np.max(model.predict(np.identity(3)[new_s:new_s + 1]))
            target_vec = model.predict(np.identity(3)[s:s + 1])[0]
            target_vec[a] = target
            model.fit(np.identity(3)[s:s + 1], target_vec.reshape(-1, 3), epochs=1, verbose=0)
            s = new_s
            r_sum += r
            days += 1 
            if days == len(df1): #This stops the While loop
                done = True
        r_avg_list.append(r_sum)
    plt.plot(r_avg_list)
    plt.ylabel('Average reward per game')
    plt.xlabel('Number of games')
    plt.show()
    for i in range(3):
        print("State {} - action {}".format(i, model.predict(np.identity(3)[i:i + 1])))
    


def TradeAction(action,Storage,days): #action is the action the agent chooses, while Storage is a dictionary which stores Trading process?
    #action 0 is buying
    #action 1 is selling
    #action 2 is holding on

    if action == 0 and (Storage['Cash']-df1['Close'].iloc[days])>0:
            Storage['AXPShares'] += 1 #for now it only buys one share at a time
            Storage['Cash'] -= df1['Close'].iloc[days] #removing money from cash
    elif action == 1 and Storage['AXPShares'] > 0:
            Storage['AXPShares'] -= 1 #selling 1 share
            Storage['Cash'] += df1['Close'].iloc[days] #adding money to cash
    else:
        pass
    
    #Now the state has to be defined:
    #state0 = no shares
    #state1 = shares
    #state2 = no cash
    if Storage['AXPShares'] == 0:
        state = 0
    elif Storage['Cash'] - df1['Close'].iloc[days] <= 0:
        state = 2
    else:
        state = 1
    
    #defining hte reward:
    #reward will be given as the difference between previousday networth and thisday networth
    NetWorth = Storage['Cash'] + Storage['AXPShares']*df1['Close'].iloc[days]
    reward = NetWorth - Storage['Old_NetWorth']
    Storage['Old_NetWorth'] = NetWorth

    return state, reward, Storage

q_learning_keras()