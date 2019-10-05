 # 引用包
import os

import jwt
from flask import (
    request, jsonify, current_app
)
from werkzeug.utils import secure_filename

from . import bp
from .. import db
from ..models import IdleThing, User

# 上传图片相关
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def list_2_json(li):
    json_data = {}  # 每一个键值对是一个帖子
    for idx, post in enumerate(li):  # posts列表，列表元素为元组
        json_data.update({'post_%s' % idx: {
            "user_Email": post.user.email,
            "user_Avatar": post.user.avatar_url,
            "user_Nickname": post.user.nickname,
            "idle_thing_id": post.id,
            "content": post.content,
            "picture_url_1": post.picture_url_1,
            "picture_url_2": post.picture_url_2,
            "picture_url_3": post.picture_url_3,
            "like_number": post.like_number,
            "comment_number": post.comment_number,
            "is_deleted": post.is_deleted,
            "is_finished":post.is_finished,
            "money": post.money}})
    return json_data


# 通过ID获取详细信息
@bp.route('/get_post_by_id', methods=('GET', 'POST'))
def get_post_by_id():
    if request.method == 'POST':
        try:
            id = request.form['post_id']
        except:
            return jsonify(status='error', error='Data obtain failure')

        error = None

        if id is None:
            error = 'Error id.'

        if error is None:
            li = IdleThing.query.filter_by(id=id, is_deleted=0).all()
            json_data = list_2_json(li)
            data = {'status': "success", 'posts': json_data}
            return jsonify(data)
        return jsonify({'status': "error", 'error': 'no data'})
    return jsonify({'status': "error", 'error': 'error method'})


# 改变任务描述
@bp.route('/up_content', methods=('GET', 'POST'))
def up_content():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            post_id = request.form['post_id']
            content = request.form['content']
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
        # 打开数据库连接
        user = User.query.filter_by(user_id=user_id).first()
        # 验证token是否一致，不一致就return
        if str(request.form['auth_token']) != user.auth_token:
            return jsonify(status='error', error='authentication failed')

        post = IdleThing.query.filter_by(id=post_id).first()
        if post.user.user_id != user.user_id:
            return jsonify(status='error', error='Not belonging to the user')
        error = None

        if error is None:
            post.content = content
            try:
                db.session.add(post)
            except:
                db.session.rollback()
                return jsonify({'status': "error", 'error': 'Database error'})

            return jsonify(status='success')
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


# 改变图片1
@bp.route('/up_picture_url_1', methods=('GET', 'POST'))
def up_picture_url_1():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            post_id = request.form['post_id']
            picture = request.files['picture_1']
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
        # 打开数据库连接
        user = User.query.filter_by(user_id=user_id).first()
        # 验证token是否一致，不一致就return
        if str(request.form['auth_token']) != user.auth_token:
            return jsonify(status='error', error='authentication failed')

        post = IdleThing.query.filter_by(id=post_id).first()
        if post.user.user_id != user.user_id:
            return jsonify(status='error', error='Not belonging to the user')
        error = None

        if allowed_file(picture.filename):
            p_name = secure_filename(picture.filename)
            p_name = 'a.' + p_name  # 防止全中文命名经过secure后变成没有名字
            p_name = 'post_id_' + str(post_id) + '_picture_1' + '.' + p_name.rsplit('.', 1)[1].lower()
            picture.save(os.path.join('''./app/static/idle_pictures''', p_name))
        else:
            error = 'Type error'
            return jsonify({'status': 'error', 'error': error})

        if error is None:
            post.picture_url_1 = p_name
            try:
                db.session.add(post)
            except:
                db.session.rollback()
                return jsonify({'status': "error", 'error': 'Database error'})

            return jsonify(status='success')
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


# 改变图片2
@bp.route('/up_picture_url_2', methods=('GET', 'POST'))
def up_picture_url_2():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            post_id = request.form['post_id']
            picture = request.files['picture_2']
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
        # 打开数据库连接
        user = User.query.filter_by(user_id=user_id).first()
        # 验证token是否一致，不一致就return
        if str(request.form['auth_token']) != user.auth_token:
            return jsonify(status='error', error='authentication failed')

        post = IdleThing.query.filter_by(id=post_id).first()
        if post.user.user_id != user.user_id:
            return jsonify(status='error', error='Not belonging to the user')
        error = None

        if allowed_file(picture.filename):
            p_name = secure_filename(picture.filename)
            p_name = 'a.' + p_name  # 防止全中文命名经过secure后变成没有名字
            p_name = 'post_id_' + str(post_id) + '_picture_2' + '.' + p_name.rsplit('.', 1)[1].lower()
            picture.save(os.path.join('''./app/static/idle_pictures''', p_name))
        else:
            error = 'Type error'
            return jsonify({'status': 'error', 'error': error})

        if error is None:
            post.picture_url_2 = p_name
            try:
                db.session.add(post)
            except:
                db.session.rollback()
                return jsonify({'status': "error", 'error': 'Database error'})

            return jsonify(status='success')
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


