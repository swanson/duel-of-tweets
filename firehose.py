#!/usr/bin/env python
from mongoengine import *
import tweetstream
from datetime import datetime

class TweetStore(Document):
    user = StringField(required = True)
    body = StringField(required = True)
    timestamp = DateTimeField()

connect('testing')
words = ["@showoftweets", "beiber"]
stream = tweetstream.TrackStream("battleoftweets", "secretpass", words)
for tweet in stream:
    print "Storing tweet %s" % tweet['text']
    ts  = TweetStore(body = tweet['text'], user = tweet['user']['screen_name'], timestamp = datetime.now())
    ts.save()

