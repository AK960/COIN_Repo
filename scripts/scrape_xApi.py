import sys
import os
import argparse
import requests
import time
from random import randint


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

    # Declare static vars
    api_key = ReadApiKey()
    headers = {'x-api-key': api_key}
    url = "https://api.twitterapi.io/twitter/tweet/advanced_search"

    # Counter
    i = 1

    while True:
        try:
            cursor = ReadCursor()
            print(f"[Main][Info] Starting new scraping loop with cursor [...{cursor[-10:]}]")
            print(f"[Main][Info] Iteration {i}")

            print("[Main][Info] Making request ...")
            response = requests.request(
                "GET",
                url,
                headers=headers,
                params={
                    "query": "from:elonmusk since:2023-05-01 until:2025-05-01 -is:retweet",
                    "cursor": cursor
                }
            )

            if response.status_code == 200:
                # Debugging Infos
                print(f"[Main][Success] Status Code: {response.status_code}")
                print("[Main][Info] Processing response ...")

                # throw exception for http error
                response.raise_for_status()

                # Store response
                json_data = response.json()

                # Extract necessary vars
                has_next_page = json_data.get("has_next_page")
                next_cursor = json_data.get("next_cursor")
                tweets = json_data.get("tweets", [])
                tweet_ids = [tweet["id"] for tweet in tweets]
                new_tweet_count = len(tweets)
                print(f"[Main][Info] New Tweets count: {new_tweet_count}")
                print(f"[Main][Info] New Total Tweets count: {len(tweets)}")

                # Store cursor data
                print(f"[Main][Info] Storing new cursor [...{next_cursor[-10:]}] to cursor.yml ...")
                StoreCursor(has_next_page, next_cursor, new_tweet_count, tweet_ids)

                # Save to CSV
                print("[Main][Info] Saving Tweets to CSV ...")
                try:
                    WriteTweetsToCsv(tweets)
                except Exception as e:
                    print("[Main][Error] Could not write tweets to CSV. Exiting ...")
                    raise

                # Terminating loop conditions
                if not has_next_page:
                    print(f"[Main][Finished] Got {new_tweet_count} tweets. Finished.")
                    break

                if TEST_LOOP_MODE:
                    if i == 800:
                        print(f"[Main][Info] TEST_LOOP_MODE active: stopping after three pages.")
                        break

                if DEBUG_MODE:
                    debug_mode_tweets = json_data["tweets"][new_tweet_count - 1]
                    print("[Main][Info] DEBUG_MODE active: stopping after first page.")
                    # pprint(debug_mode_tweets)
                    i += 1
                    break

                # Update counter
                i += 1

                # Wait random time to avoid rate limits
                delay = randint(1, 5)
                print(f"[Main][Info] Starting new iteration in {delay} seconds ...")
                time.sleep(delay)

        except Exception as e:
            print(f"[Main][Error] {str(e)}")
            raise

if __name__ == "__main__":
    main()
