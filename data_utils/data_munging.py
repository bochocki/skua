import numpy as np
import pandas as pd
import psycopg2
import re
import string


def preprocess_text(tweet):
    # define some useful regex
    mention_regex = r'@[\w\-]+'
    url_regex = (r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
                '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    # remove unnecessary symbols
    tweet = re.sub(r'\n', ' ', tweet)  # newlines
    tweet = re.sub(r'\t', ' ', tweet)  # tabs
    tweet = re.sub(url_regex, ' ', tweet)  # urls
    tweet = re.sub(mention_regex, ' ', tweet)  # mentions
    tweet = re.sub(r'[^\w\s]', ' ',tweet)  #punctuation
    tweet = re.sub(r'\s+', ' ', tweet) # extra whitespace
    tweet = tweet.strip() # leading/trailing whitespace

    ## TODO: REMOVE pic.twitter.com

    return tweet.lower()


def make_like_tweet(text):
    return text.str.slice(0, 279, 1)


def balance_samples(df_1, df_2):
    lengths = [len(df_1), len(df_2)]

    if lengths[0] < lengths[1]:
        new_df_1 = df_1
        new_df_2 = df_2.sample(lengths[0])
    elif lengths[0] > lengths[1]:
        new_df_1 = df_1.sample(lengths[1])
        new_df_2 = df_2
    else:
        new_df_1 = df_1
        new_df_2 = df_2

    return new_df_1.append(new_df_2).sample(frac=1).reset_index(drop=True)


def get_labeled_data(dbname='skua_db', username='brad'):
    con = None
    con  = psycopg2.connect(database=dbname, user=username)
    sql_query = """
    SELECT * FROM main_data_table;
    """

    return pd.read_sql_query(sql_query, con)
