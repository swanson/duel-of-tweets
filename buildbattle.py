from mongoengine import *
from db.document import Battle
from datetime import datetime
import sys

connect('tweet-store')
print 'enter tag: '
tag = sys.stdin.readline().strip()
print 'enter choices: '
c = sys.stdin.readline().split(',')
d = {c[0].strip():[], c[1].strip():[]}
b = Battle(tag = tag, start = datetime.now(), suggester = "someone", choices = d, active = True)
b.save()
b = Battle.objects.get(tag = tag)
print b.tag, b.choices
