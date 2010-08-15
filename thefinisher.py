#!/usr/bin/env python

import sys
import logging
import time
from mongoengine import *
from datetime import datetime, timedelta

from db.document import Battle, OutgoingTweet

if __name__ == "__main__":
    # start up the default logging
    logging.basicConfig(level=logging.DEBUG)

    # connect to mongodb
    try:
        connect('tweet-store')
    except:
        logging.critical('couldnt connect to mongodb!')
        sys.exit(-1)
    else:
        logging.info('connected to mongodb')

    while True:
        battles = Battle.objects(active = True)

        for battle in battles:
            if (battle.end - datetime.now()) <= timedelta(seconds=0):
                logging.info("battle '%s' ended!" % battle)

                battle.active = False
                battle.save()

                # find the winner
                max_votes = 0
                max_choice = None
                total_votes = 0
                for choice, voters in battle.choices.items():
                    num_votes = len(voters)
                    total_votes += num_votes
                    if num_votes > max_votes:
                        max_votes = len(voters)
                        max_choice = choice

                # announce results to frontend
                OutgoingTweet(
                    body="The results are in! \"%s\" won with %d votes out of %d" % (
                        max_choice,
                        max_votes,
                        total_votes
                    ),
                    bot = False,
                ).save()

                # announce results to voters
                for choice, voters in battle.choices.items():
                    num_votes = len(voters)
                    if choice == max_choice:
                        # these are the winners
                        for voter in voters:
                            OutgoingTweet(
                                body="@%s Congrats! Your pick, \"%s\", won with %d/%d votes! Follow @DuelOfTweets to find out about more duels!" % (
                                    voter,
                                    choice,
                                    num_votes,
                                    total_votes
                                ),
                                bot = True,
                            ).save()
                    else:
                        # these are the losers
                        for voter in voters:
                            OutgoingTweet(
                                body="@%s Sorry! Your pick, \"%s\", lost with %d/%d votes! Follow @DuelOfTweets to find out about more duels!" % (
                                    voter,
                                    choice,
                                    num_votes,
                                    total_votes
                                ),
                                bot = True,
                            ).save()

        
        time.sleep(1)

