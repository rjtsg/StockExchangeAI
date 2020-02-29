import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


print('hello world')
os.chdir('DataFiles')
dividend = pd.read_excel('DividendData.xlsx')
PE_ratio = pd.read_excel('PERData.xlsx')
earnings_per_share = pd.read_excel('EPSData.xlsx')
DER     = pd.read_excel('DERData.xlsx')
revenue = pd.read_excel('RevenueData.xlsx')

AAPL = pd.read_excel('AAPLData.xlsx')
AXP  = pd.read_excel('AXPData.xlsx')
BA   = pd.read_excel('BAData.xlsx')
CAT  = pd.read_excel('CATData.xlsx')
CSCO = pd.read_excel('CSCOData.xlsx')

print(AAPL.head())
STOCKS = [AAPL, AXP, BA, CAT, CSCO]
STOCKS_string = ['AAPL', 'AXP', 'BA', 'CAT', 'CSCO']
for i in STOCKS:
    plt.plot(i['Date'],i['Close'])
plt.xlabel('Year')
plt.ylabel('Closing price [$]')
plt.legend(STOCKS_string)
# plt.show()
print(PE_ratio.head())
for i in STOCKS_string:
    plt.plot(PE_ratio['Date'][::-1],PE_ratio[i][::-1])
plt.xticks(rotation=90)
# plt.show()

#Do a PE-ratio over a year by adding
#Also take the return rate over that year
#Do it with a pandas dataframe for training/convenience
eval_years = np.arange(2006,2021)
pe_year_dict = {'Years': eval_years,
                'AAPL': np.zeros(len(eval_years)),
                'AXP':np.zeros(len(eval_years)),
                'BA':np.zeros(len(eval_years)),
                'CAT':np.zeros(len(eval_years)),
                'CSCO':np.zeros(len(eval_years))}
annual_return_dict = {'Years': eval_years,
                'AAPL':np.zeros(len(eval_years)),
                'AXP':np.zeros(len(eval_years)),
                'BA':np.zeros(len(eval_years)),
                'CAT':np.zeros(len(eval_years)),
                'CSCO':np.zeros(len(eval_years))}
pe_year_df = pd.DataFrame(data=pe_year_dict)
annual_return_df = pd.DataFrame(data=annual_return_dict)
print(pe_year_df)
for i in range(len(pe_year_df)):
    for j in range(len(PE_ratio)):
        if str(pe_year_df['Years'][i]) in PE_ratio['Date'][j]:
            for k in list(pe_year_df.columns.values)[1::]:
                if math.isnan(PE_ratio[k][j]):
                    pass
                else:
                    pe_year_df[k][i] += PE_ratio[k][j]

print(pe_year_df)
