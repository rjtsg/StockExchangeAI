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
    if datecheck[0:4] == '2001':
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
model = Sequential() 
model.add(InputLayer(batch_input_shape=(1, 3))) #should thus be the 3x1 vector (1,0,0) state0 state1 = (0,1,0) ...
model.add(Dense(1000, activation='sigmoid'))
model.add(Dense(1000, activation='sigmoid'))
model.add(Dense(1000, activation='sigmoid'))
model.add(Dense(3, activation='linear')) #3 possible actions to be taken
model.compile(loss='mse', optimizer='adam', metrics=['mae'])

def q_learning_keras(num_episodes=100): #Number of training runs
    
    
    # now execute the q learning
    y = 0.95 
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
                a = np.argmax(model.predict(np.identity(3)[s:s + 1]))
            new_s, r, Storage = TradeAction(a,Storage,days,df1) #This does the action So here the function must be called 
            target = r + y * np.max(model.predict(np.identity(3)[new_s:new_s + 1]))
            target_vec = model.predict(np.identity(3)[s:s + 1])[0]
            target_vec[a] = target
            model.fit(np.identity(3)[s:s + 1], target_vec.reshape(-1, 3), epochs=1, verbose=0)
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

    plt.plot(r_avg_list)
    plt.ylabel('Average reward per game')
    plt.xlabel('Number of games')
    plt.show()
    fig, (ax1, ax2, ax3) = plt.subplots(3,1,sharex=True)
    ax1.plot(NumberSharesList)
    ax1.set_ylabel('# shares')
    ax1.set_title('# of shares at the end of a game')
    ax2.plot(NetWorthList)
    ax2.set_ylabel('$')
    ax2.set_title('NetWorth at the end of a game')
    ax3.plot(CashList)
    ax3.set_ylabel('$')
    ax3.set_title('Cash at the end of a game')
    plt.show()
    AgentRL = np.ndarray((3,3))
    for i in range(3):
        print("State {} - action {}".format(i, model.predict(np.identity(3)[i:i + 1])))
        AgentRL[i] =  model.predict(np.identity(3)[i:i + 1])
        #print(AgentRL)
    return AgentRL
    
    
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
    
    #Now the state has to be defined:
    #state0 = 2 days ago price is higher
    #state1 = 1 day ago price is higher
    #state2 = prices are equal
    if DataFrame['Close'].iloc[days-2] > DataFrame['Close'].iloc[days-1] and days >= 2:
        state = 0
    elif DataFrame['Close'].iloc[days-2] < DataFrame['Close'].iloc[days-1] and days >= 2:
        state = 1
    else:
        state = 2
    
    #defining hte reward:
    #reward will be given as the difference between previousday networth and thisday networth
    NetWorth = Storage['Cash'] + Storage['AXPShares']*DataFrame['Close'].iloc[days]
    reward = NetWorth - Storage['Old_NetWorth']
    Storage['Old_NetWorth'] = NetWorth

    return state, reward, Storage

AgentRL = q_learning_keras()
print(AgentRL)
"""
generate the test year (2001) and see how the model performs on this and compare to anual return of that 
year for the stock
"""
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
s = 0 #always start from state 0 (no shares)
while not done: #This plays the game untill it is done
    a = np.argmax(model.predict(np.identity(3)[s:s + 1]))
    print(a,s)
    new_s, r, TestStorage = TradeAction(a,TestStorage,days,TestYear) #This does the action So here the function must be called 
    s = new_s
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

"""
Different states can apperently increase computational time pretty hard.
"""
