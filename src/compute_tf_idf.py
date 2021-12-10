# This script computes the TF-IDF scores of each word in the tweet dataset
# And outputs the 10 words in each category with the highest TF-IDF

import os, sys, json
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
    categories = 1:8
    words = dict()
    for category in categories:
        words[category] = compute_tf_idf(category,data,stopwords)
    
    # If output file directory doesn't exist, create it
    output_filename = parent_path + '/data/tf_idf.json'
    os.makedirs(osp.dirname(output_filename),exist_ok=True)
    
    # Write to output file
    with open(output_filename, "w") as output_file:
        json.dump(words,output_file,indent=4)
        
        
# Given a category, find top 10 TF-IDF of words in category 
def compute_tf_idf(category,data,stopwords):
    df = data[data["topics"] == str(category)]
    
    # For inverse frequency, use all 1000 tweets
    
    

if __name__=='__main__':
    main()
