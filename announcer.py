#!/usr/bin/env python

import logging
import tweepy
from db.document import OutgoingTweet
from mongoengine import *
import sys
import time
import json

class Announcer(object):
    DEFAULT_RETRY_COUNT = 5
    DEFAULT_RETRY_DELAY = 0.1

    def __init__(self, consumer_key, consumer_secret, access_key, access_secret,
            retry_count=DEFAULT_RETRY_COUNT,
            retry_delay=DEFAULT_RETRY_DELAY):


        logging.info("inside Announcer __init__")
        
        # switch to oauth after 2010-08-16!
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(
            self.auth,
            retry_count=retry_count,
            retry_delay=retry_delay
        )

        logging.info("finished Announcer __init__")

        return



    def tweet(self, body):
        """Trys to send the specified tweet. Returns True on success, False
        on failure."""

        try:
            status = self.api.update_status(body)
        except tweepy.TweepError:
            logging.warning("failed to send tweet \"%s\"" % body)
            return False
        else:
            logging.debug("sent tweet \"%s\"" % body)
            return True


        
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

    announcer = Announcer(config['consumer_key'], config['consumer_secret'],
        config['access_key'], config['access_secret'])


    # connect to mongodb
    try:
        connect('tweet-store')
    except:
        logging.critical('couldnt connect to mongodb!')
        sys.exit(-1)
    else:
        logging.info('connected to mongodb')

    while True:
        # due to the default IDs containing a timestamp, this will get
        # the oldest tweets first
        tweet = OutgoingTweet.objects.first()
        if tweet is not None:
            # found a tweet, try and send it
            if not announcer.tweet(tweet.body):
                logging.debug('failed to tweet!')
            # found tweet, sent it, so get rid of it
            tweet.delete()
        # dont piss of twitter, throttle
        time.sleep(1)
    
