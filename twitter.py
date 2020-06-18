import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    def __init__(self):
        key = ""
        secret = ""
        token = ""
        token_secret = ""

        try:
            self.auth = OAuthHandler(key, secret)
            self.auth.set_access_token(token, token_secret)
            self.api = tweepy.API(self.auth)
        except:
            pass

    def clean_tweet(self, tweet):
        return " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count = 10):
        tweets = []
        try:
            fetched_tweets = self.api.search(q = query, count = count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
        except:
            pass


def main():
    api = TwitterClient()
    tweets = api.get_tweets('Donald Trump', count = 200)
    positive_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print(f'Positive tweets percentage = {100*len(positive_tweets)/len(tweets)}')
    negative_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print(f'negative tweets percentage = {100*len(negative_tweets)/len(tweets)}')
    print(f'Neutral tweets percentage = {100*(len(tweets)-(len(negative_tweets)+len(positive_tweets)))/len(tweets)}')
    print("\n\nPositive Tweets :\n\n")
    for tweet in positive_tweets[:10]:
        print(tweet['text'])
    print("\n\nNegative Tweets :\n\n")
    for tweet in negative_tweets[:10]:
        print(tweet['text'])

if __name__ == '__main__':
    main()