import pandas as pd
#from topic_modeling import cleaning

df = pd.read_excel('Hashtag_Topics_new.xlsx')

df.reset_index(inplace=True)

df.shape
#object_topic = cleaning(df1['tweet'],int(len(df)/1000),"")
#object_topic.run()
topics = list(set(list(pd.read_csv("Topics_LDA_hashtags.csv").topics)))


df_topics = pd.DataFrame(columns = topics)
df_topics['tweet'] = df['tweet']
for index,row in df.iterrows():
    for element in df_topics.columns:
        if str(element).lower() in str(df_topics.tweet[index]).lower():
            print(element)
            df_topics.at[index,str(element)] = 1
            break
#df_topics.drop(topics,axis=1,inplace=True)
df_topics.reset_index(inplace=True)
Topic = []
for index,row in df_topics.iterrows():
    tweet_topic = []
    #print(index,row)
    for topic in df_topics.columns:
        if df_topics.at[index,str(topic)] == 1.0:
                tweet_topic.append(topic)
    Topic.append(tweet_topic)
df_topics['Topics'] = Topic    
df_topics.to_excel("topic_final.xlsx")