#!/usr/bin/env python

import sys
import logging
import time
from mongoengine import *
from datetime import datetime, timedelta

from db.document import Battle

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

    b = Battle(
        tag = '#dot23',
        start = datetime.now(),
        end = datetime.now() + timedelta(minutes=1),
        suggester = 'jevinskie',
        choices = {'beiber' : [], 'lohan' : []},
        active = True
    )
    b.save()

