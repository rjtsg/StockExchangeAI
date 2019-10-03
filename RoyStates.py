#Imports:
import pandas as pd
import numpy as np

def Example(Storage,days,DataFrame): #3 states
    #state0 = 2 days ago price is higher
    #state1 = 1 day ago price is higher
    #state2 = prices are equal
    if DataFrame['Close'].iloc[days-2] > DataFrame['Close'].iloc[days-1] and days >= 2:
        state = 0
    elif DataFrame['Close'].iloc[days-2] < DataFrame['Close'].iloc[days-1] and days >= 2:
        state = 1
    else:
        state = 2
    return state

def ShortTerm(Storage,days,DataFrame): #6 states
    closing_price = DataFrame['Close'].iloc[days-1]
    trading_period_short = 5
    list_short = []
    if trading_period_short < days:
        for i in range(0,trading_period_short):
            list_short.append(DataFrame['Close'].iloc[days - i])
        short_period_low = np.min(list_short)
        short_period_high = np.max(list_short)
        if closing_price <= short_period_low:
            position_relative_short = 0
        elif closing_price <= (short_period_low + 0.2 * (short_period_high - short_period_low)):
            position_relative_short = 1
        elif closing_price <= (short_period_low + 0.8 * (short_period_high - short_period_low)):
            position_relative_short = 2
        elif closing_price <= short_period_high:
            position_relative_short = 3
        elif closing_price > short_period_high:
            position_relative_short = 4
    else:
        position_relative_short = 5
    return position_relative_short

def LongTerm(Storage,days,DataFrame): #6 states
    closing_price = DataFrame['Close'].iloc[days-1]
    trading_period_long = 20
    list_long = []
    if trading_period_long < days:
        for i in range(0,trading_period_long):
            list_long.append(DataFrame['Close'].iloc[days - i])
        long_period_low = np.min(list_long)
        long_period_high = np.max(list_long)
        if closing_price <= long_period_low:
            position_relative_long = 0
        elif closing_price <= (long_period_low + 0.2 * (long_period_high - long_period_low)):
            position_relative_long = 1
        elif closing_price <= (long_period_low + 0.8 * (long_period_high - long_period_low)):
            position_relative_long = 2
        elif closing_price <= long_period_high:
            position_relative_long = 3
        elif closing_price > long_period_high:
            position_relative_long = 4
    else:
        position_relative_long = 5
    return position_relative_long

def ShortLongTerm(Storage,days,DataFrame): #36 states
    closing_price = DataFrame['Close'].iloc[days-1]
    trading_period_short = 5
    trading_period_long = 20
    list_short = []
    list_long = []
    if trading_period_short < days:
        for i in range(0,trading_period_short):
            list_short.append(DataFrame['Close'].iloc[days - i])
        short_period_low = np.min(list_short)
        short_period_high = np.max(list_short)
        if closing_price <= short_period_low:
            position_relative_short = 0
        elif closing_price <= (short_period_low + 0.2 * (short_period_high - short_period_low)):
            position_relative_short = 1
        elif closing_price <= (short_period_low + 0.8 * (short_period_high - short_period_low)):
            position_relative_short = 2
        elif closing_price <= short_period_high:
            position_relative_short = 3
        elif closing_price > short_period_high:
            position_relative_short = 4
    else:
        position_relative_short = 5
    
    if trading_period_long < days:
        for i in range(0,trading_period_long):
            list_long.append(DataFrame['Close'].iloc[days - i])
        long_period_low = np.min(list_long)
        long_period_high = np.max(list_long)
        if closing_price <= long_period_low:
            position_relative_long = 0
        elif closing_price <= (long_period_low + 0.2 * (long_period_high - long_period_low)):
            position_relative_long = 1
        elif closing_price <= (long_period_low + 0.8 * (long_period_high - long_period_low)):
            position_relative_long = 2
        elif closing_price <= long_period_high:
            position_relative_long = 3
        elif closing_price > long_period_high:
            position_relative_long = 4
    else:
        position_relative_long = 5
    
    """
    Construct the for-loop that creates the 36 states.
    First short term, second long term (1,1) is the second state of both and has count number of 7? or 8?
    """
    StateCount = 0 #number of states, each number is a state
    for i in range(0,6): #short term
        for j in range(0,6): #long term
            if i == position_relative_short:
                if j == position_relative_long:
                    state = StateCount
            StateCount += 1
    
    return state

def FreeCash(Storage,days,DataFrame): #4 states
    FreeCash = Storage['Cash']
    NetWorth = Storage['Old_NetWorth']
    if FreeCash / NetWorth <= 0.25:
        state = 0
    elif FreeCash / NetWorth > 0.25 and FreeCash / NetWorth <= 0.5:
        state = 1
    elif FreeCash / NetWorth > 0.5 and FreeCash / NetWorth <= 0.75:
        state = 2
    elif FreeCash / NetWorth > 0.75: #and FreeCash / NetWorth <= 1:
        state = 3
    #print(FreeCash/NetWorth)
    return state

