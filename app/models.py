from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


# 定义模型
class Mission(db.Model):
    __tablename__ = 'missions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    content = db.Column(db.String(1000))
    picture_url_1 = db.Column(db.String(100), default='')
    picture_url_2 = db.Column(db.String(100), default='')
    picture_url_3 = db.Column(db.String(100), default='')
    origin = db.Column(db.String(100), default='')
    destination = db.Column(db.String(100), default='')
    like_number = db.Column(db.Integer, default=0)
    comment_number = db.Column(db.Integer, default=0)
    is_deleted = db.Column(db.Integer, default=0)
    end_time = db.Column(db.DateTime)
    money = db.Column(db.Float)
    evaluate = db.Column(db.Integer)
    receiver_id = db.Column(db.Integer)
    release_time = db.Column(db.DateTime, default=datetime.now)
    is_received = db.Column(db.Integer, default=0)

    # 生成虚拟帖子
    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Mission(content=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                        release_time=forgery_py.date.date(True),
                        user=u)
            db.session.add(p)
            db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.content


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gender = db.Column(db.String(100), default='男')
    email = db.Column(db.String(100), unique=True, index=True)
    nickname = db.Column(db.String(100), unique=True, index=True)
    phone = db.Column(db.String(100), index=True, default='')
    signature = db.Column(db.String(100), default='')
    avatar_url = db.Column(db.String(100), default='')
    hash_pw = db.Column(db.String(128), default='')
    wechat = db.Column(db.String(100), default='')
    favor_rate = db.Column(db.Integer, default=100)
    time = db.Column(db.DateTime, default=datetime.now)
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

    # 生成虚拟用户
    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     nickname=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     time=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<User %r>' % self.nickname


class VCode(db.Model):
    __tablename__ = 'verification_codes'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(100), index=True, default='')
    verification_code = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<VCode %r>' % self.verification_code


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
