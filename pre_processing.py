# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 13:14:09 2019

@author: BB-8
"""

import pandas as pd
df1 = pd.read_excel("nishantTopics.xlsx")
df= pd.read_excel("modi_raw.xlsx")
import datetime
#-----------------------------------------pie----------------------------------

RT_flag_dict = df.groupby("RT Flag").count()['id'].to_dict()

RT_flag_json = [['type','count']]

RT_flag_json.append([list(RT_flag_dict.keys())[0],list(RT_flag_dict.values())[0]])
RT_flag_json.append([list(RT_flag_dict.keys())[1],list(RT_flag_dict.values())[1]])
RT_flag_json.append([list(RT_flag_dict.keys())[2],list(RT_flag_dict.values())[2]])

RT_flag_json

import json
with open('RT_pie_chart.json', 'w') as outfile:
    json.dump(RT_flag_json, outfile)
    
from datetime import datetime
#-----------------------------------------sentiment timeline----------------------------------
compound_score = df['Compound_score']
date_timeline = df['shifted_date']

sentiment_list_json= list(map(lambda X: ([int(x) for x in datetime.strptime(str(X[0]), '%Y-%m-%d %H:%M:%S').strftime("%Y,%m,%d,%H,%M,%S").split(",")],X[1]), list(zip(date_timeline,compound_score))))

with open('sentiment_corrected_timeline_chart.json', 'w') as outfile:
    json.dump(sentiment_list_json, outfile)
-----------------------------------------engagements timeline----------------------------------
engagements = df['Engagements']
date_timeline = df['shifted_date']

engagement_list_json= list(map(lambda X: ([int(x) for x in datetime.strptime(str(X[0]), '%Y-%m-%d %H:%M:%S').strftime("%Y,%m,%d,%H,%M,%S").split(",")],X[1]), list(zip(date_timeline,engagements))))

with open('engagement_timeline_chart.json', 'w') as outfile:
    json.dump(engagement_list_json, outfile)
-----------------------------------------tweet timeline----------------------------------

df.groupby("shifted_date").count()['shifted_date'].date







Sentiment_flag_dict = df.groupby("Sentiment").count()['id'].to_dict()

Sentiment_flag_json = [['type','count']]

Sentiment_flag_json.append([list(Sentiment_flag_dict.keys())[0],list(Sentiment_flag_dict.values())[0]])
Sentiment_flag_json.append([list(Sentiment_flag_dict.keys())[1],list(Sentiment_flag_dict.values())[1]])
Sentiment_flag_json.append([list(Sentiment_flag_dict.keys())[2],list(Sentiment_flag_dict.values())[2]])

with open('Sentiment_pie_chart.json', 'w') as outfile:
    json.dump(Sentiment_flag_json, outfile)
    
#-----------------------------------------------------------------------------------------------
Influencer_by_count = df.groupby('Influencers').count()['id'].to_dict()

Influencer_by_count_json = list(map(lambda X: (X[0],X[1]), list(zip(Influencer_by_count.keys(),Influencer_by_count.values()))))



with open('Influencer_by_count_wc.json', 'w') as outfile:
    json.dump(Influencer_by_count_json, outfile)
    
#------------------------------------------------topical word cloud

Topic_by_count = df1.groupby('Topics').count()['id'].to_dict()
if "blank" in Topic_by_count:
    del Topic_by_count["blank"]
Topic_by_count_json = list(map(lambda X: (X[0],X[1]), list(zip(Topic_by_count.keys(),Topic_by_count.values()))))



with open('Topic_by_count_wc.json', 'w') as outfile:
    json.dump(TOpicz_by_count_json, outfile)
#-----------------------------------------------------hashtag word cloud
hashtag_by_count = df1.groupby('Hashtags').count()['id'].to_dict()
hashtag_by_count_json = list(map(lambda X: (X[0],X[1]), list(zip(hashtag_by_count.keys(),hashtag_by_count.values()))))

with open('hashtag_by_count_wc.json', 'w') as outfile:
    json.dump(hashtag_by_count_json, outfile)

#---------------------------------------------------metircs
list_metrics = [int(df.Engagements.sum()),
                int(df.Reach.sum()),
                int(len(set(df.user_name))),
                float(df.shape[0]/len(set(df.user_name))),
                int(df.followers.sum()/len(set(df.user_name))),
                int(df['RT Flag'].value_counts()['Original']),
                int(len(set(df[df['RT Flag'] == "Original"]['user_name']))),
                float(df['RT Flag'].value_counts()['Original']/len(set(df.user_name)))]
dict_metrics


import json
with open('list_metrics.json', 'w') as fp:
    json.dump(list_metrics, fp)
