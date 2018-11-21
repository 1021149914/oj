from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin,db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    useremail = db.Column(db.String(120), index=True, unique=True)
    userpassword = db.Column(db.String(128))
    userp=db.Column(db.Integer)
    commits = db.relationship('Commit', backref='author', lazy='dynamic')

    def set_password(self,password):
        self.userpassword=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.userpassword,password)

    @property
    def id(self):
        return self.userid

    def __repr__(self):
        return '<User {}>'.format(self.username)  

class Problem(db.Model):
    problemid=db.Column(db.Integer,primary_key=True)
    problemms=db.Column(db.Integer)
    problemkb=db.Column(db.Integer)

    def __repr__(self):
        return '<Problem {}>'.format(self.problemid) 

class Contest(db.Model):
    contestid=db.Column(db.Integer,primary_key=True)
    contestbegin=db.Column(db.DateTime)
    contestlen=db.Column(db.Integer)

    def __repr__(self):
        return '<Contest {}>'.format(self.contestid)   

class Info(db.Model):
    Infoid=db.Column(db.Integer,primary_key=True)
    Infotitle=db.Column(db.String(128))

    def __repr__(self):
        return '<Info {}>'.format(self.Infoid)  

class Commit(db.Model):
    commitid=db.Column(db.Integer,primary_key=True)
    userid=db.Column(db.Integer,db.ForeignKey('user.userid'))
    problemid=db.Column(db.Integer,db.ForeignKey('problem.problemid'))
    committime=db.Column(db.DateTime,index=True,default=datetime.utcnow)
    commitans=db.Column(db.String(64))
    commitms=db.Column(db.Integer)
    commitkb=db.Column(db.Integer)

    def __repr__(self):
        return '<Commit {}>'.format(self.commitid)  

