
from twitter_API_scrapper_election import twitter_api
from twitter_class import twitter_api
#from Twitter_streaming_on_time_election import streaming_api_time
from twitter_handles_api_election import Twitter_handles
#from premium_api import twitter_api
import pandas as pd
'''
consumer_key='hbwjipkBG7tP0ohtia7hCAQDB'
consumer_secret='0biMHiFkJNz5nFNVE13kcpoHjBW3qJ7F4pAxgh7wVKmHTqYAoh'
access_key='112166849-VsUzdcK2aQXPAd5VVg77q608ESOCx4R1QABitR6J'
access_secret='LaHCSMiMNsoP6BMjrNxUFXKH2Fn6KWmMTXCeYb21QQKh1'


consumer_key='V2qwIFQFkq29mlZdqfXqcwfdP'
consumer_secret='RggvK6C70YbveYdlpgogoVc7Okx6AkrdWtdguvWPvZ9CyY52ZF'
access_key='2252707229-f1mtDeug3TjvkAKA9PHqa7LW6lqdRqV12kGeid0'
access_secret='BALeMDezc3llku7YiAcHUOEudlWcJo4Kc8fJW4zYDjPM3'


consumer_key='oqyhKtrSrCyYfAjYdhLdNrEOh'
consumer_secret='8qHWSiLfV6vNot0gkltG2uGkJwJhExedmBVRKwAfXnSZOZSS4I'
access_key='796928120741761024-vG8nQrFyhzs28SchXZKD3Fh4XO1yQru'
access_secret='72siJ2y6SZWkUnA2OeRRWohxO3lbxTlEWFBZo7g3heSv7'



#akash

consumer_key='HK92sfktQdQONb2lh822rsL3g'
consumer_secret='l9ZIihb9ATXOm8B1RxoYCUgy4Su7ODXKVuSmOFOJrKLYC3aBb3'
access_key='626504527-7vQwkB06EF4EsZ9UnKAVTKULWYj6r0jDvvKBb0VS'
access_secret='R6HUQmqlKuX9yvi4HdZtzFC7eOn7VZUavgca6Re9y8hAb'

'''
#bramhesh
consumer_key='FEIq9oOX5gY2Uk80cLjCuaLTu'
consumer_secret='l5CVTE0fqsqIrN9e0yZXvNjUHKY5WGK8rbbqp4Iuy5HrjwF9RW'
access_key='370162760-57o86rED5Xh2u2TGRMGlD127fXHRrVQBFTRNmzPR'
access_secret='FFKt4z4dVpFJ50kiRMCZXOGCPakMuxGm4ks91VAQBF3wg'

'''
#shivam
consumer_key='A5g4VgiHFN5UfKM3ia0j44o7t'
consumer_secret='bdp8I7OiZhpMhvogDH70VbQC1RDILmjcHorE5VEYfVK93XxsgG'
access_key='1130070993953730561-ZgUX00Eb8TXsFetw9BzIcHnnrp0mCl'
access_secret='rtoJulbeRq5hZDU6iLXiPH30fR3smBfLVNnHJ3BURJbVw'
'''
	


keyword =input("Enter Keyword: ")

'''
handle_search = input("search handle data?: y/n ")
if handle_search == "y":  
'''
  
'''
twitter_handle = input("Enter Handle: ")

Object5 = Twitter_handles(twitter_handle, consumer_key, consumer_secret, access_key, access_secret)
Object5.run()

'''
#object6 = twitter_api(keyword)
#tweets = object6.run()
	


#____________________________________Twitter_________________________________


print("fetching from twitter")
Object4 = twitter_api(keyword, consumer_key, consumer_secret, access_key, access_secret)
Object4.run()
print("twitter done") 


#RAYMOND WEIL Gen�ve
#______________________________________Twitter handles________________________

'''
Object5 = Twitter_handles(twitter_handle, consumer_key, consumer_secret, access_key, access_secret)
Object5.run()
'''

#_________________________________Streaming_api______________________________

    #_________________________ontime_________________________    
'''
print("fetching from twitter")
till_date = 'Jul 18 2019  4:00PM'

Object8 = streaming_api_time(till_date,keyword, consumer_key, consumer_secret, access_key, access_secret)
Object8.run()
print("tweets fetching done")
'''

