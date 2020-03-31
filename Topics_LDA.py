import nltk
nltk.download('stopwords')

import sys
sys.setrecursionlimit(10000)
import re
import numpy as np
import pandas as pd
from pprint import pprint

#gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

#spacy for lemmatization
import spacy
#plotting tools
import pyLDAvis
import pyLDAvis.gensim 
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter("ignore",DeprecationWarning)


#load the LDA model from sk-learn
from sklearn.decomposition import LatentDirichletAllocation as LDA

#enable logging for gensim - optional
import logging
logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s',level = logging.ERROR)

import warnings
warnings.filterwarnings("ignore",category = DeprecationWarning)

#load the library with the CountVectorizer method
from sklearn.feature_extraction.text import CountVectorizer
import seaborn as sns
sns.set_style('whitegrid')
#%matplotlib inline

#nltk stopwrods
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['from','subject','re','edu','use'])

import os

#os.chdir(r"Z:\Data Science\Internship\Opin8")

class lda_topicmodelling(object):
    
    def __init__(self,dataframe,number_of_topics,number_of_words):
        self.dataframe = dataframe
        self.number_of_topics = number_of_topics
        self.number_of_words = number_of_words
    
    def run(self):
        data_text = pd.DataFrame()
        data_text['text'] = self.dataframe['headline']
        data_text['index'] = data_text.index
        documents = data_text
        
        #documents.head()
        #data_text['text'].head()
       
        
        #remove the punctuation
        '''
        documents['text'] = re.sub("[^a-zA-Z]",  # Search for all non-letters
                                  " ",          # Replace all non-letters with spaces
                                  str(documents['text']))
        '''
        
        documents['text'] = documents['text'].str.replace('[^\w\s]','')
        
        
        #convert the titles to lowercase
        documents['text'] = documents['text'].str.lower()        
            
        #Remove words which does not make sense to your analysis and add accordingly 
        delwords = ['rt','day','video','left','logo','co','https']
        documents['text'] = documents['text'].replace(to_replace=delwords, value="",regex=True)
        
        #import the wordcloud library
        from wordcloud import WordCloud
        
        #create a wordcloud object
        wordcloud = WordCloud(background_color = "white",
                              max_words = 1000, contour_width = 3,
                              contour_color = 'steelblue'
                              ).generate(' '.join(map(str,documents['text'])))
        
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig("WordCloud.png", format="png")
        
        print("-- A wordcloud image WordCloud.png is saved at the path")

        
        #helper function
        def plot_10_most_common_words(count_data, count_vectorizer):
            import matplotlib.pyplot as plt
            words = count_vectorizer.get_feature_names()
            total_counts = np.zeros(len(words))
            for t in count_data:
                total_counts+=t.toarray()[0]
            
            count_dict = (zip(words, total_counts))
            count_dict = sorted(count_dict, key=lambda x:x[1], reverse=True)[0:10]
            words = [w[0] for w in count_dict]
            counts = [w[1] for w in count_dict]
            x_pos = np.arange(len(words)) 
            
            plt.figure(2, figsize=(15, 15/1.6180))
            plt.subplot(title='10 most common words')
            sns.set_context("notebook", font_scale=1.25, rc={"lines.linewidth": 2.5})
            sns.barplot(x_pos, counts, palette='husl')
            plt.xticks(x_pos, words, rotation=90) 
            plt.xlabel('words')
            plt.ylabel('counts')
            plt.show()
            plt.savefig("top_10_most_common_words.png",format = "png")
            print("-- A plot of top 10 common words has been saved as top_10_most_common_words.png image file.")

            
        #intialize the count vectorizer eith the english stop words
        count_vectorizer = CountVectorizer(stop_words = 'english')
        
        #fit and transform the processed titles
        count_data = count_vectorizer.fit_transform(documents['text'])
        
        #visualize the 10 most common words
        #plot_10_most_common_words(count_data, count_vectorizer)
        
       # Helper function
        
        def print_topics(model, count_vectorizer, n_top_words):
            words = count_vectorizer.get_feature_names()
            topics = []
            
            for topic_idx, topic in enumerate(model.components_):
                print("\nTopic #%d:" % topic_idx)
                print(" ".join([words[i]
                                for i in topic.argsort()[:-n_top_words - 1:-1]]))
                topic = (" ".join([words[i]
                                for i in topic.argsort()[:-n_top_words - 1:-1]]))     
                topics.append(topic.split(" "))
            return topics
    # Tweak the two parameters below
        number_topics = self.number_of_topics
        number_words = self.number_of_words
        
        print("-- Wait!! till topics get generated and stored.")
        
        # Create and fit the LDA model
        lda = LDA(n_components=number_topics)
        lda.fit(count_data)
        
        
        # Print the topics found by the LDA model
        print("Topics found via LDA:")
        topics_df = pd.DataFrame()
        
        topics_df['topics'] = print_topics(lda, count_vectorizer, number_words)    
        topics_df.to_excel("Topics_LDA.xlsx")