# 改变图片3
@bp.route('/up_picture_url_3', methods=('GET', 'POST'))
def up_picture_url_3():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            post_id = request.form['post_id']
            picture = request.files['picture_3']
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
        # 打开数据库连接
        user = User.query.filter_by(user_id=user_id).first()
        # 验证token是否一致，不一致就return
        if str(request.form['auth_token']) != user.auth_token:
            return jsonify(status='error', error='authentication failed')

        post = IdleThing.query.filter_by(id=post_id).first()
        if post.user.user_id != user.user_id:
            return jsonify(status='error', error='Not belonging to the user')
        error = None

        if allowed_file(picture.filename):
            p_name = secure_filename(picture.filename)
            p_name = 'a.' + p_name  # 防止全中文命名经过secure后变成没有名字
            p_name = 'post_id_' + str(post_id) + '_picture_3' + '.' + p_name.rsplit('.', 1)[1].lower()
            picture.save(os.path.join('''./app/static/idle_pictures''', p_name))
        else:
            error = 'Type error'
            return jsonify({'status': 'error', 'error': error})

        if error is None:
            post.picture_url_3 = p_name
            try:
                db.session.add(post)
            except:
                db.session.rollback()
                return jsonify({'status': "error", 'error': 'Database error'})

            return jsonify(status='success')
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


# 改变钱
@bp.route('/up_money', methods=('GET', 'POST'))
def up_money():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            post_id = request.form['post_id']
            money = int(request.form['money'])
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
        # 打开数据库连接
        user = User.query.filter_by(user_id=user_id).first()
        # 验证token是否一致，不一致就return
        if str(request.form['auth_token']) != user.auth_token:
            return jsonify(status='error', error='authentication failed')

        post = IdleThing.query.filter_by(id=post_id).first()
        if post.user.user_id != user.user_id:
            return jsonify(status='error', error='Not belonging to the user')
        error = None

        if error is None:
            post.money = money
            try:
                db.session.add(post)
            except:
                db.session.rollback()
                return jsonify({'status': "error", 'error': 'Database error'})

            return jsonify(status='success')
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


# 删除或反删除
@bp.route('/delete_or_not', methods=('GET', 'POST'))
def delete_or_not():  # 如果删除传入ideleted = 1, 如果恢复 = 0
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            post_id = request.form['post_id']
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
        # 打开数据库连接
        user = User.query.filter_by(user_id=user_id).first()
        # 验证token是否一致，不一致就return
        if str(request.form['auth_token']) != user.auth_token:
            return jsonify(status='error', error='authentication failed')

        post = IdleThing.query.filter_by(id=post_id).first()
        if post.user.user_id != user.user_id:
            return jsonify(status='error', error='Not belonging to the user')

        error = None
        if int(post_id) < 0:
            error = 'Error Mission_id.'

        if error is None:
            post.is_deleted = not post.is_deleted
            try:
                db.session.add(post)
            except:
                db.session.rollback()
                return jsonify({'status': "error", 'error': 'Database error'})
            return jsonify(status='success')
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


# 向idle thing表插入新的行
@bp.route('/insert', methods=('GET', 'POST'))
def insert():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            content = request.form['content']
            money = request.form['money']
        except:
            return jsonify(status='error', error='Data obtain failure')

        picture_num = 0
        try:
            picture_1 = request.files['picture_1']
            picture_num = picture_num + 1
        except:
            pass
        try:

            picture_2 = request.files['picture_2']
            picture_num = picture_num + 1
        except:
            pass

        try:
            picture_3 = request.files['picture_3']
            picture_num = picture_num + 1
        except:
            pass

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
            return jsonify(status='error', error='authentication failed')

        # 获取帖子的id用来命名图片
        res = db.session.query(db.func.max(IdleThing.id).label('max_id')).one()
        post_id = res.max_id + 1
        # 重写文件名，保存图片
        p1_name = None
        p2_name = None
        p3_name = None
        if picture_num >= 1 and allowed_file(picture_1.filename):
            p1_name = secure_filename(picture_1.filename)
            p1_name = 'a.' + p1_name  # 防止全中文命名经过secure后变成没有名字
            p1_name = 'post_id_' + str(post_id) + '_picture_1' + '.' + p1_name.rsplit('.', 1)[1].lower()
            picture_1.save(os.path.join('''./app/static/idle_pictures''', p1_name))

        if picture_num >= 2 and allowed_file(picture_2.filename):
            p2_name = secure_filename(picture_2.filename)
            p2_name = 'a.' + p2_name  # 防止全中文命名经过secure后变成没有名字
            p2_name = 'post_id_' + str(post_id) + '_picture_2' + '.' + p2_name.rsplit('.', 1)[1].lower()
            picture_2.save(os.path.join('''./app/static/idle_pictures''', p2_name))

        if picture_num >= 3 and allowed_file(picture_3.filename):
            p3_name = secure_filename(picture_3.filename)
            p3_name = 'a.' + p3_name  # 防止全中文命名经过secure后变成没有名字
            p3_name = 'post_id_' + str(post_id) + '_picture_3' + '.' + p3_name.rsplit('.', 1)[1].lower()
            picture_3.save(os.path.join('''./app/static/idle_pictures''', p3_name))

        error = None
        if content is None:
            error = 'Error content.'
        if money is None:
            error = 'Error money.'

        if error is None:
            # 打开数据库连接
            try:
                p = IdleThing(user=user, content=content, picture_url_1=p1_name, picture_url_2=p2_name,
                              picture_url_3=p3_name, money=money)
                db.session.add(p)
            except:
                db.session.rollback()
                return jsonify({'status': "error", 'error': 'Database error'})

            return jsonify(status='success')
        return jsonify({'status': "error", 'error': 'no data'})
    return jsonify({'status': "error", 'error': 'error method'})


# 刷新任务目的地点获取任务的详细信息
@bp.route('/refresh_newest', methods=('GET', 'POST'))
def refresh_newest():
    if request.method == 'POST':
        json_data = {}
        json_data = list_2_json(
            IdleThing.query.order_by(IdleThing.id.desc()).limit(10).all())
        data = {'status': "success", 'data': json_data}
        return jsonify(data)
    return jsonify({'status': "error", 'error': 'error method'})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
