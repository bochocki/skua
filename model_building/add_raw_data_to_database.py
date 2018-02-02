from sqlalchemy import create_engine
import pandas as pd
import psycopg2

# run from skua directory

# (local) database information
psql_db = 'skua'
psql_user = 'brad'
psql_host = 'localhost'
psql_port = '5432'

# columns for each table
ol_cols = ['comment', 'label', 'handle'] # online learning data
ab_cols = ['comment', 'troll', 'label']  # abusive tweets data
wi_cols = ['comment', 'troll']           # wikipedia data

# ------------------------------------------------------------------------------
# Prep data

# Abusive tweets dataset ----------
# load data
ab_data = pd.read_csv('./raw_data/abusive_tweets.csv', index_col=0)

# assign data-specific class labels
ab_data['label'] = 'none'
ab_data.loc[ab_data['class'] == 0, 'label'] = 'hate'
ab_data.loc[ab_data['class'] == 1, 'label'] = 'swearing'
ab_data.loc[ab_data['class'] == 2, 'label'] = 'neither'

# assign troll label
ab_data['troll'] = False
ab_data.loc[ab_data['label'] == 'hate', 'troll'] = True

# rename column
ab_data.rename(index=str, columns={'tweet': 'comment'}, inplace=True)

# drop unneccesary columns
ab_data = ab_data[ab_cols]


# Wikipedia training dataset ----------

# load comments and annotations
wi_data = pd.read_csv('./raw_data/wikipedia_comments.tsv', sep='\t', index_col=0)
wi_anno = pd.read_csv('./raw_data/wikipedia_annotations.tsv',  sep='\t')

# label a comment as an atack if the majority of annoatators did so
wi_lab = wi_anno.groupby('rev_id')['attack'].mean() > 0.5

# join labels and comments
wi_data['troll'] = wi_lab

# remove newline and tab tokens
wi_data['comment'] = wi_data['comment'].apply(lambda x: x.replace("NEWLINE_TOKEN", " "))
wi_data['comment'] = wi_data['comment'].apply(lambda x: x.replace("TAB_TOKEN", " "))

# drop unnecessary columns
wi_data = wi_data[wi_cols]

# ------------------------------------------------------------------------------
# Load data into tables

# build engine
engine = create_engine( 'postgresql://{}@{}:{}/{}'.format(psql_user, psql_host, psql_port, psql_db) )

wi_data.to_sql('wikipedia', engine, if_exists='replace', index=False)
ab_data.to_sql('abusive',   engine, if_exists='replace', index=False)
