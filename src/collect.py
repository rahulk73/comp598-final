from dotenv import load_dotenv
import tweepy, os
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

def main():
    auth,keywords = setup()
    api = tweepy.API(auth, wait_on_rate_limit=True)
    query = keywords.join(" OR ")
    
    tweets = api.search_tweets(query,lang='en',count=20)
    for tweet in tweets:
        print(tweet.text)
    
if __name__ == '__main__':
    setup()
    main()
