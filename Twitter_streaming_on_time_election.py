#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import re
import json
import pandas as pd
from nltk.sentiment import vader
sia= vader.SentimentIntensityAnalyzer()  
from datetime import datetime
from Topics_election import pronoun_topicmodelling_hindi
from googletrans import Translator
import emoji



class streaming_api_time(object):
    def __init__(self,till_datetime,string,consumer_key,consumer_secret,access_key,access_secret):
        #self.sec = sec
        self.till_datetime = datetime.strptime(str(till_datetime), '%b %d %Y %I:%M%p')
        self.string = string
        self.consumer_key=consumer_key
        self.consumer_secret=consumer_secret
        self.access_key=access_key
        self.access_secret=access_secret
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        
        #This is a basic listener that just prints received tweets to stdout.
        class StdOutListener(StreamListener):
            #change the value of limit based on the the time limit = 60 means it will stream till 60 secs from the now
            
            def on_data(self, data):
                try:
                    #print(data)
                    print("Fetching Data")
                    with open(self.string+'_TwitterAPItime.txt','a') as f:
                        f.write(data)
                    print("done")
                    #if datetime.now()> self.till_datetime:
                        #print("--------------------")
                        #stream.disconnect()
                except:
                    pass
        
            def on_error(self, status):
                print(status)
        l = StdOutListener()
        stream = Stream(auth, l)
        stream.filter(track=[self.string])
    
    
    def run(self):    
        
            def convert_df(tweets):
                
                
                df = pd.DataFrame.from_dict(tweets)
            
                df['user_id'] = df['id_str']
                df['Date']  = df['created_at'].apply(lambda x: datetime.strptime(x, '%a %b %d %H:%M:%S +0000 %Y'))
                
                #Calculating useful variables
                screen_name = []
                description = []
                verified = []
                followers_count = []
                place = []
                hashtag = []
                usermention = []
                geo_enabled = []
                friends_count = []
                for i in range(len(df)):
                    screen_name.append(df['user'][i]['screen_name'])
                    description.append(df['user'][i]['description'])
                    verified.append(df['user'][i]['verified'])
                    followers_count.append(df['user'][i]['followers_count'])
                    geo_enabled.append(df['user'][i]['geo_enabled'])
                    friends_count.append(df['user'][i]['friends_count'])
                    if df['place'][i] != None:
                        place.append(df['place'][i]['name'])
                    else:
                        place.append("NA")
                        
                    y0 = []
                    for j in range(len(df['entities'][i]['hashtags'])):
                         y0.append( df['entities'][i]['hashtags'][j]['text'])
                    hashtag.append(y0)
                    y1 = []
                    for j in range(len(df['entities'][i]['user_mentions'])):
                         y1.append( df['entities'][i]['user_mentions'][j]['screen_name'])
                    usermention.append(y1)
                    
                
                
                df['user_name'] = screen_name
                df['description'] = description
                df['users_verified'] = verified
                df['followers_count'] = followers_count
                df['place'] = place
                df['Hashtags'] = hashtag
                df['User_Mentions'] = usermention  
                df['geo_enabled'] = geo_enabled
                df['friends_count'] = friends_count    
                   
                
                #Calculating Compound score and Sentiments using vader lib
                twees = df['text']
                compound=[]
                senti=[]  
                for twee in twees:               
                    compound.append(sia.polarity_scores(twee)["compound"])
                
                    if compound[len(compound)-1]>0:
                        senti.append('positive')
                    elif compound[len(compound)-1]==0:
                        senti.append('neutral')
                    else:
                        senti.append('negative')
                
                df['Sentiment'] = senti
                df['Compound_score'] = compound
                
                
                #Calculating RT Flag which contains if the tweet is Retweeted or Replied or Original
                
                for index,row in df.iterrows():
                    if "RT @" in row["text"]:
                        df.at[index, "RT Flag"]= "Retweet"
                        df.at[index, "Engagements"]= 0
                    elif "@" in row["text"]:
                        df.at[index, "RT Flag"]= "Reply"
                        df.at[index, "Engagements"]= (row["favorite_count"] + row["retweet_count"])
                    else:
                        df.at[index, "RT Flag"]= "Original"
                        df.at[index, "Engagements"]= (row["favorite_count"] + row["retweet_count"])                
                        
                df['Influencers'] = df['text'].str.extract("RT\s+(\@[^\:]*)", expand=False).fillna('Original')
                        
                # Calculating impression (10% of no of followers)           
                impression=[]
                for index,row in df.iterrows():
                    impression.append(int(0.1*(int(df['followers_count'][index]))))
                
                df['Impressions'] = impression
                
                # Calculating Reach and Engagements     
                for index,row in df.iterrows():
                        
                    if "RT @" in row["text"]:
                        df.at[index, "Reach"]= 0
                    else:
                        df.at[index, "Reach"]= (row["Engagements"]+ int(df["Impressions"][index]))
                
                
                
                #Deleting extra columns
                del_cols =['contributors','coordinates','entities',
                         'filter_level','user','retweeted_status','id_str',
                         'quote_count','created_at']
                
                df = df.drop(del_cols, axis = 1)
                
                try:
                   df.drop(['extended_entities','possibly_sensitive','extended_tweet','display_text_range','quoted_status',
                            'quoted_status_id','quoted_status_id_str','quoted_status_permalink'],axis = 1,inplace = True)
                except:
                    pass
                
                comment = []
                for i in range(len(df)):
                    if df['RT Flag'][i] == "Original":
                       if df['text'][i].find("https://t.co/") !=-1:
                           comment.append("Yes")
                       else:
                           comment.append("No")
                    else:
                       comment.append("No")
                        
                df['Comment'] = comment
            
                for i in range(len(df)):
                    if(df['Comment'][i]=="Yes"):
                        df['RT Flag'][i] = 'Retweet'
            
                df['Date'] = pd.to_datetime(df['Date'])  
                 
                #filter date here
                '''
                mask = (df['Date'] > '1-1-2019 14:9:29') & (df['Date'] <= '1-5-2019 14:9:29')
                df = df.loc[mask]
                '''
                #extracting subjects
                topic_object = pronoun_topicmodelling_hindi(df['text'])
                topics = topic_object.run()
                
                df['Topics'] = topics
                
                # Sentiment Calculation (for hindi and english tweets)
                translator = Translator()
                converted = []
                failed = []
                for i in range(len(df)):
                  if df['Language'][i]=='hi':
                    try:
                      inpt = emoji.demojize(df['text'][i])
                      converted.append(translator.translate(inpt).text)
                    except:
                      converted.append('failed')
                      failed.append(df['text'][i])
                  else:
                    converted.append(df['text'][i])
                    
                df['Translated_text'] = converted
                
                compound_vernacular=[]
                senti_vernacular=[]  
                for tweet in df['Translated_text']:               
                    compound_vernacular.append(sia.polarity_scores(tweet)["compound"])
                    if compound_vernacular[len(compound_vernacular)-1]>0:
                        senti_vernacular.append('positive')
                    elif compound_vernacular[len(compound_vernacular)-1]==0:
                        senti_vernacular.append('neutral')
                    else:
                        senti_vernacular.append('negative')
                df['Sentiment_vernacular'] = senti_vernacular
                df['Compound_vernacualar'] = compound_vernacular
        
                
                #writing to csv file
                df.to_csv("Streaming_"+self.string+"_raw.csv", header= True,index=False)
                
                # Spliting every element of the hashtags lists        
                df['Hashtags'] = df['Hashtags'].astype(str).str.strip("[u']")
                df['Hashtags'] = df['Hashtags'].str.strip("'")
                df1 = df.drop('Hashtags', axis=1).join(df.Hashtags.str.split(expand=True)
                                    .stack().reset_index(drop=True, level=1).rename('Hashtags'))        
                df1['Hashtags'] =df1['Hashtags'].astype(str).str.strip("u'  ',")
                df1['Hashtags'] = "#"+df1['Hashtags']
                df1['Hashtags'] = df1['Hashtags'].str.replace('#nan','')   
                df1['User_Mentions'] = df.drop('User_Mentions', axis = 1)   
                   
                # writing it to csv file       
                df1.to_csv("Streaming_"+self.string+"_HT_on_time.csv", header= True,index=False)
                 
                # Spliting every element of the UserMentions lists        
                df['User_Mentions'] = df['User_Mentions'].astype(str).str.strip("[u']")
                df2 = df.drop('User_Mentions', axis=1).join(df.User_Mentions.str.split(expand=True)
                                     .stack().reset_index(drop=True, level=1).rename('User_Mentions'))
                df2['User_Mentions'] = df2['User_Mentions'].astype(str).str.strip("u'  ',")
                        
                df2['User_Mentions'] = "@"+df2['User_Mentions']       
                df2['User_Mentions'] = df2['User_Mentions'].str.replace('@nan','')
                df2['User_Mentions'] = df2['User_Mentions'].str.replace('@htTweets','')
                
                df1['Hashtags'] = df.drop('Hashtags', axis = 1)
                
                # writing it to csv file  
                df2.to_csv("Streaming_"+self.string+"_UM_on_time.csv", header= True,index=False)
            
    
            tweets_data_path = 'TwitterAPItime.txt'
            tweets_data = []
            tweets_file = open(tweets_data_path, "r")
            for line in tweets_file:
                try:
                    tweet = json.loads(line)
                    tweets_data.append(tweet)
                except:
                    continue
            convert_df(tweets_data)        
      
       
            
                             
                             
                             