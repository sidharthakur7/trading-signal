#!/usr/bin/env python
# coding: utf-8

# In[7]:


import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

#Downloading Stock Data
data = yf.download("TCS.NS", start="2026-02-01",end="2026-03-25", interval="15m", multi_level_index=False)
data.index=pd.to_datetime(data.index)
data['Date']=data.index.date

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(1)

#Creating Featues of Data
window = 20
data['mean'] = data['Close'].rolling(window).mean()
data['std'] = data['Close'].rolling(window).std()
data['z_score'] = (data['Close'] - data['mean']) / data['std']

#Duplicate & Missing values are removed
data.dropna(inplace=True)

#Setting Buy/Sell Conditions
data['signal']=0
data.loc[data['z_score']< -0.75,'signal']=1
data.loc[data['z_score']> 0.75,'signal']=-1

#Entry & Exit responses on Signals
capital=1000
position=0
entry_price=0
trades=[]

for i in range(len(data)):
    price=data['Close'].iloc[i]
    signal=data['signal'].iloc[i]

    if signal == 1 and position == 0 :
      position=capital/price
      entry_price=price
      capital =0
    elif signal==-1 and position>0:
      capital=position*price
      profit=capital-(position*entry_price)
      trades.append(profit)
      position=0
    if position>0:
      capital=position*data['Close'].iloc[-1]
      profit=capital-(position*entry_price)
      trades.append(profit)
    total_return=((capital-10000)/10000)*100 
    wins=[t for t in trades if t>0]
    win_rate= (len(wins)/len(trades))*100 if trades else 0
    avg_profit=np.mean(trades) if trades else 0

#Strategy Performance Metrics
print("\nFinal Capital", capital)
print("Trades",trades)
print(f"Total return (%):{total_return}")
print(f"Number of trades:{len(trades)}")
print(f"Win Rate (%): {win_rate}")
print(f"Average Profit:{avg_profit}")



# In[ ]:




