from __future__ import unicode_literals
import tweepy #https://github.com/tweepy/tweepy
import pandas as pd
import datetime

from Topics_election import pronoun_topicmodelling_hindi
from googletrans import Translator
import emoji
from nltk.sentiment import vader
sia= vader.SentimentIntensityAnalyzer()
from Topics_LDA import lda_topicmodelling


"""retrieves approximately 3000 tweets for each twitter handle"""
"""gets all the attributes as mentioned in the social media analytics folder for each tweet"""

class Twitter_handles(object):
    
    def __init__(self,screen_name,consumer_key,consumer_secret,access_key,access_secret):
        #Twitter API credentials
        self.consumer_key=consumer_key
        self.consumer_secret=consumer_secret    
        self.access_key=access_key
        self.access_secret=access_secret
        self.screen_name = screen_name

    def run(self):
        #Twitter only allows access to a users most recent 3240 tweets with this method

        #authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        api = tweepy.API(auth)

        #initialize a list to hold all the tweepy Tweets
        alltweets = []  

        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name = self.screen_name,count=200)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            print("getting tweets before %s" % (oldest))

            #all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name = self.screen_name,count=200,max_id=oldest)

            #save most recent tweets
            alltweets.extend(new_tweets)

            #upDate the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1

            print ("...%s tweets downloaded so far" % (len(alltweets)))

        simple_list=[]
        
        def Dateformat(temp):
            return(str(temp.day)+ "-" +str(temp.month)+ "-" +str(temp.year) + " " +str(temp.hour)+ ":" +str( temp.minute)+ ":" +str(temp.second))
        
        
        
        for status in alltweets:
            array = [status._json["id"],status.created_at,status._json["text"].strip(),status._json["lang"],
                     status.user._json["id_str"], status.user._json["friends_count"],
                     status._json["favorited"],status._json["retweeted"],
                     status.user._json['description'], status.user._json["time_zone"],
                     status._json["place"],status._json["in_reply_to_screen_name"],
                     status._json["in_reply_to_status_id"],status._json["in_reply_to_user_id"],
                     status._json["is_quote_status"],
                     status._json["favorite_count"], status._json["retweet_count"],
                     status.user._json["screen_name"],status.user._json["name"],
                     status.user._json["location"],status.user._json["verified"],
                     status.user._json["followers_count"],
                     status._json["source"],status.user._json["statuses_count"],
                     status.user._json["geo_enabled"],
                     status.user._json["profile_image_url"],
                     [h["text"] for h in status._json["entities"]["hashtags"]],
                     [h["name"] for h in status._json["entities"]['user_mentions']]]
            simple_list.append(array)
        
        df = pd.DataFrame(simple_list)
        df.columns = ['id', 'Date','tweet','language','user_id',
                      'friends','favorited_status','retweet_status',
                      'description','time_zone','place','in_reply_to_screenname',
                      'in_reply_to_status_id','in_reply_to_userid',
                      'is_quote_status','favorite_count','retweet_count',
                      'user_screen_name','user_name','user_location','Verified','followers','Sources','status_count',
                      'geo_enabled','Profile_URL',
                      'Hashtags',"User_Mentions"]
        ###############################################################################
        
        
        
        final_compound_score = []
        final_sentiment = []
        comment = []
        translator = Translator()
        converted = []
        compound_vernacular=[]
        senti_vernacular=[] 
        translation_flag = []
        impression=[]
        df['shifted_date'] = pd.to_datetime(df['Date'])
        df['RT Flag'] = 'Blank'
        
        
        for index,row in df.iterrows():
            final_compound_score.append(sia.polarity_scores(df.at[index,'tweet'])["compound"])
            if final_compound_score[len(final_compound_score)-1]>0:
                final_sentiment.append('positive')
            elif final_compound_score[len(final_compound_score)-1]==0:
                final_sentiment.append('neutral')
            else:
                final_sentiment.append('negative')
            
            if "RT @" in row["tweet"]:
                df.at[index, "RT Flag"]= "Retweet"
                df.at[index, "Engagements"]= 0
            elif "@" in row["tweet"]:
                df.at[index, "RT Flag"]= "Reply"
                df.at[index, "Engagements"]= (row["favorite_count"] + row["retweet_count"])
            else:
                df.at[index, "RT Flag"]= "Original"
                df.at[index, "Engagements"]= (row["favorite_count"] + row["retweet_count"])                
            
            if df.at[index,'is_quote_status'] == False:
                comment.append("No")
            else:
                comment.append("Yes")
            
            if df.at[index,'language'] != 'en':
                try:
                    inpt = emoji.demojize(df.at[index,'tweet'])
                    converted.append(translator.translate(inpt).text)
                    translation_flag.append('Successful')
                except:
                    converted.append(df.at[index,'tweet'])
                    translation_flag.append('Failed')
            else:
                converted.append(df.at[index,'tweet'])
                translation_flag.append('NA')
            
            compound_vernacular.append(sia.polarity_scores(df.at[index,'tweet'])["compound"])
            if compound_vernacular[len(compound_vernacular)-1]>0:
                senti_vernacular.append('positive')
            elif compound_vernacular[len(compound_vernacular)-1]==0:
                senti_vernacular.append('neutral')
            else:
                senti_vernacular.append('negative')
            
            #df.at[index,'shifted_Date'] = df.at[index,'Date'].strftime('%d-%m-%y %H:%M:%S')
            
            df.at[index,'shifted_date'] = pd.to_datetime(df['Date'][index]).strftime('%d-%m-%y %H:%M:%S')
            df.at[index,'shifted_date'] = pd.to_datetime(df['shifted_date'][index]- datetime.timedelta(hours=7)).strftime('%d-%m-%y %H:%M:%S')
            
            
            
            impression.append(int(0.1*(int(df.at[index,'followers']))))
            
        
        df['Sentiment'] = final_sentiment
        df['Compound_score'] = final_compound_score
        df['Translated_tweet'] = converted
        df['Comment'] = comment
        
        df['Sentiment_vernacular'] = senti_vernacular
        df['Compound_vernacualar'] = compound_vernacular
        
        df['Issue'] = str(self.screen_name)  #Defining the ISSUEs column as the search term itself
        df['Influencers'] = df['tweet'].str.extract("RT\s+(\@[^\:]*)", expand=False).fillna('Original')
        df['Impressions'] = impression
        df['translation_flag'] = translation_flag
        topic_object = pronoun_topicmodelling_hindi(df['tweet'])
        topics = topic_object.run()
        df['Topics'] = topics
        
        columns = ['id','Date','shifted_date','tweet','RT Flag','language','user_id',
                      'friends','favorited_status','retweet_status',
                      'description','time_zone','place','in_reply_to_screenname',
                      'in_reply_to_status_id','in_reply_to_userid',
                      'is_quote_status','favorite_count','retweet_count',
                      'user_screen_name','user_name','user_location','Verified','followers','Sources','status_count',
                      'geo_enabled','Profile_URL','Hashtags','User_Mentions','Sentiment','Compound_score','Issue',
                      'Influencers','Impressions']
        #df = df[columns]
        
      
        #sdf['Date'] = pd.to_Datetime(df['Date'])
        
        
        df.reset_index(inplace=True)
        df.to_excel(str(self.screen_name)+"_handle_raw.xlsx")
        print("Raw Data Fetching Done into excel !!!")  
        
        df['Hashtags'] = df['Hashtags'].astype(str).str.strip("[u']")
        df['Hashtags'] = df['Hashtags'].str.strip("'")
        df1 = df.drop('Hashtags', axis=1).join(df.Hashtags.str.split(expand=True)
                            .stack().reset_index(drop=True, level=1).rename('Hashtags'))
                
        df1['Hashtags'] =df1['Hashtags'].astype(str).str.strip("u'  ',")
        if str(df1['Hashtags'].astype(str)).find("nan") ==-1:    
            df1['Hashtags'] ="#"+ df1['Hashtags'].astype(str)
                
        df1.to_excel(str(self.screen_name)+"_handle_HT.xlsx", header= True,index=False)
        print("HT Data Done into excel !!!")  
        
        
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
                
        df1.to_excel(str(self.screen_name)+"_handle_UM.xlsx", header= True,index=False)   
        
        print("UM Data Done into excel !!!")  
        
        df3 = df
        df3['Topics'] = df.Topics.apply(pd.Series) \
                     .merge(df, right_index = True, left_index = True) \
                     .drop(["Topics"], axis = 1)
        
        df3.to_excel(str(self.screen_name)+"Topics.xlsx")
        print("Raw Data Done into excel !!!")  
        
        '''
        lda_topic_object = lda_topicmodelling(df[df['language']=='en'],10,5)
        lda_topics = lda_topic_object.run()
        lda_df = pd.DataFrame()
        lda_df['Topics'] = lda_topics 
        
        lda_df.to_excel(str(self.screen_name)+"_LDA_Topics")
        '''