# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 12:28:02 2019

@author: BB-8
"""
import pandas as pd
input_file = "search-cocacola-twitter_raw.xlsx"
df = pd.read_excel(input_file)
import datetime
for index,row in df.iterrows():
    #df['shifted_date'][index] =  pd.to_datetime(df['Date'][index]).strftime('%d-%m-%y %H:%M:%S')
    
    #df['shifted_date'][index] = pd.to_datetime(df['shifted_date'][index]- datetime.timedelta(hours=7)).strftime('%d-%m-%y %H:%M:%S')
    
    df.at[index,'shifted_date'] = pd.to_datetime(df['Date'][index]).strftime('%d-%m-%y %H:%M:%S')
    df.at[index,'shifted_date'] = pd.to_datetime(df['shifted_date'][index]- datetime.timedelta(hours=7))
            

df.to_excel(input_file)