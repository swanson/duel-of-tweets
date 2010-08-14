#!/usr/bin/env python
from mongoengine import *
import tweetstream
from datetime import datetime
from db.document import StoredTweet

import sys
import json
import logging

if __name__ == "__main__":
    # start up the default logging
    logging.basicConfig(level=logging.DEBUG)

    # get the config
    try:
        with open('config.json') as cfg:
            config = json.load(cfg)
    except:
        logging.critical('couldnt open config!')
        sys.exit(-1)

    # connect to mongodb
    try:
        connect('tweet-store')
    except:
        logging.critical('couldnt connect to mongodb!')
        sys.exit(-1)
    else:
        logging.info('connected to mongodb')

    words = ["@showoftweets"]
    stream = tweetstream.TrackStream(config['user'], config['password'], words)

    for tweet in stream:
        logging.debug("Storing tweet %s" % tweet['text'])
        ts  = StoredTweet(body = tweet['text'], user = tweet['user']['screen_name'], timestamp = datetime.now())
        ts.save()

