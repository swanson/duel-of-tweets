import tweetstream
import getpass

words = ["showoftweets", "@showoftweets"]
stream = tweetstream.TrackStream("_swanson", getpass.getpass(), words)
for tweet in stream:
    print "Got interesting tweet:", tweet['text']

