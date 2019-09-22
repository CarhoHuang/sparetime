from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


# 定义模型
class Mission(db.Model):
    __tablename__ = 'mission'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    content = db.Column(db.String(100))
    picture_url_1 = db.Column(db.String(100), unique=True, default='')
    picture_url_2 = db.Column(db.String(100), unique=True, default='')
    picture_url_3 = db.Column(db.String(100), unique=True, default='')
    origin = db.Column(db.String(100), default='')
    destination = db.Column(db.String(100), default='')
    like_number = db.Column(db.Integer)
    comment_number = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_deleted = db.Column(db.Integer, default=0)
    end_time = db.Column(db.DateTime)
    money = db.Column(db.Float)
    evaluate = db.Column(db.Integer)
    receiver_id = db.Column(db.Integer)
    release_time = db.Column(db.DateTime, default=datetime.now())
    is_received = db.Column(db.Integer, default=1)

    def __repr__(self):
        return '<Role %r>' % self.content


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gender = db.Column(db.String(100), default='男')
    email = db.Column(db.String(100), unique=True, index=True, default='')
    nickname = db.Column(db.String(100), unique=True, index=True)
    phone = db.Column(db.String(100), unique=True, index=True, default='')
    signature = db.Column(db.String(100), default='')
    avatar_url = db.Column(db.String(100), unique=True, default='')
    hash_pw = db.Column(db.String(128), unique=True)
    wechat = db.Column(db.String(100), unique=True)
    favor_rate = db.Column(db.Float, default=1.0)
    time = db.Column(db.DateTime, default=datetime.now())
    role = db.Column(db.String(10), default='user')
    auth_token = db.Column(db.String(200))
    bg_url = db.Column(db.String(200))

    missions = db.relationship('Mission', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.hash_pw = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hash_pw, password)

    def __repr__(self):
        return '<User %r>' % self.nickname


class VCode(db.Model):
    __tablename__ = 'verification_code'
    email = db.Column(db.String(100), unique=True, index=True, default='')
    verification_code = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now())
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)

    def __repr__(self):
        return '<VCode %r>' % self.verification_code


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
