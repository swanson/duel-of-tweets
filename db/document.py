from mongoengine import *
from wtforms import TextField, IntegerField, Form, validators

class BattleForm(Form):
    option1 = TextField("", [validators.Required()])
    option2 = TextField("", [validators.Required()])
    tags = TextField("Tags")
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

    def __str__(self):
        c = []
        v = []
        print self.choices
        for choice in self.choices:
            c.append(choice)
            v.append(len(self.choices[choice]))
        return 'Duel %s: %s (%s) vs %s (%s)' % (self.tag, c[0], v[0], c[1], v[1]) 

class OutgoingTweet(Document):
    body = StringField(required = True)
    timestamp = DateTimeField()

class Suggestion(Document):
    user = StringField(required = True)
    choices = ListField(StringField(), required = True)
    timestamp = DateTimeField(required = True)

    def __str__(self):
        return '%s vs %s - By @%s' % (self.choices[0], self.choices[1], self.user)


