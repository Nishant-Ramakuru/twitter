# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 10:40:40 2019

@author: BB-8
"""

import os
import pandas as pd
df_raw_topics = pd.DataFrame()
df_raw_HT = pd.DataFrame()
df_raw_UM = pd.DataFrame()
df_raw_raw = pd.DataFrame()
path = 'C:/Users/BB-8/Downloads/new keywords/twitter/merged/dd/'
for filename in os.listdir(path):
    try:
        print(filename)
        if "Topics" in filename:
            
            df = pd.read_excel(path + str(filename))
            #df.drop(['Profile_URL'],axis=1,inplace=True)
            #df['keyword'] = "colonies"
            df['keyword'] = str(filename.split("_")[0])
            df_raw_topics = pd.concat([df_raw_topics,df],axis = 0)
        elif "HT" in filename:
            
            df = pd.read_excel(path + str(filename))
            #df.drop(['Profile_URL'],axis=1,inplace=True)
            #df['keyword'] = "colonies"
            df['keyword'] = str(filename.split("_")[0])
            df_raw_HT = pd.concat([df_raw_HT,df],axis = 0)
        elif "UM" in filename:
            
            df = pd.read_excel(path + str(filename))
            #df.drop(['Profile_URL'],axis=1,inplace=True)
            #df['keyword'] = "colonies"
            df['keyword'] = str(filename.split("_")[0])
            df_raw_UM = pd.concat([df_raw_UM,df],axis = 0)
        elif "raw" in filename:
            
            df = pd.read_excel(path + str(filename))
            #df.drop(['Profile_URL'],axis=1,inplace=True)
            #df['keyword'] = "colonies"
            df['keyword'] = str(filename.split("_")[0])
            df_raw_raw = pd.concat([df_raw_raw,df],axis = 0)
            
        else:
            pass
            
    except:
        print("couldn't merger - "+str(filename))
print("done merging")
df_raw_topics.to_excel("C:/Users/BB-8/Downloads/merged_topcis.xlsx")
df_raw_HT.to_excel("C:/Users/BB-8/Downloads/merged_HT.xlsx")
df_raw_UM.to_excel("C:/Users/BB-8/Downloads/merged_UM.xlsx")
df_raw_raw.to_excel("C:/Users/BB-8/Downloads/merged_raw.xlsx")

