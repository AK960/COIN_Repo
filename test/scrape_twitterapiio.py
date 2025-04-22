import requests
import pandas as pd
import time  # Optional: to avoid rate limits

url = "https://api.twitterapi.io/twitter/user/last_tweets"
headers = {"X-API-Key": "<api_key>"}  # Replace with your actual key
querystring = {"userName": "elonmusk", "cursor": "\"\""}

all_tweets = []
page = 0

while len(all_tweets) < 1000:
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data_first_level = response.json()
        data = data_first_level.get("data", {})

        tweets = data.get("tweets", [])
        cursor = data.get("next_cursor")

        print('fetching tweets...')
        # Skip pin_tweet (already shown separately)
        pin_tweet_id = data.get("pin_tweet", {}).get("id")

        # Append tweet info
        for tweet in tweets:
            if tweet.get("id") == pin_tweet_id:
                continue
            all_tweets.append({
                "id": tweet.get("id"),
                "url": tweet.get("url"),
                "text": tweet.get("text"),
                "source": tweet.get("source"),
                "retweetCount": tweet.get("retweetCount"),
                "replyCount": tweet.get("replyCount"),
                "likeCount": tweet.get("likeCount"),
                "quoteCount": tweet.get("quoteCount"),
                "viewCount": tweet.get("viewCount"),
                "createdAt": tweet.get("createdAt"),
            })

        print(f"✅ Page {page + 1}: Collected {len(tweets)} tweets (Total: {len(all_tweets)})")

        # Update cursor for next request
        if data_first_level.get('has_next_page'):
            querystring["cursor"] = cursor
            page += 1
            time.sleep(0.5)  # Optional delay to respect rate limits
        else:
            print("No nextCursor found. Finished.")
            break

    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        break

df = pd.DataFrame(all_tweets)
df.to_csv("elon_musk_1000_tweets.csv", index=False, encoding='utf-8')
print("✅ Saved to elon_musk_1000_tweets.csv")
