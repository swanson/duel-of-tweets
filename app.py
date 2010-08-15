from flask import Flask, g, session, request, render_template, flash, redirect, url_for, jsonify
from mongoengine import *
from datetime import datetime, timedelta
import json
from db.document import *

app = Flask(__name__)
app.debug = True
app.secret_key = 'very_secret_key'

@app.template_filter()
def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.now()
    diff = now - dt
    
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:        
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/suggestions/')
def suggestions():
    return render_template('suggestions.html', suggestions = Suggestion.objects)

@app.route('/create/<id>/', methods = ["GET"])
def create_from_suggestion(id):
    s = Suggestion.objects.get(id = id)
    form = BattleForm(option1 = s.choices[0], option2 = s.choices[1], submitter = s.user)
    return render_template('create.html', form=form)

@app.route('/create/')
def create():
    form = BattleForm()
    return render_template('create.html', form=form)

@app.route('/results/')
def results():
    battles = Battle.objects
    return render_template('results.html', battles = battles)

@app.route('/results/<id>/')
def result_details(id):
    battle = Battle.objects.get(id = id)
    return render_template('result_details.html', battle = battle)

@app.route('/status/')
def status():
    return "status"

@app.route('/posts/duel/', methods = ['POST'])
def post_duel():
    form = BattleForm(request.form)
    print form.option1.data, form.option2.data, form.tags.data, form.time_limit.data
    if form.validate():
        c = {form.option1.data.strip():[], form.option2.data.strip():[]}
        n = datetime.now()
        b = Battle(tag = form.tags.data, start = n, end = n + timedelta(minutes=form.time_limit.data), \
                suggester = "someone", choices = c, active = True)
        b.save()
        o = OutgoingTweet(body = "A new duel! %s vs %s - @reply me with the tag %s and your vote!" % \
                (form.option1.data, form.option2.data, form.tags.data))
        o.save()
        
        return redirect('/results/%s' % b.id)
    return "invalid"

if __name__ == '__main__':
    connect('tweet-store')
    app.run(host='0.0.0.0', port=8000)
