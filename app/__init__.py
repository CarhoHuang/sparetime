import os
from flask import Flask
from config import config
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'


def create_app(config_name):
    app = Flask(__name__)

    # 设置配置信息
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 初始化相关组件
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # 注册蓝图
    from .auth import auth
    app.register_blueprint(auth.bp)

    from .mission import mission
    app.register_blueprint(mission.bp)

    from .user import user
    app.register_blueprint(user.bp)

    app.app_context()
    return app
