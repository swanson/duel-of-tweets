#!/usr/bin/env python

import tweetstream
import getpass

words = ["@showoftweets"]
stream = tweetstream.TrackStream("battleoftweets", "secretpass", words)
for tweet in stream:
    print "Got interesting tweet:", tweet['text']

