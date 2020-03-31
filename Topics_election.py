import pandas as pd
from nltk.tag import pos_tag

class pronoun_topicmodelling_hindi:
     def __init__(self,tweets):
        self.tweets = tweets
        
     def run(self):
         
        rawfile = pd.DataFrame()
        rawfile['tweet'] = self.tweets
        #rawfile['tweet'] = rawfile['tweet'].fillna("")
        rawfile['Subject'] = 'Blank'
        rawfile['Cleaned_Subject'] ='blank'
        
        
        for index,rows in rawfile.iterrows():
            sentence = rawfile.at[index,'tweet']
            tagged_sent = pos_tag(sentence.split())
            propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
            rawfile.at[index,'Subject'] = propernouns
                    #topics[i] = propernouns
                
            if(len(rawfile.at[index,'Subject'])==0):
                rawfile.at[index,'Subject'] = ['']
            else:  
                rawfile.at[index,'Subject'] = rawfile.at[index,'Subject']  
                clean_topic = []
                for topic in rawfile.at[index,'Subject']:
                    if str(topic).find("@") !=-1:
                        pass
                    elif str(topic).find("#") !=-1:
                        pass
                    else:
                        clean_topic.append(topic)

                rawfile.at[index,"Cleaned_Subject"] = clean_topic
                
                
        return rawfile['Cleaned_Subject']
            
        
        
