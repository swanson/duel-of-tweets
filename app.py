from flask import Flask, g, session, request, render_template, flash, redirect, url_for, jsonify
from mongoengine import *
from datetime import datetime
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

@app.route('/create/')
def create():
    return render_template('create.html')

@app.route('/results/')
def results():
    battles = Battle.objects
    return render_template('results.html', battles = battles)

@app.route('/results/<id>')
def result_details(id):
    return "results for %s" % id

@app.route('/status/')
def status():
    return "status"

@app.route('/posts/duel/', methods = ['POST'])
def post_duel():
    return "post duel"
    comment_form = CommentForm(request.form)
    if g.user and comment_form.validate():
        question = Question.objects.get(id = id)
        new_comment = Comment(body = comment_form.comment_body.data, author = g.user)
        new_comment.save()
        question.comments.append(new_comment)
        question.save()
        return redirect('/questions/%s' % id) #avoid double POSTs
    else:
        #add error handling
        return redirect('/questions/%s' % id) #avoid double POSTs

if __name__ == '__main__':
    connect('tweet-store')
    app.run(host='0.0.0.0', port=8000)
