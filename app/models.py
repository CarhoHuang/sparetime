from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from . import login_manager
from datetime import datetime


# 定义模型

class MissionComment(db.Model):
    __tablename__ = 'mission_comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('missions.id'))

    def __repr__(self):
        return '<MissionComment %r>' % self.content


class SearchThing(db.Model):
    __tablename__ = 'search_things'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    content = db.Column(db.Text)
    picture_url_1 = db.Column(db.String(100), default='')
    picture_url_2 = db.Column(db.String(100), default='')
    picture_url_3 = db.Column(db.String(100), default='')
    like_number = db.Column(db.Integer, default=0)
    comment_number = db.Column(db.Integer, default=0)
    is_deleted = db.Column(db.Integer, default=0)
    is_solved = db.Column(db.Integer, default=0)
    release_time = db.Column(db.DateTime, default=datetime.now)

    # 生成虚拟帖子
    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = SearchThing(content=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                            release_time=forgery_py.date.date(True),
                            user=u)
            db.session.add(p)
            db.session.commit()

    def __repr__(self):
        return '<SearchThing %r>' % self.content


class Study(db.Model):
    __tablename__ = 'studies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    content = db.Column(db.Text)
    picture_url_1 = db.Column(db.String(100), default='')
    picture_url_2 = db.Column(db.String(100), default='')
    picture_url_3 = db.Column(db.String(100), default='')
    like_number = db.Column(db.Integer, default=0)
    comment_number = db.Column(db.Integer, default=0)
    is_deleted = db.Column(db.Integer, default=0)
    is_solved = db.Column(db.Integer, default=0)
    release_time = db.Column(db.DateTime, default=datetime.now)

    # 生成虚拟帖子
    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Study(content=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                      release_time=forgery_py.date.date(True),
                      user=u)
            db.session.add(p)
            db.session.commit()

    def __repr__(self):
        return '<Study %r>' % self.content


class IdleThing(db.Model):
    __tablename__ = 'idle_things'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    content = db.Column(db.Text)
    picture_url_1 = db.Column(db.String(100), default='')
    picture_url_2 = db.Column(db.String(100), default='')
    picture_url_3 = db.Column(db.String(100), default='')
    like_number = db.Column(db.Integer, default=0)
    comment_number = db.Column(db.Integer, default=0)
    money = db.Column(db.Integer, default=2)
    release_time = db.Column(db.DateTime, default=datetime.now)
    is_deleted = db.Column(db.Integer, default=0)
    is_finished = db.Column(db.Integer, default=0)

    # 生成虚拟帖子
    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = IdleThing(content=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                          release_time=forgery_py.date.date(True),
                          user=u)
            db.session.add(p)
            db.session.commit()

    def __repr__(self):
        return '<IdleThing %r>' % self.content


class Mission(db.Model):
    __tablename__ = 'missions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    content = db.Column(db.Text)
    picture_url_1 = db.Column(db.String(100), default='')
    picture_url_2 = db.Column(db.String(100), default='')
    picture_url_3 = db.Column(db.String(100), default='')
    origin = db.Column(db.String(100), default='')
    destination = db.Column(db.String(100), default='')
    like_number = db.Column(db.Integer, default=0)
    comment_number = db.Column(db.Integer, default=0)
    end_time = db.Column(db.DateTime)
    money = db.Column(db.Float)
    evaluate = db.Column(db.Integer)
    receiver_id = db.Column(db.Integer)
    release_time = db.Column(db.DateTime, default=datetime.now)
    is_deleted = db.Column(db.Integer, default=0)
    is_received = db.Column(db.Integer, default=0)
    is_finished = db.Column(db.Integer, default=0)

    comments = db.relationship('MissionComment', backref='post', lazy='dynamic')

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
        return '<Mission %r>' % self.content


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }

        # 在数据库中创建角色
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
            db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gender = db.Column(db.String(100), default='男')
    email = db.Column(db.String(100), unique=True, index=True)
    nickname = db.Column(db.String(100), index=True, default='萌新')
    phone = db.Column(db.String(100), index=True, default='')
    signature = db.Column(db.Text, default='')
    avatar_url = db.Column(db.String(100), default='default.png')
    hash_pw = db.Column(db.String(128), default='')
    wechat = db.Column(db.String(100), default='')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    favor_rate = db.Column(db.Integer, default=100)
    time = db.Column(db.DateTime, default=datetime.now)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    auth_token = db.Column(db.String(200))
    bg_url = db.Column(db.String(200))

    missions = db.relationship('Mission', backref='user', lazy='dynamic')
    idle_things = db.relationship('IdleThing', backref='user', lazy='dynamic')
    studies = db.relationship('Study', backref='user', lazy='dynamic')
    search_things = db.relationship('SearchThing', backref='user', lazy='dynamic')

    missions_comments = db.relationship('MissionComment', backref='user', lazy='dynamic')

    def get_id(self):
        try:
            return str(self.user_id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    # 定义默认的用户角色
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['MAIL_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    # 检查用户是否有指定的权限
    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    # 刷新用户最后登录时间
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

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


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
