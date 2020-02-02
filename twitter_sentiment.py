import time
import config
import sys
import datetime
import re
import os
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")
import yfinance as yf
import pymysql
import pandas as pd
from yahoo_fin import stock_info as si
import matplotlib as mpl
import matplotlib.pyplot as plt
import glob
import shutil
import nltk
import warnings
warnings.filterwarnings('ignore')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()
import time
import datetime
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")
currentdate = now.strftime("%Y-%m-%d")

db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
cursor = db.cursor()
cursor.execute("SELECT symbol FROM symbols WHERE active=1")
symbols=cursor.fetchall()




def main():
    print('Starting twitter module')


    tw()


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = config.consumer_key
        consumer_secret = config.consumer_secret
        access_token = config.access_token
        access_token_secret = config.access_token_secret



        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]), wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0.1:
            return 'positive'
        elif analysis.sentiment.polarity == 0 or analysis.sentiment.polarity == 0.1:
            return 'neutral'
        else:
            return 'negative'


			
    def get_tweet_score(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity != 0:
            return analysis.sentiment.polarity			
        else:
            return 'neutral'			



    def get_tweets(self, query):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:


            marketcount=market_count()
#            print (marketcount)

#            max_tweets=1200/marketcount
            max_tweets=1200

            fetched_tweets = [status for status in tweepy.Cursor(self.api.search, q=query).items(max_tweets)]

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
				
				
                parsed_tweet['score'] = self.get_tweet_score(tweet.text)

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




def tw():
          for symbol in symbols: #Loop trough the stock summary
            try:
                symbol=(symbol[0])
                				
                # creating object of TwitterClient Class
                api = TwitterClient()
                name=symbol_full_name(symbol, 3)

                query = symbol_func(symbol, 4)
                # calling function to get tweets
                tweets = api.get_tweets(query=query)

                print (symbol, (" Number of tweets extracted: {}.\n".format(len(tweets))))
#                print (tweets)

                # picking positive tweets from tweets
                ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
                # percentage of positive tweets
#                print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
                positive=round(100 * len(ptweets) / len(tweets), 2)
                # picking negative tweets from tweets
                ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
                negative= round(100 * len(ntweets) / len(tweets), 2)
                # percentage of negative tweets
#                print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
                
#                print (neutral)
                tweets_score = [tweet for tweet in tweets if tweet['score'] != 'neutral']
                tweet_score= [ sub['score'] for sub in tweets_score ]
                tweet_texts= [ sub['text'] for sub in tweets_score ]
                passage = str(tweet_texts)
                nltk_score= round(sia.polarity_scores(passage)['compound'], 2)
                print ("Sentiment Score: ", round(sia.polarity_scores(passage)['compound'], 2))
                #print (str(tweet_texts))
                average = sum(tweet_score) / len(tweet_score)
                average= round(average, 2)
#                print(symbol, "Average of the list =", average) 
                printed = (symbol, "Positive tweets percentage: {} %".format(positive), "Negative tweets percentage: {} %".format(negative), "Average NLTK Score is: {} ".format(average))
                print (printed)



                try:
                    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
                    cursor = db.cursor()
                    cursor.execute('update symbols set positive_sentiments = %s, negative_sentiments =%s, tweeter_polarity =%s, tweeter_text=%s, tweeter_score=%s where symbol=%s',(positive, negative, average, str(tweet_texts), nltk_score, symbol))
                    cursor.execute('insert into logs(date, entry) values("%s", "%s")' % (currenttime, printed))
                    cursor.execute("update history set positive_tweets = %s, negative_tweets =%s, twitter_polarity ='%s', twitter_score='%s'  where symbol='%s' and date='%s'" % (positive, negative, average, nltk_score, symbol, currentdate))
                    db.commit()
                except pymysql.Error as e:
                    print ("Error %d: %s" % (e.args[0], e.args[1]))
                    sys.exit(1)
                finally:
                    db.close()


                # percentage of neutral tweets
#                print ("Neutral tweets percentage: {} %".format(
#                    100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)))
					
                neutral= (100 - negative - positive)
                labels = 'Neutral', 'Negative', 'Positive' 
                print (neutral, negative, positive)
                sizes = (neutral, negative, positive)
                colors = ["#1f77b4",  "#fe2d00", "#2ca02c"]				
                explode = (0, 0.1, 0)  
                
                fig1, ax1 = plt.subplots()
                
                ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', colors=colors, shadow=True, startangle=90)
                ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                plt.grid()
                plt.title(name, bbox={'facecolor':'0.8', 'pad':5}, fontsize=18)
                plt.xlabel("Polarity is: {} ".format(average)+" NLTK Score is: {} ".format(nltk_score), fontsize=18)
                #plt.ylabel("Unit")
                plt.show()					
                plt.savefig('/root/PycharmProjects/stock-advisor/images/tweets.png', bbox_inches = 'tight', pad_inches = 0)
                newfilename=("{}_tweets.png".format(symbol))
                my_path = "/root/PycharmProjects/stock-advisor/images/tweets.png"
                new_name = os.path.join(os.path.dirname(my_path), newfilename)
                os.rename(my_path, new_name)

#                print (new_name)

                src_dir = "/root/PycharmProjects/stock-advisor/images/"
                dst_dir = "/var/www/html/images/"
                for pngfile in glob.iglob(os.path.join(src_dir, "*.png")):
                  shutil.copy(pngfile, dst_dir)				

					

                # printing first 5 positive tweets
#                print("\n\nPositive tweets:")
#                for tweet in ptweets[:10]:
#                    print(tweet['text'])

                # printing first 5 negative tweets
#                print("\n\nNegative tweets:")
#                for tweet in ntweets[:10]:
#                    print(tweet['text'])

                time.sleep(600)



            except:
               continue



def symbol_func(symbolname, value):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    symbol = symbolname
    cursor.execute("SELECT * FROM symbols WHERE symbol = '%s'" % symbol)
    r = cursor.fetchall()
    for row in r:
        if row[1] == symbolname:
            return row[value]

    return False


def market_count():
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    #market=marketname
    cursor.execute("SELECT COUNT(*) FROM symbols where active=1")
    r = cursor.fetchall()
    for row in r:
        return row[0]
    return 0

def symbol_full_name(symbolname, value):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    symbol = symbolname
    cursor.execute("SELECT * FROM symbols WHERE symbol = '%s'" % symbol)
    r = cursor.fetchall()
    for row in r:
        if row[1] == symbolname:
            return row[value]

    return False	
	
	
if __name__ == "__main__":
    main()
