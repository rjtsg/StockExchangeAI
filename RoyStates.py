#Imports:
import pandas as pd
import numpy as np

def Example(Storage,days,DataFrame):
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

def ShortTerm(Storage,days,DataFrame):
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

def LongTerm(Storage,days,DataFrame):
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