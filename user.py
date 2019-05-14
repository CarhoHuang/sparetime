import jwt
import os
import random
import smtplib
from email.header import Header
from email.mime.text import MIMEText
import pymysql
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from datetime import datetime
from flask import (
    Blueprint, request, jsonify
)

from dbconfig import *

bp = Blueprint('user', __name__, url_prefix='/user')
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
            phone = request.form['phone']
            signature = request.form['signature']
        except:
            return jsonify(status='error', error='Data acquisition failure')

        # 通过token获取用户
        try:
            key = 'sparetimeforu_key'
            user_json = jwt.decode(auth_token, key, algorithms=['HS256'])
        except:
            return jsonify(status='error', error='decode failed')
        # 判断该token是否跟解析出来的用户token一致
        user_id = user_json.get('user_id')
        # 打开数据库连接
        db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
        # 使用 cursor() 方法创建一个游标对象 cursor，获取对应的user
        cur = db.cursor()
        cur.execute('''select * from users where user_id=%s''', user_id)
        test_user = cur.fetchone()
        # 验证token是否一致，不一致就return
        if str(request.form['auth_token']) != test_user[12]:
            return jsonify(status='error', error='authentication failed')
        error = None
        if nickname is None:
            error = 'Error nickname'
        if gender is None:
            error = 'Error gender'
        if len(phone) is not 11:
            error = 'Error phone'
        if signature is None:
            error = 'Error signature'

        if error is None:
            # 打开数据库连接
            db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
            # 使用 cursor() 方法创建一个游标对象 cursor，获取对应的user
            cur = db.cursor()
            cur.execute('''update users set nickname=%s,gender=%s,phone=%s,signature=%s where user_id=%s''',
                        (nickname, gender, phone, signature, user_id))
            db.commit()
            db.close()
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
            key = 'sparetimeforu_key'
            user_json = jwt.decode(auth_token, key, algorithms=['HS256'])
        except:
            return jsonify(status='error', error='decode failed')
        # 判断该token是否跟解析出来的用户token一致
        user_id = user_json.get('user_id')
        # 打开数据库连接
        db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
        # 使用 cursor() 方法创建一个游标对象 cursor，获取对应的user
        cur = db.cursor()
        cur.execute('''select * from users where user_id=%s''', user_id)
        test_user = cur.fetchone()
        # 验证token是否一致，不一致就return
        if str(request.form['auth_token']) != test_user[12]:
            return jsonify(status='error', error='authentication failed')

        error = None
        if avatar_file is None:
            error = 'Error avatar file'
        # 没有错误就开始处理
        if error is None and allowed_file(avatar_file.filename):
            avatar_name = secure_filename(avatar_file.filename)
            now_second = int((datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0)).total_seconds())
            avatar_name = 'user_id_' + str(user_id) + '_' + str(now_second) + '.' + \
                          avatar_name.rsplit('.', 1)[1].lower()
            avatar_file.save(os.path.join('''./static/avatar''', avatar_name))

            # 打开数据库连接
            db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
            # 使用 cursor() 方法创建一个游标对象 cursor，获取对应的user
            cur = db.cursor()
            cur.execute('''update users set avatar_url=%s where user_id=%s''',
                        (avatar_name, user_id))
            db.commit()
            db.close()
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
            key = 'sparetimeforu_key'
            user_json = jwt.decode(auth_token, key, algorithms=['HS256'])
        except:
            return jsonify(status='error', error='decode failed')
        # 判断该token是否跟解析出来的用户token一致
        user_id = user_json.get('user_id')
        # 打开数据库连接
        db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
        # 使用 cursor() 方法创建一个游标对象 cursor，获取对应的user
        cur = db.cursor()
        cur.execute('''select * from users where user_id=%s''', user_id)
        test_user = cur.fetchone()
        # 验证token是否一致，不一致就return
        if str(request.form['auth_token']) != test_user[12]:
            return jsonify(status='error', error='authentication failed')

        error = None
        if bg_file is None:
            error = 'Error bg file'
        # 没有错误就开始处理
        if error is None and allowed_file(bg_file.filename):
            bg_name = secure_filename(bg_file.filename)
            now_second = int((datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0)).total_seconds())
            bg_name = 'user_id_' + str(user_id) + '_' + str(now_second) + '.' + \
                      bg_name.rsplit('.', 1)[1].lower()
            bg_file.save(os.path.join('''./static/personal_background''', bg_name))

            # 打开数据库连接
            db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
            # 使用 cursor() 方法创建一个游标对象 cursor，获取对应的user
            cur = db.cursor()
            cur.execute('''update users set personal_background_url=%s where user_id=%s''',
                        (bg_name, user_id))
            db.commit()
            db.close()
            return jsonify(status='success')
        return jsonify(status='error', error=error)
    return jsonify(status='error', error='method error')  # is not post method


# 修改密码
@bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        if request.form['request_type'] == 'send_verification_code':
            try:
                email = request.form['email']
            except:
                return jsonify(status='error', error='Failure to obtain data')

            error = None
            if email is None:
                error = 'Error email'
            # 查用户是否存在
            db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
            # 使用 cursor() 方法创建一个游标对象 cursor
            cur = db.cursor()
            error = None
            if cur.execute('select * from users where email = %s', (email,)) <= 0:
                error = 'User is not existed.'

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
                    return jsonify(status='success', info='send_verification_code')
                except smtplib.SMTPException:
                    return jsonify(status='error', error='send email fail!')
            db.close()
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
            # 打开数据库连接
            db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
            # 使用 cursor() 方法创建一个游标对象 cursor
            cur = db.cursor()

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

            if cur.execute('select * from users where email = %s', (email,)) <= 0:
                error = 'User is not existed.'

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
                    'update users set hash_pw=%s where email=%s',
                    (generate_password_hash(password1), email)
                )
                db.commit()
                # disconnect mysql
                db.close()
                return jsonify(status='success', info='change password')
            return jsonify(status='error', error=error)
    return jsonify(status='error', error='method error')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
