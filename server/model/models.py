# models.py
from datetime import datetime

from flask_login import UserMixin
from server import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    neutal_cnt = db.Column(db.Integer)
    happy_cnt = db.Column(db.Integer)
    sad_cnt = db.Column(db.Integer)
    hate_cnt = db.Column(db.Integer)
    anger_cnt = db.Column(db.Integer)


class SampleSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    summary_id = db.Column(db.Integer, db.ForeignKey('summary.id'))
    neutral = db.Column(db.Float)
    happy = db.Column(db.Float)
    sad = db.Column(db.Float)
    hate = db.Column(db.Float)
    anger = db.Column(db.Float)