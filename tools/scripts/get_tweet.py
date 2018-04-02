# inspired by: https://stackoverflow.com/a/37862197/5538961

import csv
import os

import pandas as pd
import tweepy  # https://github.com/tweepy/tweepy

# Twitter API credentials
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_key = os.getenv('ACCESS_KEY')
access_secret = os.getenv('ACCESS_SECRET')


def get_all_tweets(screen_name):
    """ 

    Parameters
    ----------
    screen_name:str
        user account
    """

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(
            screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

    data = [[tweet.id_str, tweet.created_at, tweet.text]
            for tweet in alltweets]
    return pd.DataFrame(data, columns=['_id', 'timestamp', 'text'])


if __name__ == '__main__':
    for i in range(1, 14):
        ratp = f'Ligne{i}_RATP'
        print(f'Getting tweets for {ratp}')
        get_all_tweets(ratp).to_csv(ratp+'.csv', index=False)
