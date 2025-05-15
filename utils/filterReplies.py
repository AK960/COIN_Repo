import os
import pandas as pd

tweets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'twitter', 'tweets.csv')
tweets_cleaned = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'twitter', 'tweets_isTweet.csv')
tweets_path = os.path.abspath(tweets_path)
tweets_cleaned = os.path.abspath(tweets_cleaned)


# read the entire dataframe
df = pd.read_csv(tweets_path)

# filter replies from the dataframe
non_replies = df[df['isReply'] == False]

# export to csv file
non_replies.to_csv(tweets_cleaned, index=False)
