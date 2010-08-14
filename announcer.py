#!/usr/bin/env python

import logging
import tweepy


class Announcer(object):
    DEFAULT_RETRY_COUNT = 5
    DEFAULT_RETRY_DELAY = 0.1

    def __init__(self, username, password,
            retry_count=DEFAULT_RETRY_COUNT, retry_delay=DEFAULT_RETRY_DELAY):


        logging.info("inside Announcer __init__")
        
        # switch to oauth after 2010-08-16!
        self.auth = tweepy.BasicAuthHandler(username, password)
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

    announcer = Announcer("battleoftweets", "secretpass")
    status = announcer.tweet("hello, world!")
    print status

