import random
import smtplib
from datetime import datetime

import jwt
from flask import (request, jsonify, current_app)
from flask_login import current_user, login_user
from . import bp
from .. import db
from ..email import EmailSender
from ..models import User, VCode


@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST' and request.form['request_type'] == 'sign_up':
        email = request.form['email']
        username = request.form['nickname']
        password1 = request.form['password1']
        password2 = request.form['password2']
        verification_code = request.form['verification_code']
        error = None

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

        if len(User.query.filter_by(email=email).all()) > 0:
            error = 'User is existed.'

        if len(VCode.query.filter_by(email=email).all()) > 0:
            v_codes = VCode.query.filter_by(email=email).all()
            time_code = v_codes[len(v_codes) - 1].time  # 取最后一条记录的时间，再转为datetime
            time_now = datetime.now()

            real_v_code = ''
            delta_time = (time_now - time_code).total_seconds()
            if delta_time <= 15 * 60:  # 时间少于15分钟才算
                real_v_code = v_codes[len(v_codes) - 1].verification_code
            real_v_code = str(v_codes[len(v_codes) - 1].verification_code)
            print('用户v_code：' + verification_code)
            print('数据库v_code：' + real_v_code)
            if verification_code != real_v_code:
                error = '验证码不正确！'
        else:
            error = '还没有发送验证码！'

        if error is None:
            e_sender = EmailSender()
            e_sender.send_picture_mail(to=email, subject='注册成功', template='mail/sign_up_success', username=username)
            user = User(nickname=username, password=password1, email=email)
            db.session.add(user)
            return jsonify(status='success')
        return jsonify(status='error', error=error)
    elif request.method == 'POST' and request.form['request_type'] == 'send_verification_code':  # 验证码
        email = request.form['email']

        # 查是否重复注册
        error = None
        if len(User.query.filter_by(email=email).all()) > 0:
            error = 'User is existed.'
        if error is None:
            verification_code = random.randint(1000, 9999)
            e_sender = EmailSender()
            try:
                e_sender.send_picture_mail(to=email, subject='注册验证码', template='mail/sign_up',
                                           verification_code=verification_code)
                vcode = VCode(email=email, verification_code=verification_code)
                db.session.add(vcode)
                return jsonify(status='success')
            except smtplib.SMTPException:
                return jsonify(status='error', error='send email fail!')
        else:
            return jsonify(status='error', error=error)
    return jsonify(status='error', error='other error')  # 两种请求之外的其他情况


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        global pw_hash

        error = None
        # 打开数据库获取一个用户
        user = User.query.filter_by(email=email).first()

        if user is None:
            error = 'Incorrect email.'
        elif not user.verify_password(password):
            error = 'Incorrect password.'

        if error is None:
            key = current_app.config['SECRET_KEY']
            now_second = int((datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0)).total_seconds())
            second_of_20_days = 1728000
            auth_token = jwt.encode({'user_id': user.user_id, 'exp': now_second + second_of_20_days}, key,
                                    algorithm='HS256')  # 得到的为bytes
            # 打开数据库连接，把生成的token写入数据库
            user.auth_token = str(auth_token)
            db.session.add(user)
            login_user(user)
            user_info = {"user_id": user.user_id, "nickname": user.nickname, "signature": user.signature,
                         "avatar_url": user.avatar_url, "gender": user.gender,
                         "phone": user.phone, "email": user.email,
                         'auth_token': user.auth_token, 'bg_url': user.bg_url, 'favourable_rate': user.favor_rate,
                         'money': user.money}
            return jsonify({"status": 'success', "data": user_info})
        return jsonify(status='error', error=error)
    return jsonify(status='error', error='other error')


@bp.route('/is_token_invalid', methods=['GET', 'POST'])
def is_token_invalid():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
        except:
            return jsonify(status='error', error='Data obtain failure')

        # 通过token获取用户
        try:
            key = current_app.config['SECRET_KEY']
            user_json = jwt.decode(auth_token, key, algorithms=['HS256'])
        except:
            return jsonify(status='error', error='decode failed')
        # 判断该token是否跟解析出来的用户token一致
        user_id = user_json.get('user_id')
        user = User.query.filter_by(user_id=user_id).first()

        # 验证token是否一致，不一致就return
        if str(request.form['auth_token']) != user.auth_token:
            return jsonify(status='error', error='Authenticate failed')

        return jsonify({'status': "success"})
    return jsonify({'status': "error", 'error': 'error method'})


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
