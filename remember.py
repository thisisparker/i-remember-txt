#!/usr/bin/env python3

import random, json, yaml, os, time
from twython import Twython

fullpath = os.path.dirname(os.path.realpath(__file__))
CONFIG = os.path.join(fullpath,"config.yaml")
TWEETS = os.path.join(fullpath,"remember.json")
NEXT_TWEETS = os.path.join(fullpath, "remember-shuffle.json")

def get_config():
    with open(CONFIG,'r') as c:
        config = yaml.load(c)
    return config

def get_tweets():
    with open(TWEETS,'r') as f:
        tweets = json.load(f)
    return tweets

def get_next_tweets():
    with open(NEXT_TWEETS,'r') as f:
        next_tweets = json.load(f)
    return next_tweets

def write_next_tweets(next_tweets):
    with open(NEXT_TWEETS,'w') as f:
        json.dump(next_tweets,f)

def get_twitter_instance(config):
    twitter_app_key = config['twitter_app_key']
    twitter_app_secret = config['twitter_app_secret']
    twitter_oauth_token = config['twitter_oauth_token']
    twitter_oauth_token_secret = config['twitter_oauth_token_secret']
    return Twython(twitter_app_key, twitter_app_secret, twitter_oauth_token, twitter_oauth_token_secret)

def main():
    config = get_config()
    tweets = get_tweets()
    twitter = get_twitter_instance(config)

    next_tweets = get_next_tweets()

    if len(next_tweets) == 0:
        keys = [key for key in tweets.keys()]
        random.shuffle(keys)
        next_tweets = keys

    tweet_content = tweets[next_tweets.pop(0)]
    write_next_tweets(next_tweets)

    reply_to = 'null'

    for i in range(len(tweet_content)):
        response = twitter.update_status(status=tweet_content[i],in_reply_to_status_id=reply_to)
        reply_to = response['id_str']
        time.sleep(60)
        
if __name__ == "__main__":
    main()
