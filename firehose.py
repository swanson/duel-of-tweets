#!/usr/bin/env python
from mongoengine import *
import tweetstream
from datetime import datetime

class StoredTweet(Document):
    user = StringField(required = True)
    body = StringField(required = True)
    timestamp = DateTimeField()

connect('tweet-store')
words = ["@showoftweets", "bieber"]
stream = tweetstream.TrackStream("battleoftweets", "secretpass", words)
for tweet in stream:
    print "Storing tweet %s" % tweet['text']
    ts  = StoredTweet(body = tweet['text'], user = tweet['user']['screen_name'], timestamp = datetime.now())
    ts.save()

