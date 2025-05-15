# Requirements
import csv
import json
import os
import sys
from utils.checkTweetsForDuplicates import DuplicateFinder

# Adjust field limit
maxInt = sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

# Writing tweets to the csv file
def WriteTweetsToCsv(tweets):
    try:
        # Target location
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'twitter', 'tweets.csv')
        filepath = os.path.abspath(filepath)

        # Store existing tweet ids as set and write all existing ones
        existing_ids = set()
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8", newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_ids.add(row["id"])

        # Open the file in append mode
        with open(filepath, "a", encoding="utf-8", newline='') as f:
            if not tweets:
                print("No tweets to write. Exiting ...")
                exit()

            # Flatten tweet structure
            def flatten_tweet(tw):
                if not tw:
                    return {}

                flat = {}
                for k, v in tw.items():
                    try:
                        if isinstance(v, (dict, list)):
                            flat[k] = json.dumps(v, ensure_ascii=False)
                        else:
                            flat[k] = v
                    except Exception as e:
                        print(f"Error when processing field {k}: {e}")
                        flat[k] = None
                return flat

            flattened_tweets = [flatten_tweet(tw) for tw in tweets]
            if not flattened_tweets:
                print("[WriteTweetsToCsv][Info]Did not find tweets to write. Exiting ...")
                exit()

            # Derive col names from the first tweet
            fieldnames = list(flattened_tweets[0].keys())

            # Create a csv writer with fieldnames
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if os.stat(filepath).st_size == 0:
                writer.writeheader()

            # Write new tweets to a file
            new_count = 0
            for tweet in flattened_tweets:
                if tweet["id"] not in existing_ids:
                    writer.writerow(tweet)
                    new_count += 1

            print(f"[WriteTweetsToCsv][Info] Wrote {new_count} new tweets to CSV.")

            # Finding duplicates
            print("[WriteTweetsToCsv][Info] Checking for duplicates ...")
            try:
                has_duplicates = DuplicateFinder(filepath)
                print(f"[WriteTweetsToCsv][Info] Has duplicates: {has_duplicates}")
            except Exception as e:
                print("[WriteTweetsToCsv][Error] Could not call function. Exit with error:")
                print(e)

    except Exception as e:
        print('[WriteTweetsToCsv][Error] Failed to convert tweets to file. Exit with error:')
        print(e)