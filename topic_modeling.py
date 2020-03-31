from nltk.corpus import stopwords
from nltk import FreqDist
import re
from nltk.tokenize import word_tokenize 
import pandas as pd
from gensim import corpora
import pickle
import gensim
import spacy
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import random
from spacy.lang.en import English
import string
en_stop = set(nltk.corpus.stopwords.words('english'))
parser= English()

from nltk.sentiment import vader
sia= vader.SentimentIntensityAnalyzer()


"""This class computes topics for given text arrays for individual platforms for ex. an array of tweets should be passed which will be cleaned 
   and topics will be computed by dividing the array into chunks for a more concentrated window span of text array passed""" 
    
class cleaning:
    def __init__(self,dataframe_array,no_of_chunks,key_word):
        self.dataframe_array = dataframe_array
        self.no_of_chunks = no_of_chunks
        self.key_word = key_word
    
    def run(self):
        
        def text_clean(dataframe_array,key_word):
            """To remove all special characters and convert the text to lower case"""
            bag = ""
            print("cleaning data")
            
            a = []
            for i in range(len(dataframe_array)):
                s = (str((dataframe_array[i])).lower())
                s = re.sub('[^ a-zA-Z0-9]', '', s)  
                s = str(s).replace(key_word,"")
                a.append(s)
                
            print("text cleaned")
            return a

        c = text_clean(self.dataframe_array,self.key_word)

        
        
        def chunk(dataframe_array, no_of_chunks):
            
            print("creating chunks")
            avg = len(dataframe_array) / float(no_of_chunks)
            chunk_array = []
            last = 0.0

            while last < len(dataframe_array):
                chunk_array.append(dataframe_array[int(last):int(last + avg)])
                last += avg
            print("chunks created")    
            return chunk_array

        c_a = chunk(c,self.no_of_chunks)
        
        def tokenize(text):
            lda_tokens = []
            tokens = parser(text)
            for token in tokens:
                lda_tokens.append(token.lower_)
            return lda_tokens

        def get_lemma(word):
            lemma = wn.morphy(word)
            if lemma is None:
                return word
            else:
                return lemma

        def get_lemma2(word):
            return WordNetLemmatizer().lemmatize(word)

        def prepare_text_for_lda(text):
            tokens = tokenize(text)
            tokens = [token for token in tokens if len(token) > 4]
            tokens = [token for token in tokens if token not in en_stop]
            tokens = [get_lemma(token) for token in tokens]
            return tokens
        
        def topics(df_array,i):
            
            parser = English()
            print("Initialized")
            text_data =[]

            for line in df_array:
                tokens = prepare_text_for_lda(line)
                text_data.append(tokens)

            print("words tokenized")

            dictionary = corpora.Dictionary(text_data)
            corpus = [dictionary.doc2bow(text) for text in text_data]

            pickle.dump(corpus, open('corpus.pkl', 'wb'))
            dictionary.save('dictionary.gensim')
            
            NUM_TOPICS = 1
            ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
            
            ldamodel.save('model5.gensim')
            topics = ldamodel.print_topics(num_words=1)
            Topic = []
            compound_avg = []
            senti = []
            
            for topic in topics:
                t = ''.join([x for x in str(topic) if x in string.ascii_letters + '\'- '])
                t = t.replace('"','')
                t = t.replace("'","")
                t = t.split(" ")
                to = t
                #to = [t[1],t[3],t[5],t[7]]
                
                compound = []
                for d in (df_array):
                    
                    if any(x in d for x in to):
                        
                        compound.append(sia.polarity_scores(d)["compound"])
                    
                compound_avg.append(sum(compound)/len(compound))
                if compound_avg[len(compound_avg)-1]>0:
                    senti.append('positive')
                elif compound_avg[len(compound_avg)-1]==0:
                    senti.append('neutral')
                else:
                    senti.append('negative')   
                    
                to = str(to).replace('",',"")
                to = str(to).replace("'","")
                to = str(to).replace(",","")
                to = str(to).replace(" ","")
                
                
                
                Topic.append(to)
            dict_topic = {"Topics":Topic,
                          "Compound":compound_avg,
                          "sentiment":senti
                          }
            
            df = pd.DataFrame.from_dict(dict_topic)
            return df
            #df.to_csv("Topics "+str(i)+".csv")

        df_final = pd.DataFrame()  
        print("computing topics")
        for i,a in enumerate(c_a):
            print(i)
            df = topics(a,i)
            df_final = pd.concat([df_final,df])
        freq=[]
        for topi in df_final['Topics']:
            topi = str(topi).replace("[","")
            topi = str(topi).replace("]","")
            
            cou = 1
            for i in range(len(self.dataframe_array)):    
                if str(self.dataframe_array[i]).find(str(topi)) !=-1:
                    cou = cou+1
                else:
                    pass
                
            freq.append(cou)  
           
        df_final["frequency"] = freq
        
        df_final.to_csv("search-"+self.key_word+"-topic.csv")
            
        
        

