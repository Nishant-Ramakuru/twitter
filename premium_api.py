
"""This api call is done over a loop and will retrieve data for 7 days for input given on key word search"""
"""raw file is created with all the attributes, for all the retrieved tweets based on the key word, mentioned in the doc in the social media analyitcs folder """
"""this code also creates two seperate file for Hashtags and usermentions with Retweet and Engagement flags"""
import pandas as pd
import datetime
from nltk.sentiment import vader
sia= vader.SentimentIntensityAnalyzer()  
import numpy as np
from googletrans import Translator
import emoji
from Topics_election import pronoun_topicmodelling_hindi
from searchtweets import ResultStream, gen_rule_payload, load_credentials,collect_results
premium_search_args = load_credentials("twitter_keys.yaml",
                       yaml_key="search_tweets_api",
                       #env_overwrite=False
                       )
    
from Topics_LDA import lda_topicmodelling



class twitter_api(object):
    
    def __init__(self,string):
        self.string = string
        

    def run(self):
    
        def tweets_to_data_frame(tweets):
            print("started parsing data")
            df = pd.DataFrame()
            df['id'] = np.array([tweet.id for tweet in tweets])
            df['Date'] = pd.to_datetime(np.array([tweet['created_at'] for tweet in tweets]))
            df['shifted_date']=None
            df['tweet'] = np.array([tweet['text'] for tweet in tweets])
            df['language'] = np.array([tweet['lang'] for tweet in tweets])
            df['user_id'] = np.array([tweet['id_str'] for tweet in tweets])
            df['friends'] = np.array([tweet['user']['friends_count'] for tweet in tweets])
            df['favorited_status'] = np.array([tweet['favorited'] for tweet in tweets])
            df['retweet_status'] = np.array([tweet['retweeted'] for tweet in tweets])
            df['description'] = np.array([tweet['user']['description'] for tweet in tweets])
            df['time_zone'] = np.array([tweet['user']['retweet_count'] for tweet in tweets])
            df['place'] = np.array([tweet['place'] for tweet in tweets])
            df['in_reply_to_screen_name'] = np.array([tweet['in_reply_to_screen_name'] for tweet in tweets])
            df['in_reply_to_status_id'] = np.array([tweet['in_reply_to_status_id'] for tweet in tweets])
            df['in_reply_to_user_id'] = np.array([tweet['in_reply_to_user_id'] for tweet in tweets])
            df['is_quote_status'] = np.array([tweet['is_quote_status'] for tweet in tweets])
            #df['label'] = None
            df['favorite_count'] = np.array([tweet['favorite_count'] for tweet in tweets])
            df['retweet_count'] = np.array([tweet['retweet_count'] for tweet in tweets])
            df['user_screen_name'] = np.array([tweet['user']['screen_name'] for tweet in tweets])
            df['user_name'] = np.array([tweet['user']['name'] for tweet in tweets])
            df['user_location'] = np.array([tweet['user']['location'] for tweet in tweets])
            df['Verified'] = np.array([tweet['user']['verified'] for tweet in tweets])
            df['followers'] = np.array([tweet['user']['followers_count'] for tweet in tweets])
            df['source'] = np.array([tweet['source'] for tweet in tweets])
            df['status_count'] = np.array([tweet['statuses_count'] for tweet in tweets])
            df['geo_enabled'] = np.array([tweet['geo_enabled'] for tweet in tweets])
            df['Profile_URL'] = np.array([tweet['user']['profile_image_url'] for tweet in tweets])
            df['Hashtags'] = np.array([tweet['entities']['hashtags'] for tweet in tweets])
            df['User_Mentions'] = np.array([tweet['entities']['user_mentions'] for tweet in tweets])
           
            
            #df['retweeted_status'] = np.array([tweet['retweeted_status'] for tweet in tweets])
            #df['quoted_status_id'] = np.array([tweet['quoted_status_id'] for tweet in tweets])
            #df['quoted_status_id_str'] = np.array([tweet['quoted_status_id_str'] for tweet in tweets])
            #df['quoted_status'] = np.array([tweet['quoted_status'] for tweet in tweets])
            #df['quoted_status_permalink'] = np.array([tweet['quoted_status_permalink'] for tweet in tweets])
            #df['urls'] = np.array([tweet['entities']['urls'] for tweet in tweets])    
            #df['user'] = np.array([tweet['user'] for tweet in tweets])
        
            
            
            compound=[]
            senti=[] 
            comment = []
            translator = Translator()
            converted = []
            compound_vernacular=[]
            senti_vernacular=[]  
            hashtags = []
            usermentions = []
            translation_flag = []
            impression = []
            df['shifted_date'] = df['Date']
            
            for index,row in df.iterrows():
                hashtags.append([hashtag['tweet'] for hashtag in df['Hashtags'][index]])
                usermentions.append([hashtag['screen_name'] for hashtag in df['User_Mentions'][index]])
                
                compound.append(sia.polarity_scores(df['tweet'][index])["compound"])
                
                if compound[len(compound)-1]>0:
                    senti.append('positive')
                elif compound[len(compound)-1]==0:
                    senti.append('neutral')
                else:
                    senti.append('negative')
                
                if df['is_quote_status'][index] == False:
                    comment.append("No")
                else:
                    comment.append("Yes")
                '''
                if df['lang'][index] != 'en':
                    try:
                      inpt = emoji.demojize(df['tweet'][index])
                      converted.append(translator.translate(inpt).tweet)
                      translation_flag.append('Successful')
                    except:
                      converted.append(df['tweet'][index])
                      translation_flag.append('failed')
                else:
                    converted.append(df['tweet'][index])
                    translation_flag.append('NA')
    
                compound_vernacular.append(sia.polarity_scores(converted[-1])["compound"])
                if compound_vernacular[len(compound_vernacular)-1]>0:
                    senti_vernacular.append('positive')
                elif compound_vernacular[len(compound_vernacular)-1]==0:
                    senti_vernacular.append('neutral')
                else:
                    senti_vernacular.append('negative')
                '''
                if "RT @" in row["tweet"]:
                    df.at[index, "RT Flag"]= "Retweet"
                    df.at[index, "Engagements"]= 0
                elif "@" in row["tweet"]:
                    df.at[index, "RT Flag"]= "Reply"
                    df.at[index, "Engagements"]= (row["fav_count"] + row["retweet_count"])
                else:
                    df.at[index, "RT Flag"]= "Original"
                    df.at[index, "Engagements"]= (row["fav_count"] + row["retweet_count"])   
                
                df.at[index,'shifted_date'] = df.at[index,'shifted_date'] - datetime.timedelta(hours=7)

                impression.append(int(0.1*(int(df['followers'][index]))))
                
            df['sentiment'] = senti
            df['Compound_Score'] = compound
            df['Hashtags'] = hashtags    
            df['User_Mentions'] = usermentions
            df['Translated_tweet'] = converted
            df['Comment'] = comment
            df['Sentiment_vernacular'] = senti_vernacular
            df['Compound_vernacualar'] = compound_vernacular
            df['Issue'] = str(self.string)
            df['Influencers'] = df['tweet'].str.extract("RT\s+(\@[^\:]*)", expand=False).fillna('Original')
            
            df['Impressions'] = impression
            df['translation_flag'] = translation_flag
            '''
            topic_object = pronoun_topicmodelling_hindi(df['tweet'])
            topics = topic_object.run()
            df['Topics'] = topics
            '''
            df['Influencers'] = df['tweet'].str.extract("RT\s+(\@[^\:]*)", expand=False).fillna('Original')
            
            
            columns = ['id','Date','shifted_date','tweet','RT Flag','language','user_id',
                      'friends','favorited_status','retweet_status',
                      'description','time_zone','place','in_reply_to_screenname',
                      'in_reply_to_status_id','in_reply_to_userid',
                      'is_quote_status','favorite_count','retweet_count',
                      'user_screen_name','user_name','user_location','Verified','followers','Sources','status_count',
                      'geo_enabled','Profile_URL','Hashtags','User_Mentions','Sentiment','Compound_score',
                      'entities','translation_flag','Translated_tweet','Comment','Sentiment_vernacular',
                      'Compound_vernacualar','Issue',
                      'Influencers','Impressions']
            df = df[columns]
        
            
            df['len_tweet'] = np.array([len(tweet.tweet) for tweet in tweets])
            df['geo'] = np.array([tweet['geo'] for tweet in tweets])
            df['coordinates'] = np.array([tweet['coordinates'] for tweet in tweets])
            df['quote_count'] = np.array([tweet['quote_count'] for tweet in tweets])
            df['reply_count'] = np.array([tweet['reply_count'] for tweet in tweets])
            
            df.to_excel(str(self.string)+"_raw.xlsx")

            df['Hashtags'] = df['Hashtags'].astype(str).str.strip("[u']")
            df['Hashtags'] = df['Hashtags'].str.strip("'")
            df1 = df.drop('Hashtags', axis=1).join(df.Hashtags.str.split(expand=True)
                                .stack().reset_index(drop=True, level=1).rename('Hashtags'))
                    
            df1['Hashtags'] =df1['Hashtags'].astype(str).str.strip("u'  ',")
            if str(df1['Hashtags'].astype(str)).find("nan") ==-1:    
                df1['Hashtags'] ="#"+ df1['Hashtags'].astype(str)
                    
            df1.to_excel(str(self.string)+"_HT.xlsx", header= True,index=False)
            
            
            df.User_Mentions = df.User_Mentions.astype(str).str.replace(" ", "")
            df.User_Mentions = df.User_Mentions.astype(str).str.replace("[", "")
            df.User_Mentions = df.User_Mentions.astype(str).str.replace("]", "")
            df.User_Mentions = df.User_Mentions.astype(str).str.replace("'", "")
            df.User_Mentions = df.User_Mentions.astype(str).str.replace(".", "")
            df.User_Mentions = df.User_Mentions.astype(str).str.lower()
            
            
            df1 = df.drop('User_Mentions', axis=1).join(df.User_Mentions.str.split(",",expand=True)
                                 .stack().reset_index(drop=True, level=1).rename('User_Mentions'))
                    
            df1['User_Mentions'] = "@"+df1['User_Mentions']
            
            df1['User_Mentions'] = df1['User_Mentions'].str.replace('@nan','')
            df1['User_Mentions'] = df1['User_Mentions'].str.replace('@htTweets','')
                    
            df1.to_excel(str(self.string)+"_UM.xlsx", header= True,index=False)
            '''
            df3 = df
            df3['Topics'] = df.Topics.apply(pd.Series) \
                     .merge(df, right_index = True, left_index = True) \
                     .drop(["Topics"], axis = 1)
        
            df3.to_excel(str(self.string)+"Topics.xlsx")
            
            lda_topic_object = lda_topicmodelling(df[df['language']=='en'],10,5)
            lda_topics = lda_topic_object.run()
            lda_df = pd.DataFrame()
            lda_df['Topics'] = lda_topics 
            
            lda_df.to_excel(str(self.screen_name)+"_LDA_Topics")
            '''
            print("done writing to excel")            
            
            return df
            
        def createTestData(search_string):
            try:
                print('Start Fetching')
                #print(date,nextdate)
                rule = gen_rule_payload(search_string,
                                        from_date="2019-05-18",
                                        to_date="2019-05-20",
                                        
                                        results_per_call=500)
                
                alltweets = collect_results(rule,
                                         max_results=500,
                                         result_stream_args=premium_search_args)
                print("data fetched")
                
                return alltweets
                    
            except:
                print("error")
    

        tweets = createTestData(self.string)
        dataframe_tweets = tweets_to_data_frame(tweets)
        return dataframe_tweets