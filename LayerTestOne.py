""" 
This code will build an function through which the amount of layers will be iterated upon in order to asses 
the influence of this in the learning process. Eventually it is the idea that this function should be able to
test multiple parameters. 
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
df1 = pd.DataFrame(data=None, columns=df.columns)
counter = 0
for i in range(len(df)):
    datecheck = str(df.Date[i])
    for j in range(2001,2002): #user input!!!!
        if datecheck[0:4] == str(j):
            df1.loc[datecheck] = df.iloc[i]
        
#now we will have to flip it in order to make it easier for ourselfs (2000-01-01 is not the start date)
df1 = df1.iloc[::-1]


"""
q_learning_keras is the reinforcement learning function which can be called to run the aget
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
            
    elif action == 1 and Storage['AXPShares'] > 0:
            Storage['AXPShares'] -= 1 #selling 1 share
            Storage['Cash'] += DataFrame['Close'].iloc[days] #adding money to cash
            
    else:
        pass

    #the state method:
    state = RoyStates.Example(Storage,days,DataFrame)
    
    NetWorth = Storage['Cash'] + Storage['AXPShares']*DataFrame['Close'].iloc[days]
    reward = NetWorth - Storage['Old_NetWorth'] 
    Storage['Old_NetWorth'] = NetWorth

    return state, reward, Storage


""" 
From here on onwards the code that should test the influence of the layers will be developed.
This should be a function with the input the number of layers that need to be tested. It should return
some valuable plots and save them on the server.

A problem is that when you put it in a function the 'model' becomes local... how to make it global again? just putting 
global model in the code hah.
"""
def LayerAssesment(MinL=1,MaxL=3): #This function will thus always asses layers 1 to 3 
    global model
    MaxL += 1 #in order to actually create the number of layers the user wants
    for i in range(MinL,MaxL): #This for-loop resets the model after each assesment
        model = Sequential()
        model.add(InputLayer(batch_input_shape=(1, num_states))) #should thus be the 3x1 vector (1,0,0) state0 state1 = (0,1,0) ...
        for j in range(MinL,i+1): #loop in order to create the right amount of layers each time
            model.add(Dense(150, activation='relu')) #adds layers
        model.add(Dense(3, activation='linear')) #3 possible actions to be taken (output layer)
        model.compile(loss='mse', optimizer='adam', metrics=['mae'])
        #saving mechanism:
        if i == MinL:
            Rewards = q_learning_keras()
            RewardsB = Rewards
        else:
            Rewards = q_learning_keras()
            RewardsB = np.vstack((RewardsB,Rewards))

    for k in range(0,MaxL-1):
        plt.plot(RewardsB[k])

    #add a legend! need some list created or something
    LegendList = ['{} layer(s)'.format(MinL)]
    for k in range(MinL+1,MaxL+1):
        LegendList.append('{} layer(s)'.format(k))
    plt.legend(LegendList)
    plt.show()

#User input number of states related to the state mechanism that is used.
num_states = 3
#Call the LayerAssesment
LayerAssesment(2,4)