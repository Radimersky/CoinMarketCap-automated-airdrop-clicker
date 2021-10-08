import tweepy
from dotenv import load_dotenv
import os

load_dotenv()

def get_twitter_api_auth(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    if api.verify_credentials() == False:
        print("The twitter user credentials are invalid.")
    else:
        print("The twitter user credentials are valid.")
    return api


def retweet(tweet_id, api):
    try:
        response = api.retweet(tweet_id)
        return response.retweeted_status.id
    except Exception as e:
        print('tweet id:' + str(tweet_id) + ' failed to retweet with exception: ' + str(e))

def follow_twitter_user(id, api):
    try:
        response = api.create_friendship(screen_name = id)
        return response.screen_name
    except Exception as e:
        print('tweet id:' + str(id) + ' failed to follow with exception: ' + str(e))

index = "2"
# twitter_api_auth = get_twitter_api_auth(
#     os.getenv('TWITTER_ACCESS_TOKEN_' + index), 
#     os.getenv('TWITTER_ACCESS_TOKEN_SECRET_' + index), 
#     os.getenv('TWITTER_API_KEY_' + index), 
#     os.getenv('TWITTER_API_KEY_SECRET_' + index)
# )
twitter_api_auth = get_twitter_api_auth(
    os.getenv('TWITTER_API_KEY_' + index), 
    os.getenv('TWITTER_API_KEY_SECRET_' + index),
    os.getenv('TWITTER_ACCESS_TOKEN_' + index),
    os.getenv('TWITTER_ACCESS_TOKEN_SECRET_' + index)
)

# consumer_key = "fHaWvJTumuM7DXRfm0UEOB2Cu"
# consumer_secret = "fp6peYJlugfcqINinARQgP98cgUWL64HdRpumK9GRMp4eVOULZ"
# access_token = "1446154010256461827-NOAXCutdRHYVSB5NSzkda9guULUp7t"
# access_token_secret = "3JzxoopozlG90TtxPlBoVkLN4qmnpaCblAXB6mxQXxNwY"

# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth)
# api.retweet("1446358956193026049")
