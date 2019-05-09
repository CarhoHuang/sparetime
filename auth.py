import random
import smtplib
import pymysql
import auth_token
from datetime import datetime
from email.header import Header
from email.mime.text import MIMEText
from flask import (
    Blueprint, g, request, session, jsonify, abort
)
from werkzeug.security import check_password_hash, generate_password_hash
from dbconfig import *

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST' and request.form['request_type'] == 'sign_up':
        email = request.form['email']
        username = request.form['nickname']
        password1 = request.form['password1']
        password2 = request.form['password2']
        verification_code = request.form['verification_code']
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
            error = 'Password mismatch.'
        elif not email:
            error = 'Email is required.'
        elif len(password1) < 8:
            error = 'password is less than 8.'
        elif str(email).find('@stu.edu.cn') == 0:
            error = 'Not STU email.'

        if cur.execute('select * from users where email = %s', (email,)) > 0:
            error = 'User is existed.'

        if cur.execute('select * from verification_code where email = %s', (email,)) > 0:
            v_codes = cur.fetchall()
            time_code = v_codes[len(v_codes) - 1][2]  # 取最后一条记录的时间，再转为datetime
            time_now = datetime.now()

            real_v_code = ''
            if (time_now - time_code).total_seconds() <= 15 * 60:  # 时间少于15分钟才算
                real_v_code = str(v_codes[len(v_codes) - 1][1])
            print('用户v_code：' + verification_code)
            print('数据库v_code：' + real_v_code)
            if verification_code != real_v_code:
                error = '验证码不正确！'
        else:
            error = '还没有发送验证码！'

        if error is None:
            cur.execute(
                'insert into users (nickname,hash_pw,email) values (%s,%s,%s)',
                (username, generate_password_hash(password1), email,)
            )
            db.commit()
            # disconnect mysql
            db.close()
            return jsonify(status='success')
        return jsonify(status='error', error=error)
    elif request.method == 'POST' and request.form['request_type'] == 'send_verification_code':  # 验证码
        email = request.form['email']

        # 查是否重复注册，打开数据库连接
        db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
        # 使用 cursor() 方法创建一个游标对象 cursor
        cur = db.cursor()
        error = None
        if cur.execute('select * from users where email = %s', (email,)) > 0:
            error = 'User is existed.'

        if error is None:
            # 第三方 SMTP 服务
            mail_host = "smtp.qq.com"  # 设置服务器
            mail_user = "1542029827@qq.com"  # 用户名
            mail_pass = "hqzfpfsukqvifgdf"  # 口令

            sender = '1542029827@qq.com'
            receivers = [email]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
            verification_code = random.randint(1000, 9999)

            message = MIMEText('你的验证码为：' + verification_code.__str__() + '。请不要把验证码泄露给其他人！15分钟内有效。 【汕大顺手邦】',
                               'plain', 'utf-8')
            message['From'] = Header('汕大顺手邦', 'utf-8')
            message['To'] = Header(receivers[0], 'utf-8')
            message['Subject'] = Header('【汕大顺手邦】验证码', 'utf-8')

            try:
                smtp_obj = smtplib.SMTP()
                smtp_obj.connect(mail_host, 25)
                smtp_obj.login(mail_user, mail_pass)
                smtp_obj.sendmail(sender, receivers, message.as_string())
                cur.execute('insert into verification_code (email, verification_code) values (%s,%s)',
                            (email, verification_code,))
                db.commit()
                # disconnect mysql
                db.close()
                return jsonify(status='success')
            except smtplib.SMTPException:
                return jsonify(status='error', error='send email fail!')
        else:
            db.commit()
            # disconnect mysql
            db.close()
            return jsonify(status='error', error=error)
    return jsonify(status='error', error='other error')  # 两种请求之外的其他情况


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

            user_info = {"nickname": user[3], "signature": user[5],
                         "avatar_url": user[6], "gender": user[1],
                         "phone": user[4], "email": user[2]}

            return jsonify({"success": 1, "data": user_info})
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
