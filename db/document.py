from mongoengine import *


class StoredTweet(Document):
    user = StringField(required = True)
    body = StringField(required = True)
    timestamp = DateTimeField()

class Battle(Document):
    tag = StringField(required = True, unique = True)
    start = DateTimeField(required = True)
    end = DateTimeField()
    suggester = StringField(required = True)
    choices = DictField()

class OutgoingTweet(Document):
    body = StringField(required = True)
    timestamp = DateTimeField()

