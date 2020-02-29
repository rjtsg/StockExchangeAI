import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
# from scipy.stats import pearsonr


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
CVX  = pd.read_excel('CVXData.xlsx')
DIS  = pd.read_excel('DISData.xlsx')
GS   = pd.read_excel('GSData.xlsx')
HD   = pd.read_excel('HDData.xlsx')
IBM  = pd.read_excel('IBMData.xlsx')


print(AAPL.head())
STOCKS = [AAPL, AXP, BA, CAT, CSCO, CVX, IBM, DIS, GS, HD]
STOCKS_string = ['AAPL', 'AXP', 'BA','CAT','CSCO','CVX','IBM','DIS','GS','HD']
for i in STOCKS:
    plt.plot(i['Date'],i['Close'])
plt.xlabel('Year')
plt.ylabel('Closing price [$]')
plt.legend(STOCKS_string)
plt.show()
print(PE_ratio.head())
for i in STOCKS_string:
    plt.plot(PE_ratio['Date'][::-1],PE_ratio[i][::-1])
plt.xticks(rotation=90)
plt.show()

#Do a PE-ratio over a year by adding
#Also take the return rate over that year
#Do it with a pandas dataframe for training/convenience
eval_years = np.arange(2006,2021)
pe_year_dict = {'Years': eval_years,
                'AAPL': np.zeros(len(eval_years)),
                'AXP':np.zeros(len(eval_years)),
                'BA':np.zeros(len(eval_years)),
                'CAT':np.zeros(len(eval_years)),
                'CSCO':np.zeros(len(eval_years)),
                'CVX':np.zeros(len(eval_years)),
                'IBM':np.zeros(len(eval_years)),
                'DIS':np.zeros(len(eval_years)),
                'GS':np.zeros(len(eval_years)),
                'HD':np.zeros(len(eval_years))}
annual_return_dict = {'Years': eval_years,
                'AAPL':np.zeros(len(eval_years)),
                'AXP':np.zeros(len(eval_years)),
                'BA':np.zeros(len(eval_years)),
                'CAT':np.zeros(len(eval_years)),
                'CSCO':np.zeros(len(eval_years)),
                'CVX':np.zeros(len(eval_years)),
                'IBM':np.zeros(len(eval_years)),
                'DIS':np.zeros(len(eval_years)),
                'GS':np.zeros(len(eval_years)),
                'HD':np.zeros(len(eval_years))}
pe_year_df = pd.DataFrame(data=pe_year_dict)
annual_return_df = pd.DataFrame(data=annual_return_dict)
for i in range(len(pe_year_df)):
    for j in range(len(PE_ratio)):
        if str(pe_year_df['Years'][i]) in PE_ratio['Date'][j]:
            for k in list(pe_year_df.columns.values)[1::]:
                if math.isnan(PE_ratio[k][j]):
                    pass
                else:
                    pe_year_df[k][i] += PE_ratio[k][j]
print(pe_year_df)

for i in range(len(annual_return_df)):
    for j in range(len(STOCKS)):
        all_dates = []
        # print(STOCKS_string[j])
        for k in range(len(STOCKS[j]['Date'])):
            if str(pe_year_df['Years'][i]) in str(STOCKS[j]['Date'][k]):
                all_dates.append(k)
        # print(all_dates)
        begin_index = all_dates[-1]
        end_index = all_dates[0]
        start_value = STOCKS[j]['Close'][begin_index]
        end_value = STOCKS[j]['Close'][end_index]
        # print(end_value, start_value)
        annual_return_df[STOCKS_string[j]][i] = (end_value - start_value) / \
                                                start_value * 100
print(annual_return_df)
x = []
y = []
for j in STOCKS_string:
    plt.scatter(pe_year_df[j],annual_return_df[j])
    for k in range(len(pe_year_df[j])):
        x.append(pe_year_df[j].iloc[k])
        y.append(annual_return_df[j].iloc[k])
plt.legend(STOCKS_string)
plt.ylabel('annual return')
plt.xlabel('added PE-Ratio')
plt.title('annual return vs PE-ratio correlation')
plt.show()
print('The correlation here is :',np.corrcoef(x,y)[0,1])
