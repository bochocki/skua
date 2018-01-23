#!flask/bin/python
import colorlover as cl
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask_api import app
import fasttext as ft
import numpy as np
import pickle
import re
#from tensorflow.python import keras
from textblob import TextBlob

#app = Flask(__name__)

# color management
colors = cl.scales['11']['div']['RdBu'][::-1]

# LOAD MODELS
# fasttext
ft_model = ft.load_model('./flask_api/model.bin')

# keras
'''
ks_tokenizer = pickle.load( open( "keras_tokenizer.p", "rb" ) )
ks_classes = pickle.load( open( "keras_classes.p", "rb"))
ks_model = keras.models.load_model("keras_model.ks", custom_objects=None, compile=True)
ks_model.predict(np.array(ks_tokenizer.texts_to_matrix(['hack'])))
'''
def preprocess(tweet):
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


def fasttext_estimator(model, tweet):
    # get estimate
    estimate = model.predict_proba([tweet])

    # get label
    label = estimate[0][0][0]

    # get probability of abuse
    if label == '__label__yes':
        probability = estimate[0][0][1]
    else:
        probability = 1 - estimate[0][0][1]

    return probability, label


def keras_estimator(tokenizer, classes, tweet):
    global ks_model

    # tokenize
    tokenized_tweet = tokenizer.texts_to_matrix([tweet])

    # get estimate
    estimate = ks_model.predict(np.array(tokenized_tweet))

    # get label
    label = classes[np.argmax(estimate)]

    # get probability of abuse
    probability = estimate[0][classes == 'yes'][0]

    return probability, label


def sentiment_estimator(tweet):
    return (-TextBlob(tweet).sentiment.polarity + 1) / 2

@app.route('/')
@app.route('/index')
def index():
   return "Skua v0.0.1"

from flask import request

@app.route('/CleverBird', methods=['GET'])
def predict_abuse():

    elem  = request.args.get('element')
    tweet = request.args.get('tweet')
    print(tweet)

    '''
    tweet = preprocess(request.args.get('tweet'))

    print(tweet)


    elem  = request.args.get('element')

    # classifiers
    ft_score, ft_label = fasttext_estimator(ft_model, tweet)
    ks_score, ks_label = fasttext_estimator(ft_model, tweet)#keras_estimator(ks_tokenizer, ks_classes, tweet)
    s_score = sentiment_estimator(tweet)

    ens_score = np.mean([ft_score, ks_score, s_score])

    print('\n[enseble]    score: {0}'.format(ens_score))
    print('[fasttext]   score: {0} | label: {1}'.format(str(ft_score), ft_label))
    print('[keras]      score: {0} | label: {1}'.format(str(ks_score), ks_label))
    print('[TextBlob]   score: {0}'.format(s_score))
    print('[tweet]      {0}'.format(tweet))
    '''

    #return jsonify({'score': colors[int(ens_score * 10)], 'tweet': tweet, 'label': ft_label, 'element': elem})
    return jsonify({'score': colors[5], 'tweet': tweet, 'label': 'test', 'element': elem})
'''
if __name__ == '__main__':
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
'''
