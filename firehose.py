#!/usr/bin/env python
from mongoengine import *
import tweetstream
from datetime import datetime
from db.document import StoredTweet

connect('tweet-store')
words = ["@showoftweets"]
stream = tweetstream.TrackStream("battleoftweets", "secretpass", words)
for tweet in stream:
    print "Storing tweet %s" % tweet['text']
    ts  = StoredTweet(body = tweet['text'], user = tweet['user']['screen_name'], timestamp = datetime.now())
    ts.save()

