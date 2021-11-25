from dotenv import load_dotenv
import tweepy, os

def setup():
    load_dotenv()
    auth = tweepy.OAuthHandler(os.environ.get('KEY'), os.environ.get('SEC'))
    auth.set_access_token(os.environ.get('ACCTK'), os.environ.get('ACCTKSEC'))
    return auth

def main():
    auth = setup()
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    with open('../data/keywords.txt','r') as fp:
        keywords = fp.read().splitlines()
    query = keywords.join(" OR ")
    
    # public_tweets = api.home_timeline()
    tweets = api.search_tweets(query,lang='en',count=200)
    for tweet in tweets:
        print(tweet.text)
    
if __name__ == '__main__':
    setup()
    main()
