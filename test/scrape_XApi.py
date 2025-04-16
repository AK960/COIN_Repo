import json
import time
import csv
import asyncio
from twikit import Client, TooManyRequests
from datetime import datetime
from configparser import ConfigParser
from random import randint
from pprint import pprint

# Vars
min_tweets = 5
query = 'elonmusk'

async def main():
    try:
        # Include credentials
        config = ConfigParser()
        config.read('conf/config.ini')
        print('Reading config.ini')
        username = config['CREDS']['X_USERNAME']
        password = config['CREDS']['X_PASSWORD']
        email = config['CREDS']['X_EMAIL']

        # Authenticate to X.com 1) user creds or 2) cookies
        # Run this once to get cookies, afterward use cookies
        client = Client(language='en-US')
        #await client.login(auth_info_1=username, auth_info_2=email, password=password)
        #client.save_cookies('conf/cookies.json')
        # Use cookies
        client.load_cookies('conf/cookies.json')

        # Get tweets
        tweets = await client.search_tweet(query, product='Latest')

        for tweet in tweets:
            tweet_dict = vars(tweet)
            with open('res/tweets.json', 'w', encoding='utf-8') as f:
                json.dump(tweet_dict, f, ensure_ascii=False, indent=4)

            pprint(vars(tweet))
            break

    except Exception as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(main())