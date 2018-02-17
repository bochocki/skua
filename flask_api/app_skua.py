#!flask/bin/python
import colorlover as cl
from flask import Flask, jsonify, redirect
from flask import abort
from flask import make_response
from flask import request
from flask_api import app
import fasttext as ft
import numpy as np
import os
import pickle
import psycopg2
import re
from tensorflow.python import keras
from textblob import TextBlob

# color management
reds = cl.scales['5']['seq']['Reds']
whites = ['rgb(255, 255, 255)'] * 6
colors = whites + reds

# LOAD MODELS
# fasttext
ft_model = ft.load_model('./flask_api/model.bin')

# keras
ks_tokenizer = pickle.load( open( "./flask_api/keras_tokenizer.p", "rb" ) )
ks_classes = pickle.load( open( "./flask_api/keras_classes.p", "rb"))
ks_model = keras.models.load_model("./flask_api/keras_model.ks", custom_objects=None, compile=True)
ks_model.predict(np.array(ks_tokenizer.texts_to_matrix(['hack'])))


def preprocess(tweet):
    # define some useful regex
    mention_regex = r'@[\w\-]+'
    url_regex = (r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
                '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
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


# get environmental variable from virtual environment
def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


@app.route('/')
@app.route('/index')
def index():
   return redirect('https://chrome.google.com/webstore/detail/skua/fjdnggpcpbcfndlmoinkhnbpcjhaednl', code=302)


@app.route('/SkuaLogging', methods=['GET'])
def log_tweet():

    tweet = request.args.get('tweet')
    userid = request.args.get('userid')
    tweeterid = request.args.get('tweeterid')
    tweetid = request.args.get('tweetid')
    troll = request.args.get('troll')

    print(troll)
    print(tweet)
    print(userid)

    psql_user = get_env_variable("POSTGRES_USERNAME")
    psql_pass = get_env_variable("POSTGRES_PASSWORD")
    psql_db   = 'tweets'

    con = None
    con = psycopg2.connect(database = psql_db,
                           user = psql_user,
                           password = psql_pass)
    cur = con.cursor()

    # add to the database
    #cur.execute("INSERT INTO labeled_tweets (original, label) VALUES (%s, %s)", (tweet, troll))
    cur.execute("INSERT INTO user_labels (tweet_text, tweet_id, tweeter_id, user_id, label) VALUES (%s, %s, %s, %s, %s)",
                (tweet, tweetid, tweeterid, userid, troll)
                )
    con.commit()

    # close the connections
    cur.close()
    con.close()

    response = jsonify({'tweet': tweet, 'troll': troll})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/CleverBird', methods=['GET'])
def predict_abuse():

    elem  = request.args.get('element')
    tweet = request.args.get('tweet')

    print(tweet)
    tweet = preprocess(request.args.get('tweet'))

    # classifiers
    ft_score, ft_label = fasttext_estimator(ft_model, tweet)
    ks_score, ks_label = keras_estimator(ks_tokenizer, ks_classes, tweet)
    s_score = sentiment_estimator(tweet)

    ens_score = np.mean([ft_score, ks_score, s_score])

    print('\n[enseble]    score: {0}'.format(ens_score))
    print('[fasttext]   score: {0} | label: {1}'.format(str(ft_score), ft_label))
    print('[keras]      score: {0} | label: {1}'.format(str(ks_score), ks_label))
    print('[TextBlob]   score: {0}'.format(s_score))
    print('[tweet]      {0}'.format(tweet))

    response = jsonify({'score': int(ens_score * 100), 'color': colors[int(ens_score * 10)], 'tweet': tweet, 'element': elem})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
