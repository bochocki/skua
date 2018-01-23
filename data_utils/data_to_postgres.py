import data_munging as dm
import numpy as np
import pandas as pd

# load data and labels from text files
wiki_data = pd.read_csv('attack_annotated_comments.tsv', sep='\t', index_col=0)
wiki_annotations = pd.read_csv('attack_annotations.tsv', sep='\t')

# labels a comment as an atack if the majority of annoatators did so
labels = annotations.groupby('rev_id')['attack'].mean() > 0.5

# join labels and comments
wiki_data['attack'] = labels

# save original comments.
wiki_data['comment_original'] = data['comment']

# clean and preprocess comments


# upload comments to database
