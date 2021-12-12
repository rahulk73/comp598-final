import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA = BASE_DIR.joinpath('data')


def main():
    df = pd.read_csv(DATA.joinpath('tweet_data_dirty.tsv'), sep='\t', header=0)
    df = df[df['topics']!=8]
    df.to_csv(DATA.joinpath('tweet_data.tsv'), sep='\t', index=False)


    
if __name__ == '__main__':
    main()
    
