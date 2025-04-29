import json
import time
import csv
import asyncio
import requests
from pyjsparser.parser import true
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
        # Reading credentials for authentication
        config = ConfigParser()
        config.read('conf/config.ini')
        print('Reading config.ini')
        user_id = config['TWITTERAPI']['USER_ID']
        api_key = config['TWITTERAPI']['API_KEY']

        try:
            query = "from:elonmusk since:2023-05-01 until:2025-05-01"
            url = "https://api.twitterapi.io/twitter/tweet/advanced_search"
            headers = {'x-api-key': api_key}
            response = requests.get(url, headers=headers)
            response_dict = response.json()
            response_out = json.dumps(response_dict, indent=4)

            with open()

        except Exception as e:
            print("Failed to get tweets. Exit with error:")
            print(e)

    except Exception as e:
        print("Failed to read credentials. Exit with error:")
        print(e)

if __name__ == "__main__":
    asyncio.run(main())