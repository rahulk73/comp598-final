import pandas as pd
from pathlib import Path
from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
DATA = BASE_DIR.joinpath('data')

topics = {
    1:"Vaccination",
    2:"Variant",
    3:"Sanitary Measures",
    4:"Politics and Economy",
    5:"Symptoms and Testing",
    6:"Pandemic Stats",
    7:"Entertainment and Community",
    8:"Unrelated",
}
colours = {
    -1: 'C2',
    0: 'C1',
    1: 'C0',
}

def sentiment_group():
    df = pd.read_csv(DATA.joinpath('tweet_data.tsv'), sep='\t', header=0)
    for i in range(1,8):
        df_aux = df[df['topics']==i]
        df_aux['sentiment'].value_counts().plot.pie(autopct='%1.1f%%', colors=[colours[v] for v in df_aux['sentiment'].value_counts().keys()])
        plt.title(topics[i], bbox={'facecolor':'0.8', 'pad':5})
        plt.savefig(DATA.joinpath('fig' + str(i) + '.png'))
        plt.close()

def sentiment_all():
    df = pd.read_csv(DATA.joinpath('tweet_data.tsv'), sep='\t', header=0)
    df['sentiment'].value_counts().plot.pie(autopct='%1.1f%%', colors=[colours[v] for v in df['sentiment'].value_counts().keys()])
    plt.title("All Tweets", bbox={'facecolor':'0.8', 'pad':5})
    plt.savefig(DATA.joinpath('fig_all.png'))
    plt.close()

def cloud():
    df = pd.read_csv(DATA.joinpath('tweet_data.tsv'), sep='\t', header=0)
    with open(DATA.joinpath('keywords.txt')) as fp:
        keywords = fp.read().splitlines()
 
    comment_words = ''
    stopwords = list(STOPWORDS) + ['https','co','t','will','u','s'] +keywords
 
    # iterate through the csv file
    for val in df.tweets:
    
        # typecaste each val to string
        val = str(val)
    
        # split the value
        tokens = val.split()
        
        # Converts each token into lowercase
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        
        comment_words += " ".join(tokens)+" "
 
    wordcloud = WordCloud(width = 800, height = 800,
                    background_color ='white',
                    stopwords = stopwords,
                    min_font_size = 10).generate(comment_words)
    
    # plot the WordCloud image                      
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    
    plt.savefig(DATA.joinpath('cloud.png'))
    plt.close()

    
if __name__ == '__main__':
    cloud()
    