from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from JobManager.__init__ import db, login_manager, app
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text)
    experience = db.Column(db.Text)
    picture = db.Column(db.Text)
    jobs = db.relationship('Job', backref='author', lazy=True)

    def __repr__(self):
        return f"{self.username}"


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    job_content = db.Column(db.Text, nullable=False)
    job_experience = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False)
    tag = db.Column(db.Text)
    website = db.Column(db.Text)
    close = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Job('{self.title}', '{self.date_posted}')"



