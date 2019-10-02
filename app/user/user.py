import os
import random
import smtplib
from datetime import datetime

import jwt
import pymysql
from flask import (
    request, jsonify, current_app
)
from werkzeug.utils import secure_filename

from . import bp
from .. import db
from ..email import EmailSender
from ..models import User, VCode

# 上传图片相关
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# 修改文字资料
@bp.route('/modify_profile', methods=('GET', 'POST'))
def modify_profile():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            nickname = request.form['nickname']
            gender = request.form['gender']
            signature = request.form['signature']
        except:
            return jsonify(status='error', error='Data acquisition failure')

        try:
            phone = request.form['phone']
        except:
            phone = ''
            pass

        # 通过token获取用户
        try:
            key = current_app.config['SECRET_KEY']
            user_json = jwt.decode(auth_token, key, algorithms=['HS256'])
        except:
            return jsonify(status='error', error='auth_token decode failed')
        # 判断该token是否跟解析出来的用户token一致
        user_id = user_json.get('user_id')
        # 打开数据库连接

        user = User.query.filter_by(user_id=user_id).first()
        # 验证token是否一致，不一致就return
        if str(request.form['auth_token']) != user.auth_token:
            return jsonify(status='error', error='token authenticate failed')

        error = None
        if nickname is None:
            error = 'Error nickname'
        if gender is None:
            error = 'Error gender'
        if signature is None:
            error = 'Error signature'

        if error is None:
            # 数据库操作
            user.nickname = nickname
            user.gender = gender
            user.phone = phone
            user.signature = signature
            db.session.add(user)
            return jsonify(status='success')
        return jsonify(status='error', error=error)

    return jsonify(status='error', error='method error')


# 修改头像
@bp.route('/modify_avatar', methods=['GET', 'POST'])
def modify_avatar():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            avatar_file = request.files['avatar']
        except:
            return jsonify(status='error', error='Data acquisition failure')

        # 通过token获取用户
        try:
            key = current_app.config['SECRET_KEY']
            user_json = jwt.decode(auth_token, key, algorithms=['HS256'])
        except:
            return jsonify(status='error', error='token decode failed')
        # 判断该token是否跟解析出来的用户token一致
        user_id = user_json.get('user_id')
        # 打开数据库连接
        user = User.query.filter_by(user_id=user_id).first()
        # 验证token是否一致，不一致就return
        if str(request.form['auth_token']) != user.auth_token:
            return jsonify(status='error', error='token authenticate failed')

        error = None
        if avatar_file is None:
            error = 'Error avatar file'
        # 没有错误就开始处理
        if error is None and allowed_file(avatar_file.filename):
            avatar_name = secure_filename(avatar_file.filename)
            now_second = int((datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0)).total_seconds())
            avatar_name = 'user_id_' + str(user_id) + '_' + str(now_second) + '.' + \
                          avatar_name.rsplit('.', 1)[1].lower()
            avatar_file.save(os.path.join('./app/static/avatar', avatar_name))

            # 打开数据库操作
            user.avatar_url = avatar_name
            db.session.add(user)

            return jsonify(status='success')
        return jsonify(status='error', error=error)
    return jsonify(status='error', error='method error')


# 修改个人背景图片
@bp.route('/modify_personal_bg', methods=['GET', 'POST'])
def modify_personal_bg():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            bg_file = request.files['personal_bg']
        except:
            return jsonify(status='error', error='Data acquisition failure')

        # 通过token获取用户
        try:
            key = current_app.config['SECRET_KEY']
            user_json = jwt.decode(auth_token, key, algorithms=['HS256'])
        except:
            return jsonify(status='error', error='decode failed')
        # 判断该token是否跟解析出来的用户token一致
        user_id = user_json.get('user_id')
        # 打开数据库连接

        user = User.query.filter_by(user_id=user_id).first()
        # 验证token是否一致，不一致就return
        if str(request.form['auth_token']) != user.auth_token:
            return jsonify(status='error', error='token authenticate failed')

        error = None
        if bg_file is None:
            error = 'Error bg file'
        # 没有错误就开始处理
        if error is None and allowed_file(bg_file.filename):
            bg_name = secure_filename(bg_file.filename)
            now_second = int((datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0)).total_seconds())
            bg_name = 'user_id_' + str(user_id) + '_' + str(now_second) + '.' + \
                      bg_name.rsplit('.', 1)[1].lower()
            bg_file.save(os.path.join('''./app/static/personal_background''', bg_name))

            # 打开数据库连接
            user.bg_url = bg_name
            db.session.add(user)
            return jsonify(status='success')
        return jsonify(status='error', error=error)
    return jsonify(status='error', error='method error')  # is not post method


