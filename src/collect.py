from dotenv import load_dotenv
import tweepy, os
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA = BASE_DIR.joinpath('data')

def setup():
    load_dotenv()

    with open(DATA.joinpath('keywords.txt')) as fp:
        keywords = fp.read().splitlines()

    auth = tweepy.OAuthHandler(os.environ.get('KEY'), os.environ.get('SEC'))
    auth.set_access_token(os.environ.get('ACCTK'), os.environ.get('ACCTKSEC'))
    return auth,keywords

def store_tweets(tweets,filename):
    num_tweets = len(tweets)
    columns = ['tweets','sentiment','topics']
    df = pd.DataFrame(columns=columns)
    df['tweets'] = tweets
    df.to_csv(filename, sep='\t', index=False)
    return df


def main():
    auth,keywords = setup()
    api = tweepy.API(auth, wait_on_rate_limit=True)
    query = (" OR ").join(keywords)
    query+=" -filter:retweets"
            
    tweets = tweepy.Cursor(api.search_tweets, 
                            q=query,
                            lang='en',
                            tweet_mode='extended').items(100)
    tweet_data = [t.full_text for t in tweets][:40]
    store_tweets(tweet_data,DATA.joinpath('tweet_data_additional.tsv'))
    
if __name__ == '__main__':
    setup()
    main()
    
