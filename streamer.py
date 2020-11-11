from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import numpy as np
import pandas as pd
import credential
import matplotlib.pyplot as plt
import re
from textblob import TextBlob
import tweepy as tw
import sys
Pve=0
Nve=0
Nl=0
"""
Authenticater
"""

class TwitterAuthenticater():
    def authenticate_twitter_app(self):
     auth = OAuthHandler(credential.CONSUMER_KEY,credential.CONSUMER_SECRET)
     auth.set_access_token(credential.ACCESS_TOKEN,credential.ACCESS_TOKEN_SECRET)
     return auth




"""
client
"""
class TwitterClient():
    def __init__(self):
        self.auth=TwitterAuthenticater().authenticate_twitter_app()
        self.twitter_client=API(self.auth)
        #self.twitter_user=twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client
    def get_user_timeline_tweets(self,user,num_tweets):
        try:
            tweets=[]
            f1 = open("Peson_tweet.json", "w")
            for     tweet in self.twitter_client.user_timeline(screen_name=user,count=num_tweets,lang="en"):
                json.dump(tweet._json,f1)
                f1.write("\n")
                tweets.append(tweet)
            f1.close()
            return tweets
        except tw.TweepError as e:
            print("User Not Found ... ")
            sys.exit()
    def get_friend_list(self,num_friends):
        friend_list=[]
        for friend in Cursor(self.twitter_client.friends,id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list
    def get_home_timeline_tweets(self,num_tweets):
        home_timeline_tweets=[]
        for tweet in Cursor(self.twitter_client.home_timeline,id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets
    
            
            


"""
tweet streamer
"""
class TwitterStreamer():
   
    def __init__(self):
        self.twitter_authenticator=TwitterAuthenticater()
    def stream_tweets(self,has_tag_list,no_of_tweets):
        query_tweets=[]
        f = open("hash_tag_tweets.json", "w")
        
        twitter_client1=TwitterClient()
        twitter_client=twitter_client1.get_twitter_client_api()
        for tweet in twitter_client.search(has_tag_list, lang="en", count=no_of_tweets):
            query_tweets.append(tweet)
            json.dump(tweet._json,f)
            f.write("\n")
        f.close()
        return query_tweets
    """
    def stream_tweets(self,fetched_tweets_filename,has_tag_list):
        listener=TwitterListener(fetched_tweets_filename)
        auth=self.twitter_authenticator.authenticate_twitter_app()
        #stream=Stream(auth,listener)
        #stream.filter(track=hash_tag_list, languages=["en"])
        
        home_timeline_tweets=[]
        for tweet in Cursor(self.twitter_client.home_timeline,id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets
    """

class TwitterListener(StreamListener):
    
    def on_error(self,status):
        if status==420:
            #limit 
            return False
        print(status)
"""    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

        
    def on_data(self,data):
        try:
            print(data)
            with open(self.fetched_tweets_filename,'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error : "%str(e))
        return True
"""

 



class TweetAnalyzer():
    
    """
analyze tweet
    """
    def tweet_to_dataframe(self,tweets):
        df=pd.DataFrame(data=[tweet.text for tweet in tweets],columns=['Tweets'])
        
       # df['id']=np.array([tweet.id for tweet in tweets])
        #df['len']=np.array([len(tweet.text) for tweet in tweets])
        #df['date']=np.array([tweet.created_at for tweet in tweets])
        #df['source']=np.array([tweet.source for tweet in tweets])
        #df['likes']=np.array([tweet.favorite_count for tweet in tweets])
        #df['retweets']=np.array([tweet.retweet_count for tweet in tweets])
        return df
    def clean_tweet(self,tweet):
         return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    def analyze_sentiment(self,tweet):
        analysis=TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            global Pve
            Pve+=1
            return "Positive"
        elif analysis.sentiment.polarity == 0:
            global Nl
            Nl+=1
            return "Neutral"
        else:
            global Nve
            Nve+=1
            return "Negative"
    
    
if __name__ == '__main__':
    twitter_client=TwitterClient()
    api=twitter_client.get_twitter_client_api()
    tweetanalyzer=TweetAnalyzer()
    twitter_streamer = TwitterStreamer()
    namehashtag=input("Press 1 For Name \nPress 2 For Keyword\n")
    if(namehashtag=="1"):
        person=input("Enter Twitter Name : ")
        nooftweet=input("How Many Tweets : ")
        tweets=twitter_client.get_user_timeline_tweets(person,nooftweet)
        df=tweetanalyzer.tweet_to_dataframe(tweets)
        df['Analysis']=np.array([tweetanalyzer.analyze_sentiment(tweet) for tweet in df['Tweets']])
        print(df)
    elif(namehashtag=="2"):
        keyword=input("Enter Keyword : ")
        nooftweet=input("How Many Tweets : ")
        tweet=twitter_streamer.stream_tweets(keyword,nooftweet)
        df=tweetanalyzer.tweet_to_dataframe(tweet)
        df['Analysis']=np.array([tweetanalyzer.analyze_sentiment(tweet)  for tweet in df['Tweets']])
        print(df)
    else:
        print("Input is wrong")

    
    print("Positive Tweets : " ,Pve )
    print("Negative Tweets : " ,Nve )
    print("Neutral Tweets :  " ,Nl)
    labl = ['Positive', 'Negative', 'Neutral']
    data = [Pve,Nve,Nl]
    sizes=data
    fig = plt.figure(figsize =(10, 7))
    plt.subplot(title='Result Of Analyzing')
    plt.pie(data,autopct='%1.1f%%', labels = labl)
    
    plt.show()
