from mongoengine import *


class StoredTweet(Document):
    user = StringField(required = True)
    body = StringField(required = True)
    timestamp = DateTimeField()

class OutgoingTweet(Document):
    body = StringField(required = True)
    timestamp = DateTimeField()

