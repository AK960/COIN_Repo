# include libraries
import sys
import os
import argparse
from pprint import pprint
import json
import requests
import time
from random import randint

# local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.addTweetsToFile import WriteTweetsToCsv
from utils.trackCursor import ReadCursor, StoreCursor
from utils.readApiKey import ReadApiKey

def main():
    # Set debug mode
    parser = argparse.ArgumentParser(description="Starte das Python-Programm mit optionalem Debug-Modus.")
    parser.add_argument("--debug", action="store_true", help="Aktiviere den Debug-Modus.")
    parser.add_argument("--testloop", action="store_true", help="Aktiviere den LoopTest-Modus.")
    args = parser.parse_args()

    DEBUG_MODE = args.debug
    TEST_LOOP_MODE = args.testloop
    print(f"[Main][Info] Starting script with DEBUG_MODE: {DEBUG_MODE}")
    print(f"[Main][Info] Starting script with TEST_LOOP_MODE: {TEST_LOOP_MODE}")

    api_key = ReadApiKey()
    headers = {"X-API-Key": api_key}

    url = "https://api.twitterapi.io/twitter/tweet/advanced_search"
    # url = "https://api.twitterapi.io/twitter/user/last_tweets"

    print("[Main][Info] Making request ...")
    response = requests.request(
        "GET",
        url,
        headers=headers,
        params={
            "query": "from:elonmusk within_time:3h"
        }
    )

    print("[Main][Info] Response:")
    pprint(response.text)

    json_data = response.json()
    tweets = json_data.get("tweets", [])
    tweet_ids = [tweet["id"] for tweet in tweets]

    with open("data/twitter/new_tweets.json", "w") as f:
        json.dump(tweets, f, indent=4)

    with open("data/twitter/new_tweets.txt", "w") as f:
        f.write(json.dumps(tweets, indent=4))


if __name__ == "__main__":
    main()