# 修改密码
@bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        if request.form['request_type'] == 'send_verification_code':
            email = request.form['email']

            # 查是否重复注册
            error = None
            if len(User.query.filter_by(email=email).all()) <= 0:
                error = 'User is not existed.'
            if error is None:
                verification_code = random.randint(1000, 9999)
                e_sender = EmailSender()
                try:
                    e_sender.send_picture_mail(to=email, subject='忘记密码验证码', template='mail/sign_up',
                                               verification_code=verification_code)
                    vcode = VCode(email=email, verification_code=verification_code)
                    db.session.add(vcode)
                    return jsonify(status='success')
                except smtplib.SMTPException:
                    return jsonify(status='error', error='send email fail!')
            else:
                return jsonify(status='error', error=error)
        if request.form['request_type'] == 'change_password':
            try:
                email = request.form['email']
                password1 = request.form['password1']
                password2 = request.form['password2']
                verification_code = request.form['verification_code']
            except:
                return jsonify(status='error', error='Failure to obtain data')

            error = None

            if not password1:
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

            if len(User.query.filter_by(email=email).all()) <= 0:
                error = 'User is not existed.'

            if len(VCode.query.filter_by(email=email).all()) > 0:
                v_codes = VCode.query.filter_by(email=email).all()
                time_code = v_codes[len(v_codes) - 1].time  # 取最后一条记录的时间，再转为datetime
                time_now = datetime.now()

                real_v_code = ''
                if (time_now - time_code).total_seconds() <= 15 * 60:  # 时间少于15分钟才算
                    real_v_code = str(v_codes[len(v_codes) - 1].verification_code)
                print('用户v_code：' + verification_code)
                print('数据库v_code：' + real_v_code)
                if verification_code != real_v_code:
                    error = '验证码不正确！'
            else:
                error = '还没有发送验证码！'

            if error is None:
                user = User().query.filter_by(email=email).first()
                user.password = password1
                db.session.add(user)

                return jsonify(status='success', info='change password')
            return jsonify(status='error', error=error)
    return jsonify(status='error', error='method error')


@bp.route('/refresh', methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
        except:
            return jsonify(status='error', error='Data acquisition failure')

        # 通过token获取用户
        try:
            key = current_app.config['SECRET_KEY']
            user_json = jwt.decode(auth_token, key, algorithms=['HS256'])
        except:
            return jsonify(status='error', error='auth_token decode failed')
        # 判断该token是否跟解析出来的用户token一致
        user_id = user_json.get('user_id')
        # 打开数据库连接

        user = User.query.filter_by(user_id=user_id).first()
        # 验证token是否一致，不一致就return
        if str(request.form['auth_token']) != user.auth_token:
            return jsonify(status='error', error='token authenticate failed')

        # 能执行到这里说明验证通过了，返回数据
        user_info = {"nickname": user.nickname, "signature": user.signature,
                     "avatar_url": user.avatar_url, "gender": user.gender,
                     "phone": user.phone, "email": user.email,
                     'auth_token': user.auth_token, 'bg_url': user.bg_url, 'favourable_rate': user.favor_rate}
        return jsonify({"status": 'success', "data": user_info})

    return jsonify(status='error', error='method error')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
