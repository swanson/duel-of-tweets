#!/usr/bin/env python
import re

#remove mentions
#grab hashtags
#look for commands

class Command(object):
    def __init__(self, cmd_type, target, body = None, tag = None):
        self.cmd_type = cmd_type
        self.target = target
        self.body = body
        self.tag = tag

    def to_tweet_string(self):
        mention = '@%s' % self.target
        if self.cmd_type == 'results':
            template = "%s Current results for %s: %s" % (mention, tag, body)
        elif self.cmd_type == 'remove':
            template = "%s Your vote for %s has been removed" % (mention, tag)
        elif self.cmd_type == 'suggest':
            template = "%s thanks for the suggestion!" % (mention)
        else:
            template = "%s we received your vote for %s" % (mention, body)
        if len(template < 140):
            return template
        else:
            raise Exception("Too long too tweet")

class Worker(object):
    def __init__(self, command):
        self.command = command

    def do_work(self):
        if self.command.cmd_type == 'results':
            self.command.body = 'Coke 51, Pepsi 49'
            print 'sending results'
            #query for results
        elif self.command.cmd_type == 'remove':
            print 'removing %s\'s vote' % self.command.target
            #remove vote
        elif self.command.cmd_type == 'suggest':
            print 'adding suggestion', self.command.body
            #create suggested battle
        else:
            #vote?
            #difflib stuff
            print 'adding vote for %s\'s vote for %s' % (self.command.target, self.command.body)

    def finalize(self):
        pass

class Decoder(object):
    def __init__(self, raw_tweet):
        self.tweet = raw_tweet.body
        self.target = raw_tweet.user
        self._decode()

    def _decode(self):
        self.remove_mentions(self.tweet)
        tags = self.get_hashtags(self.tweet)
        valid_tags = []
        for tag in tags:
            if self.validate_hashtag_format(tag):
                valid_tags.append(tag)
        is_cmd, cmd = self.check_for_commands(self.tweet)
        self.remove_hashtags(self.tweet)
        if not is_cmd:
            cmd = 'vote'

        c = Command(cmd, self.target, self.tweet, valid_tags)

    def remove_mentions(self, tweet):
        self.tweet = re.sub('@[\S]+', '', tweet).strip()

    def remove_hashtags(self, tweet):
        self.tweet = re.sub('#[\S]+', '', tweet).strip()
    
    def get_hashtags(self, tweet):
        tags = re.findall('#[\S]+', tweet)
        return tags
    
    def validate_hashtag_format(self, tag):
        valid = re.findall('#SOT[0-9]+', tag, re.I)
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
                break
        return is_command, command

if __name__ == '__main__':
    print 'sup'
