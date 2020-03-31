consumer_key='tpAestpXtM2pYAlomfZr6LN7d'
consumer_secret='MCQ1aVPypaBOZIlg7MDp36znULAIcmf9Cj8xfxodyVyLpILpQu'
access_key='124163864-koQiHbqAF1QvLUzGqMb2ITvWk60jaa5yOsgJeaT7'
access_secret='qdMSjnab0O49k1pnck0fgtVQre60VN7pb0qkSC2vSYwJE'

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream  

string = input("Enter channel name: ")
#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    #start = 0
    #maxi = 10
    def on_data(self, data):
        try:
            #print(data)
            print('fetching data')
            with open(string+'TwitterAPIfunctinon.txt','a') as f:
                f.write(data)
            #if self.start > self.maxi:
                #stream.disconnect()
            #self.start = self.start + 1
        except:
            pass
        

    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    stream = Stream(auth, l)
    #This line filter tweets from the words.
    stream.filter(track=['bjp'])