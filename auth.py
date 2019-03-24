import functools, pymysql
from flask import (
    Blueprint, flash, g, request, session, url_for, json, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from dbconfig import *

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return "login_error"
        return view(**kwargs)

    return wrapped_view


@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['nickname']
        password1 = request.form['password1']
        password2 = request.form['password2']
        error = None

        # 打开数据库连接
        db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
        # 使用 cursor() 方法创建一个游标对象 cursor
        cur = db.cursor()

        if not username:
            error = 'Username is required.'
        elif not password1:
            error = 'Password is required.'
        elif not password2:
            error = 'Password is required.'
        elif password1 != password2:
            error = 'Password mismatch！'
        elif not email:
            error = 'Email is required.'

        if cur.execute('select * from users where email = %s', (email,)) > 0:
            error = 'User is existed.'

        if error is None:
            cur.execute(
                'insert into users (nickname,hash_pw,email) values (%s,%s,%s)',
                (username, generate_password_hash(password1), email,)
            )
            db.commit()
            # disconnect mysql
            db.close()
            return jsonify(success=True)
        return jsonify(error=error)

    return jsonify(stages='success')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        global pw_hash

        error = None
        # 打开数据库连接
        db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
        cur = db.cursor()
        cur.execute(
            'SELECT * FROM users WHERE email = %s', (email,)
        )
        user = cur.fetchone()
        db.close()
        if user is not None:
            pw_hash = user[7]

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(pw_hash, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['email'] = user[2]  # the third column

            json_data = {"nickname": user[3], "signature": user[5],
                          "avatar_url": user[6], "gender": user[1],
                          "phone": user[4], "email": user[2]}

            return jsonify({"success": 1, "data": json_data})

        return jsonify(error=error)

    return 1


@bp.route('/logout')
def logout():
    session.clear()
    return 1


# 已经登陆
@bp.before_app_request
def load_logged_in_user():
    if 'email' not in session:
        g.user = None
    else:
        # 打开数据库连接
        db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
        cur = db.cursor()
        cur.execute(
            'select * from users where email = %s', session['email']
        )
        g.user = cur.fetchone()
        db.close()
