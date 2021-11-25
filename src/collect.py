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
    tweet_text = [t.text for t in tweets]
    num_tweets = len(tweet_text)
    columns = ['tweets','sentiment','topics']
    df = pd.DataFrame(columns=columns)
    df['tweets'] = tweet_text
    df.to_csv(filename, sep='\t')
    return df


def main():
    auth,keywords = setup()
    api = tweepy.API(auth, wait_on_rate_limit=True)
    query = keywords.join(" OR ")
    
    tweet_data = dict()
    while(len(tweet_data) < 1000):
        tweets = api.search_tweets(query,lang='en',count=100)
        for t in tweets:
            tweet_data[t.id] = t.text
    
    filename = '../data/tweet_data.csv'
    store_tweets(tweet_data.values(),filename)
        
    
    
if __name__ == '__main__':
    setup()
    main()
    
