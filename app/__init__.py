from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from config import config

mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'


def create_app(config_name):
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('mail/base_email.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('mail/base_email.html'), 404

    @app.errorhandler(403)
    def page_not_found(e):
        return render_template('mail/base_email.html'), 403

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('mail/base_email.html'), 500

    @app.errorhandler(502)
    def internal_server_error(e):
        return render_template('mail/base_email.html'), 502

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
