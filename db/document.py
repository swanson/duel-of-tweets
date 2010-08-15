from mongoengine import *
from wtforms import TextField, IntegerField, Form, validators

class BattleForm(Form):
    option1 = TextField("", [validators.Required()])
    option2 = TextField("", [validators.Required()])
    tag = TextField("Tags")
    time_limit = IntegerField("", [validators.Required()])

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
    active = BooleanField(required = True, default = False)

class OutgoingTweet(Document):
    body = StringField(required = True)
    timestamp = DateTimeField()

class Suggestion(Document):
    user = StringField(required = True)
    choices = ListField(StringField(), required = True)
    timestamp = DateTimeField(required = True)

    def __str__(self):
        return '%s vs %s - By @%s' % (self.choices[0], self.choices[1], self.user)


