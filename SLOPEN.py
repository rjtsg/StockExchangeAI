import numpy as np 
import pandas as pd 
import sys 
import os
import random
import time
from keras.models import Sequential
from keras.layers import Dense, InputLayer
import matplotlib.pylab as plt
import RoyStates

MainDirectory = os.getcwd()
os.chdir('DataFiles')
df = pd.read_excel('AXPData.xlsx')
os.chdir(MainDirectory)

model = Sequential() 
model.add(InputLayer(batch_input_shape=(1,3))) #should thus be the 3x1 vector (1,0,0) state0 state1 = (0,1,0) ...
model.add(Dense(100, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(3, activation='linear')) #3 possible actions to be taken
model.compile(loss='mse', optimizer='adam', metrics=['mae'])

#generate dummy data
import numpy as np
data = np.random.random((1, 3))

print(model.predict(data))
action = np.argmax(model.predict(data))
print(action)
days = 1
Storage = {'AXPShares': 0, #Storage for other stuff
            'Cash': 1000,
            'Old_NetWorth': 1000}

df1 = pd.DataFrame(data=None, columns=df.columns)
counter = 0
for i in range(len(df)):
    datecheck = str(df.Date[i])
    if datecheck[0:4] == '2001':
        df1.loc[datecheck] = df.iloc[i]
        
#now we will have to flip it in order to make it easier for ourselfs (2000-01-01 is not the start date)
df1 = df1.iloc[::-1]

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
            exreward = -1 #stops it from trading with no cash???
        if action == 2:
            exreward = 0

    
    #Now the state has to be defined:
    #state0 = 2 days ago price is higher
    #state1 = 1 day ago price is higher
    #state2 = prices are equal
    #if DataFrame['Close'].iloc[days-2] > DataFrame['Close'].iloc[days-1] and days >= 2:
    #    state = 0
    #elif DataFrame['Close'].iloc[days-2] < DataFrame['Close'].iloc[days-1] and days >= 2:
    #    state = 1
    #else:
    #    state = 2
    state = RoyStates.History(Storage,days,DataFrame)
    #defining hte reward:
    #reward will be given as the difference between previousday networth and thisday networth
    NetWorth = Storage['Cash'] + Storage['AXPShares']*DataFrame['Close'].iloc[days]
    reward = NetWorth - Storage['Old_NetWorth'] + exreward
    Storage['Old_NetWorth'] = NetWorth

    return np.array(([state])), reward, Storage

new_s, r, Storage = TradeAction(action, Storage,days,df1)
print(new_s)
print(r)
print(Storage)
y = 0.9
target = r + y * np.max(model.predict(new_s))
print('target = ', target)
target_vec = model.predict(new_s)
print(target_vec)
target_vec[0][action] = target
model.fit(new_s,target_vec,epochs=1,verbose=0)


def Q_LEARNING(num_episodes=100):
    y = 0.95
    eps = 0.5
    decay_factor = 0.999
    r_avg_list = []
    for i in range(num_episodes): #start the training
        eps *= decay_factor
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
        state = np.random.random((1, 3)) #initial
        r_sum = 0 #total reward for 1 training
        while not done: #This plays the game untill it is done
            if np.random.random() < eps: #this decides the action
                action = np.random.randint(0, 3) #random action
            else:
                action = np.argmax(model.predict(state))
            new_s, r, Storage = TradeAction(action, Storage,days,df1)
            target = r + y * np.max(model.predict(new_s))
            target_vec[0][action] = target
            model.fit(new_s,target_vec,epochs=1,verbose=0)
            state = new_s
            #print(state)
            r_sum += r
            days += 1
            if days == len(df1): #This stops the While loop
                done = True
        r_avg_list.append(r_sum)
    plt.plot(r_avg_list)
    plt.ylabel('Average reward per game')
    plt.xlabel('Number of games')
    plt.show()
    print(Storage)
    

Q_LEARNING()

TestYear = pd.DataFrame(data=None, columns=df.columns)
counter = 0
for i in range(len(df)):
    datecheck = str(df.Date[i])
    if datecheck[0:4] == '2002':
        TestYear.loc[datecheck] = df.iloc[i]

TestYear = TestYear.iloc[::-1]

#eventually make this into an evaluation function, to make it callable
SimulationYears = 1
days = 0 #keeps track of the days
TestStorage = {'AXPShares': 0, #Storage for other stuff
            'Cash': 1000,
            'Old_NetWorth': 1000}
done = False
state = np.random.random((1, 3)) #initial #always start from state 0 (no shares), wierd: how are we gonna do this
while not done: #This plays the game untill it is done
    a = np.argmax(model.predict(state))
    print(a,state)
    new_s, r, TestStorage = TradeAction(a,TestStorage,days,TestYear) #This does the action So here the function must be called 
    state = new_s
    days += 1 
    if days == len(TestYear): #This stops the While loop
        done = True

StartNetWorth = 1000
TestNetWorth = TestStorage['Old_NetWorth']
StartClose = TestYear['Close'][0]
EndClose = TestYear['Close'][-1]
CAGRAXP = (EndClose/StartClose)**(1/SimulationYears) - 1 #Annual return: https://www.investopedia.com/terms/a/annual-return.asp
CAGRAgent = (TestNetWorth/StartNetWorth)**(1/SimulationYears) - 1 #annual return of the agent
print('The annual return of the axp is %.2f percent and the agents annaul return is %.2f percent' % (CAGRAXP, CAGRAgent))
