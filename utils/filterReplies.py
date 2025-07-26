import os
import pandas as pd

tweets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'twitter', 'tweets.csv')
tweets_cleaned = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'twitter', 'tweets_isTweet.csv')
tweets_cleaned_reply = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'twitter', 'tweets_isReply.csv')
tweets_path = os.path.abspath(tweets_path)
tweets_cleaned = os.path.abspath(tweets_cleaned)

def split_dataset():
    df = pd.read_csv(tweets_path)
    for type in ['isReply', 'isTweet']:
        if type == 'isReply':
            non_replies = df[df['isReply'] == True]
            non_replies.to_csv(tweets_cleaned_reply, index=False)

        elif type == 'isTweet':
            replies = df[df['isReply'] == False]
            replies.to_csv(tweets_cleaned, index=False)

        else:
            raise ValueError (f"Unknown type: {type}")
    
def merge_datasets():
    # Read the cleaned datasets
    df_tweets_isTweet = pd.read_csv(tweets_cleaned)
    df_tweets_isReply = pd.read_csv(tweets_cleaned_reply)
    df_tweets = pd.concat([df_tweets_isTweet, df_tweets_isReply], ignore_index=True)

    # Sort by time
    df_tweets['created_at'] = pd.to_datetime(df_tweets['created_at'], format='%a %b %d %H:%M:%S %z %Y')    
    df_tweets.sort_values(by='createdAt')

    # Save the merged dataframe
    df_tweets.to_csv(tweets_path, index=False)

if __name__ == "__main__":
    # Split
    #split_dataset()
    #print(f"[Info] Split datasets successfully. Cleaned files saved to {tweets_cleaned} and {tweets_cleaned_reply}.")

    # Merge
    merge_datasets()
    print(f"[Info] Merged datasets successfully. Merged file saved to {tweets_path}.")