def Gradient10(Storage,days,DataFrame): #3 states
    GradientDays = 11
    HistDay = DataFrame['Close'].iloc[days - GradientDays]
    CurrDay = DataFrame['Close'].iloc[days - 1]
    Grad = CurrDay - HistDay
    if Grad > 0:
        state = 0
    elif Grad < 0:
        state = 1
    elif Grad == 0:
        state = 2
    return state

def ShortLongTermCash(Storage,days,DataFrame): #144 states?
    closing_price = DataFrame['Close'].iloc[days-1]
    trading_period_short = 5
    trading_period_long = 20
    list_short = []
    list_long = []
    FreeCash = Storage['Cash']
    NetWorth = Storage['Old_NetWorth']
    if trading_period_short < days:
        for i in range(0,trading_period_short):
            list_short.append(DataFrame['Close'].iloc[days - i])
        short_period_low = np.min(list_short)
        short_period_high = np.max(list_short)
        if closing_price <= short_period_low:
            position_relative_short = 0
        elif closing_price <= (short_period_low + 0.2 * (short_period_high - short_period_low)):
            position_relative_short = 1
        elif closing_price <= (short_period_low + 0.8 * (short_period_high - short_period_low)):
            position_relative_short = 2
        elif closing_price <= short_period_high:
            position_relative_short = 3
        elif closing_price > short_period_high:
            position_relative_short = 4
    else:
        position_relative_short = 5
    
    if trading_period_long < days:
        for i in range(0,trading_period_long):
            list_long.append(DataFrame['Close'].iloc[days - i])
        long_period_low = np.min(list_long)
        long_period_high = np.max(list_long)
        if closing_price <= long_period_low:
            position_relative_long = 0
        elif closing_price <= (long_period_low + 0.2 * (long_period_high - long_period_low)):
            position_relative_long = 1
        elif closing_price <= (long_period_low + 0.8 * (long_period_high - long_period_low)):
            position_relative_long = 2
        elif closing_price <= long_period_high:
            position_relative_long = 3
        elif closing_price > long_period_high:
            position_relative_long = 4
    else:
        position_relative_long = 5
    
    
    if FreeCash / NetWorth <= 0.25:
        CashState = 0
    elif FreeCash / NetWorth > 0.25 and FreeCash / NetWorth <= 0.5:
        CashState = 1
    elif FreeCash / NetWorth > 0.5 and FreeCash / NetWorth <= 0.75:
        CashState = 2
    elif FreeCash / NetWorth > 0.75: #and FreeCash / NetWorth <= 1:
        CashState = 3

    StateCount = 0 #number of states, each number is a state
    for i in range(0,6): #short term
        for j in range(0,6): #long term
            for k in range(0,4):
                if i == position_relative_short:
                    if j == position_relative_long:
                        if k == CashState:
                            state = StateCount
                StateCount += 1
    
    return state
"""
def History(Storage,days,DataFrame): #1?
    avelist = []
    if days == 0:
        state = [DataFrame['Open'].iloc[days], Storage['Cash'], Storage['AXPShares'],DataFrame['Open'].iloc[days]]
    else:
        if days < 6:
            i = days
            for i in range(1,i):
                avelist.append(DataFrame['Close'].iloc[days-i])
            FiveDayAve = np.sum(avelist)/i
        else:
             for j in range(1,6):
                avelist.append(DataFrame['Close'].iloc[days-j])
             FiveDayAve = np.sum(avelist)/5
        state = [DataFrame['Close'].iloc[days-1], Storage['Cash'], Storage['AXPShares'],FiveDayAve]
    return state
"""

def SMA10(Storage,days,DataFrame): #3 states higher or lower and not in range
    if days > 10:
        Averaging = np.empty(10)
        for i in range(1,11):
            Averaging[i-1] = (DataFrame['Close'][days - i])
        SMA = np.sum(Averaging)/10
        if SMA >= DataFrame['Close'][days-1]:
            state = 0
        elif SMA < DataFrame['Close'][days-1]:
            state = 1
    else:
        state = 2
    return state

def CMA(Storage,days,DataFrame):
    Cumulative = []
    if days > 0:
        for i in range(days-1):
            Cumulative.append(DataFrame['Close'][days - i])
        CMA = np.sum(Cumulative)/days
        if CMA >= DataFrame['Close'][days-1]:
            state = 0
        elif CMA < DataFrame['Close'][days-1]:
            state = 1
    else:
        state = 2
    return state

