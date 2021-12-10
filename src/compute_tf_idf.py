# This script computes the TF-IDF scores of each word in the tweet dataset
# And outputs the 10 words in each category with the highest TF-IDF

import os, sys, json, math, re
import pandas as pd
import os.path as osp

parent_path =  osp.abspath(osp.join(__file__ ,"../.."))

def main():
    # Load stopwords
    stopwords_filename = parent_path + '/data/stopwords.txt'
    with open(stopwords_filename,'r') as fp:
        lines = fp.read().splitlines()
        stopwords = lines[6:] # Remove first 6 lines of formatting

    # Load tweet annotated dataset
    tweet_filename = parent_path + '/data/tweet_data.tsv'
    data = pd.read_csv(tweet_filename,sep='\t')
    
    # For each category, find top 10 words with highest tf-idf 
    categories = range(1,9)
    word_count = word_occurences(categories,data,stopwords)
    top_tf_idf = best_tf_idf(categories,data,word_count)
    
    # If output file directory doesn't exist, create it
    output_filename = parent_path + '/data/tf_idf.json'
    os.makedirs(osp.dirname(output_filename),exist_ok=True)
    
    # Write to output file
    with open(output_filename, "w") as output_file:
        json.dump(words,output_file,indent=4)
        
# tf_idf(word,category,data) = tf(word,category) * idf(word,data)
# tf(word,category) = num. of times word is used in category
# idf(word, data) = log {total num of categories / num of categories using word}

# Returns dictionary of top 10 TF-IDF of words in each category 
def best_tf_idf(categories,data,word_count):
    top_tf_idf = dict()
    for category in categories:
        tf_idf = dict()
        # For each word used in category
        for word, tf in word_count[category].items(): 
            # Compute number of categories using word 
            num_categories = 0 
            for c in categories:
                if word in word_count[c].keys():
                    num_categories += 1
            # Compute TF_IDF = IDF * TF
            idf = math.log(len(categories)/num_categories)
            tf_idf[word] = idf * tf
        # Pick 10 highest values of tf_idf for each category
        top_tf_idf[category] = sorted(tf_idf.keys(),key=tf_idf.get,reverse=True)[:10]
    return top_tf_idf

# Outputs a 2D dictionary of {'category' : {'word' : num of occurences in category}} 
def word_occurences(categories,data,stopwords):
    word_count = dict()
    for category in categories: 
        # Concatenate all tweets of given category 
        byCat = data[data['topics'] == category]
        tweets = ' '.join([tweet for tweet in byCat['tweets']])
        
        # Remove all links
        tweets = re.sub(r'http\S+', '', tweets)
        
        # Replace punctuations with spaces, split into lowercase words
        delimiters = ['(',')','[',']',',','.','?','!',':',';','#','&']
        for d in delimiters:
            tweets = tweets.replace(d,' ')
        words = tweets.lower().split()
    
        # Count num of occurences of each word (except stopwords/non-alphabetical)
        word_byCat = dict()
        for w in words:
            if (w.isalpha() and w not in stopwords):
                if (w in word_byCat):
                    word_byCat[w] += 1
                else:
                    word_byCat[w] = 1
        word_count[category] = word_byCat
        
    return word_count