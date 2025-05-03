import json
import time
import csv
import asyncio
import requests
import os
from configparser import ConfigParser
from random import randint

# Debug mode for testing
DEBUG_MODE = True

# Input Vars
query = "from:elonmusk since:2024-01-01 until:2024-04-30 -is:retweet"
url = "https://api.twitterapi.io/twitter/tweet/advanced_search"
querytype = "latest"

# Output Vars
all_tweets = []

try:
    # Reading credentials for authentication
    print('Reading config.ini ...')
    config = ConfigParser()
    config.read('conf/config.ini')
    api_key = config['TWITTERAPI']['API_KEY']
    print(f"API Key gefunden: {api_key[:5]} ...")

except Exception as e:
    print("Failed to read credentials. Exit with error:")
    print(e)
    exit()

try:
    if api_key is None:
        raise ValueError("Could not read api key.")

    else:
        # set loop and header params
        cursor = ""
        headers = {'x-api-key': api_key}

        print('Starting request loop ...')
        while True:
            response = requests.request(
                "GET",
                url,
                headers={
                    'x-api-key': '1228af8618b940f9a522eac41b970288',
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                params={
                    'query': query,
                    'queryType': querytype,
                    'cursor': cursor
                }
            )
            if response.status_code == 200:
                # debugging infos
                print(f"Status Code: {response.status_code}")
                print(f"Response Headers: {response.headers}")

                # throw exception for http error
                response.raise_for_status()

                # debug keys
                data = response.json()
                tweets = data.get('tweets', [])
                all_tweets.extend(tweets)
                tweet_count = len(all_tweets)
                print(f"Response data keys: {data.keys()}")
                print(f"Anzahl gefundener Tweets: {len(tweets)}")

                if DEBUG_MODE:
                    print(f'DEBUG_MODE active: stopping after first page. Got {tweet_count} tweets.')
                    print(f'Full API Response: {json.dumps(data, indent=2)}')
                    break

                if not data.get('nextCursor'):
                    print(f'Got {tweet_count} tweets. Finished.')
                    break

                # set cursor to the next page
                cursor = data.get('nextCursor')

                # wait random time to avoid rate limits
                print(f'Got {tweet_count} tweets. Sleeping random time ...')
                time.sleep(randint(1, 5))

            else:
                print("Received empty response:")
                # debugging infos
                print(f"Status Code: {response.status_code}")
                print(f"Response Headers: {response.headers}")
                print(f"Response Content: {response.text[:500]}...")
                print("Exiting ...")
                exit()

except Exception as e:
    print('Failed to get and process tweets. Exit with error:')
    print(e)
    exit()

try:
    print('Converting to file ...')

    filepath = "../data/twitter/tweets.csv"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    existing_ids = set()
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8", newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_ids.add(row["id"])

    with open(filepath, "a", encoding="utf-8", newline='') as f:
        if not all_tweets:
            print("No tweets to write. Exiting ...")
            exit()

        def flatten_tweet(tweet):
            if not tweet:
                return {}

            flat = {}
            for k, v in tweet.items():
                try:
                    if isinstance(v, (dict, list)):
                        flat[k] = json.dumps(v, ensure_ascii=False)
                    else:
                        flat[k] = v
                except Exception as e:
                    print(f"Error when processing field {k}: {e}")
                    flat[k] = None
            return flat

        flattened_tweets = [flatten_tweet(tw) for tw in all_tweets]
        if not flattened_tweets:
            print("Did not find tweets to write. Exiting ...")
            exit()

        fieldnames = list(flattened_tweets[0].keys())

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if os.stat(filepath).st_size == 0:
            writer.writeheader()

        new_count = 0
        for tweet in flattened_tweets:
            if tweet["id"] not in existing_ids:
                writer.writerow(tweet)
                new_count += 1

        print(f"Wrote {new_count} new tweets to CSV.")

except Exception as e:
    print('Failed to convert tweets to file. Exit with error:')
    print(e)