#!/usr/bin/env python
import re
from db.document import *
from datetime import datetime
from mongoengine import *
import logging
import time
import sys

#remove mentions
#grab hashtags
#look for commands

class Command(object):
    def __init__(self, cmd_type, target, body = None, tag = None):
        self.cmd_type = cmd_type
        self.target = target
        self.body = body
        self.tag = tag
        connect('tweet-store')

    def to_tweet_string(self):
        mention = '@%s' % self.target
        if self.cmd_type == 'results':
            template = "%s Current results for %s: %s" % (mention, self.tag, self.body)
        elif self.cmd_type == 'remove':
            template = "%s Your vote for %s has been removed" % (mention, self.tag)
        elif self.cmd_type == 'suggest':
            template = "%s thanks for the suggestion!" % (mention)
        else:
            template = "%s we received your vote for %s" % (mention, self.body)
        if len(template) < 140:
            return template
        else:
            raise Exception("Too long too tweet")

    def dispatch(self):
        outgoing = OutgoingTweet(body = self.to_tweet_string(), timestamp = datetime.now())
        outgoing.save()

class Worker(object):
    def __init__(self, command):
        self.command = command

    def do_work(self):
        if self.command.cmd_type == 'results':
            battle = Battle.objects.get(tag = self.command.tag)
            res = []
            for b in battle.choices:
                res.append('%s - %s' % (b, len(battle.choices[b])))
            self.command.body = ", ".join(res)
        elif self.command.cmd_type == 'remove':
            battle = Battle.objects.get(tag = self.command.tag)
            for c in battle.choices:
                if self.command.target in battle.choices[c]:
                    battle.choices[c].remove(self.command.target)
                    battle.save()
                    print 'removing %s\'s vote' % self.command.target
                    break
        elif self.command.cmd_type == 'suggest':
            choices = self.command.body.split(' or ')
            if len(choices) != 2:
                logging.warn("suggestion '%s' couldn't be decoded!" % self.command.body)
                return False
            logging.info("adding suggestion '%s' OR '%s'" % (choices[0], choices[1]))
            #create suggested battle
            s = Suggestion()
            s.user = self.command.target
            s.timestamp = datetime.now()
            s.choices = self.command.body.split(' or ')
            s.save()
        else:
            battle = Battle.objects.get(tag = self.command.tag)
            if not battle.active:
                print 'battle has ended, you cannot vote anymore'
                return False
            if self.command.body in battle.choices:
                if self.command.target not in battle.choices[self.command.body]:
                    battle.choices[self.command.body].append(self.command.target)
                    battle.save()
                else:
                    print "already voted"
            print 'adding vote for %s\'s vote for %s' % (self.command.target, self.command.body)
        return True

    def finalize(self):
        pass

class Decoder(object):
    def __init__(self, raw_tweet):
        self.tweet = raw_tweet.body
        print self.tweet
        self.target = raw_tweet.user
        self._decode()

    def _decode(self):
        self.remove_mentions(self.tweet)
        tags = self.get_hashtags(self.tweet)
        poll_tag = None
        for tag in tags:
            if self.validate_hashtag_format(tag):
                poll_tag = tag
                break
        is_cmd, cmd = self.check_for_command(self.tweet)
        self.remove_hashtags(self.tweet)
        if not is_cmd:
            cmd = 'vote'
        
        self.command = Command(cmd, self.target, self.tweet, poll_tag)

    def remove_mentions(self, tweet):
        self.tweet = re.sub('@[\S]+', '', tweet).strip()

    def remove_hashtags(self, tweet):
        self.tweet = re.sub('#[\S]+', '', tweet).strip()
    
    def get_hashtags(self, tweet):
        tags = re.findall('#[\S]+', tweet)
        return tags
    
    def validate_hashtag_format(self, tag):
        valid = re.findall('#BOT[0-9]+', tag, re.I)
        if valid:
            return True
        return False

    def check_for_command(self, tweet):
        is_command = False
        command = None
        for cmd in ['results', 'remove', 'suggest']:
            match = re.findall('%s' % cmd, tweet, re.I)
            if match:
                is_command = True
                command = cmd
                self.tweet = re.sub('%s' % cmd, '', tweet, re.I).strip()
                break
        return is_command, command

if __name__ == '__main__':
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
        #t = StoredTweet.objects.first()
        class Mock():
            def delete(self):
                pass
        t = Mock()
        t.body = '@ShowOfTweets suggest justin beiber or justin timberlake'
        t.user = 'BattleOfTweets'
        if t is not None:
            d = Decoder(t)
            w = Worker(d.command)
            if w.do_work():
                d.command.dispatch()
            t.delete()

        # don't overload mongodb
        time.sleep(0.05)

