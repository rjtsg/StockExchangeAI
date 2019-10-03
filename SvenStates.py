import numpy as np 
import pandas as pd 

def states(Storage,days,DataFrame):
    EmaState = ema(Storage,days,DataFrame) #0 or 1



    return EmaState

def ema(Storage,days,DataFrame):
    k = 0.1818
    Storage['Ema'] = DataFrame['Close'].iloc[days-1]*k + Storage['Ema']*(1-k)
    if (Storage['Ema'] > DataFrame['Close'].iloc[days-1]) and (DataFrame['Close'].iloc[days-1] > DataFrame['Close'].iloc[days-2]):
        state = 0
    elif (Storage['Ema'] > DataFrame['Close'].iloc[days-1]) and (DataFrame['Close'].iloc[days-1] <= DataFrame['Close'].iloc[days-2]): 
        state = 1
    elif (Storage['Ema'] <= DataFrame['Close'].iloc[days-1]) and (DataFrame['Close'].iloc[days-1] > DataFrame['Close'].iloc[days-2]):
        state = 2
    elif (Storage['Ema'] <= DataFrame['Close'].iloc[days-1]) and (DataFrame['Close'].iloc[days-1] <= DataFrame['Close'].iloc[days-2]):
        state = 3
    else:
        state = 4



    return state

