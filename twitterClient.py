import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

import datetime
from datetime import timedelta, date
import time

import csv
import pandas
import scipy
import matplotlib
import numpy
import sklearn

from sklearn import linear_model
from sklearn import svm

class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self):
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'wELRpStXm3ClfLm1bmFNnHylH'
        consumer_secret = 'FHpTU0BBClgULhOMFrp2QyjaMcFg9LDWaNO2buyTQJ0WUtxyvW'
        access_token = '1236399499565608961-UtDzGjrLbcRevxCJRX2gAIv9s5HIhV'
        access_token_secret = 'MscQlrcL0vtGPBxct09tXTVxgwQD70UnOxEs0bY19X7yD'

        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except:
            print("Error: Authentication Failed")

        # creating object of TwitterClient Class 
        # api = TwitterClient()
        # calling function to get tweets
        wSent = ["WSENT"]
        aSent = ["ASENT"]

        for index in range(3,8):
            day = datetime.date.today() - datetime.timedelta(days = index)
            wTweets = self.get_tweets(query = 'weather', count = 100, geocode='41.2565,-96.05,5mi', until=day)
            aTweets = self.get_tweets(query = '', count = 100, geocode='41.2565,-96.05,5mi', until = day)

            ptweets = [tweet for tweet in wTweets if tweet['sentiment'] == 'positive']
            ntweets = [tweet for tweet in wTweets if tweet['sentiment'] == 'negative']
            netPosSent = (len(ptweets)/len(wTweets)) - (len(ntweets)/len(wTweets))

            wSent.append(netPosSent)

            ptweets = [tweet for tweet in aTweets if tweet['sentiment'] == 'positive']
            ntweets = [tweet for tweet in aTweets if tweet['sentiment'] == 'negative']
            netPosSent = (len(ptweets)/len(aTweets)) - (len(ntweets)/len(aTweets))

            aSent.append(netPosSent)
        
        # print(wSent)
        # print(aSent)


        url = "https://www.ncei.noaa.gov/orders/cdo/2069913.csv"

        dataset = pandas.read_csv(url)
        dataset = dataset.drop(['STATION', 'NAME', 'DATE'], axis = 1)
        dataset['WSENT'] = wSent[1:]
        # dataset['ASENT'] = aSent[1:]
        dataset = dataset.dropna()
        # print(dataset.shape)

        classifiers = [
            svm.SVR(),
            linear_model.SGDRegressor(),
            linear_model.BayesianRidge(),
            linear_model.LassoLars(),
            linear_model.ARDRegression(),
            linear_model.PassiveAggressiveRegressor(),
            linear_model.TheilSenRegressor(),
            linear_model.LinearRegression()
        ]

        trainingData   = dataset.drop(['WSENT'], axis=1)
        trainingScores = dataset['WSENT']
        predictionData = dataset.drop(['WSENT'], axis=1)

        global clf

        for item in classifiers:
            # print(item)
            clf = item
            clf.fit(trainingData, trainingScores)
            print(clf.predict(predictionData),'\n')


    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'

    def get_tweets(self, query, count, geocode, until): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count, geocode=geocode, until=until) 
  
            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 
  
                # saving text of tweet 
                parsed_tweet['text'] = tweet.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
  
                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            # return parsed tweets 
            return tweets 
  
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


    clf = linear_model.LinearRegression()

    def predict(self, precip, snow, tavg, tmax, tmin):
        predictionData = [precip, snow, tavg, tmax, tmin]
        predictionData = [predictionData, predictionData]
        
        global clf
        # clf = linear_model.LinearRegression()
        # clf.fit(trainingData, trainingScores)
        return clf.predict(predictionData)


# if __name__ == "__main__":
#     # calling main function
#     main()