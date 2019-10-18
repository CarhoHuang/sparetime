# 引用包
import os
from datetime import datetime

import jwt
from flask import (
    request, jsonify, current_app
)
from werkzeug.utils import secure_filename

from . import bp
from .. import db
from ..models import Mission, User, MissionComment

# 上传图片相关
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def list_2_json(li):
    json_data = {}  # 每一个键值对是一个帖子
    for idx, mission in enumerate(li):  # posts列表，列表元素为元组
        json_data.update({'post_%s' % idx: {
            "user_Email": mission.user.email,
            "user_Avatar": mission.user.avatar_url,
            "user_Nickname": mission.user.nickname,
            "content": mission.content,
            "picture_url_1": mission.picture_url_1,
            "picture_url_2": mission.picture_url_2,
            "picture_url_3": mission.picture_url_3,
            "origin": mission.origin,
            "destination": mission.destination,
            "like_number": mission.like_number,
            "comment_number": mission.comment_number,
            "errand_id": mission.id,
            "is_deleted": mission.is_deleted,
            "end_time": mission.end_time,
            "release_time": mission.release_time,
            "money": mission.money,
            "evaluate": mission.evaluate,
            "receiver_id": mission.receiver_id,
            "is_received": mission.is_received,
            "is_finished": mission.is_finished}})
    return json_data


def list_2_cjson(li):
    json_data = {}  # 每一个键值对是一个帖子
    for idx, comment in enumerate(li):  # posts列表，列表元素为元组
        json_data.update({'comment_%s' % idx: {
            "id": comment.id,
            "user_email": comment.user.email,
            "user_avatar": comment.user.avatar_url,
            "user_nickname": comment.user.nickname,
            "user_id": comment.user.user_id,
            "post_id": comment.post.id,
            "content": comment.content,
            "time": comment.time,
            "disabled": comment.disabled}})
    return json_data


# 通过任务ID获取任务的详细信息
@bp.route('/get_mission_by_mission_id', methods=('GET', 'POST'))
def get_mission_by_mission_id():
    if request.method == 'POST':
        try:
            id = request.form['errand_id']
        except:
            return jsonify(status='error', error='Data obtain failure')

        error = None

        if id is None:
            error = 'Error id.'

        if error is None:
            li = Mission.query.filter_by(id=id, is_deleted=0).all()
            json_data = list_2_json(li)

            cli = MissionComment.query.filter_by(post=li[0]).all()
            comment_data = list_2_cjson(cli)

            data = {'status': "success", 'data': {'errand_message': json_data, 'comments_message': comment_data}}
            return jsonify(data)
        return jsonify({'status': "error", 'error': 'no data'})
    return jsonify({'status': "error", 'error': 'error method'})


# 通过任务开始地点获取任务的详细信息
@bp.route('/get_mission_by_origin', methods=('GET', 'POST'))
def get_mission_by_origin():
    if request.method == 'POST':
        origin = request.form['origin']
        error = None
        if origin is None:
            error = 'Error origin.'

        if error is None:
            li = Mission.query.filter_by(origin=origin, is_deleted=0).all()
            json_data = list_2_json(li)
            data = {'status': "success", 'posts': json_data}
            return jsonify(data)
        return jsonify({'status': "error", 'error': 'no data'})
    return jsonify({'status': "error", 'error': 'error method'})


# 通过任务目的地点获取任务的详细信息
@bp.route('/get_mission_by_destination', methods=('GET', 'POST'))
def get_mission_by_destination():
    if request.method == 'POST':
        destination = request.form['destination']
        error = None
        if destination is None:
            error = 'Error origin.'

        if error is None:
            li = Mission.query.filter_by(destination=destination, is_deleted=0).all()
            json_data = list_2_json(li)
            data = {'status': "success", 'posts': json_data}
            return jsonify(data)
        return jsonify({'status': "error", 'error': 'no data'})
    return jsonify({'status': "error", 'error': 'error method'})


# 改变任务开始地点
@bp.route('/up_origin', methods=('GET', 'POST'))
def up_origin():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            post_id = request.form['post_id']
            origin = request.form['origin']
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

        mission = Mission.query.filter_by(id=post_id).first()
        if mission.user.user_id != user.user_id:
            return jsonify(status='error', error='Not belonging to the user')
        error = None

        if error is None:
            m = Mission.query.filter_by(id=post_id).first()
            m.origin = origin
            try:
                db.session.add(m)
            except:
                db.session.rollback()
                return jsonify({'status': "error", 'error': 'Database error'})

            return jsonify(status='success')
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


# 改变任务目的地点
@bp.route('/up_destination', methods=('GET', 'POST'))
def up_destination():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            post_id = request.form['post_id']
            destination = request.form['destination']
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

        mission = Mission.query.filter_by(id=post_id).first()
        if mission.user.user_id != user.user_id:
            return jsonify(status='error', error='Not belonging to the user')
        error = None

        if error is None:
            m = Mission.query.filter_by(id=post_id).first()
            m.destination = destination
            try:
                db.session.add(m)
            except:
                db.session.rollback()
                return jsonify({'status': "error", 'error': 'Database error'})

            return jsonify(status='success')
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


# 改变任务截止时间 时间传入字符串格式 Apr 13 2019 18:27
@bp.route('/up_end_time', methods=('GET', 'POST'))
def up_end_time():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            post_id = request.form['post_id']
            end_time_str = request.form['end_time']
            end_time = datetime.strptime(end_time_str, '%b %d %Y %H:%M')
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

        mission = Mission.query.filter_by(id=post_id).first()
        if mission.user.user_id != user.user_id:
            return jsonify(status='error', error='Not belonging to the user')
        error = None

        if error is None:
            m = Mission.query.filter_by(id=post_id).first()
            m.end_time = end_time
            try:
                db.session.add(m)
            except:
                db.session.rollback()
                return jsonify({'status': "error", 'error': 'Database error'})

            return jsonify(status='success')
        return jsonify({'status': "error", 'error': error})
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

        mission = Mission.query.filter_by(id=post_id).first()
        if mission.user.user_id != user.user_id:
            return jsonify(status='error', error='Not belonging to the user')
        error = None

        if error is None:
            m = Mission.query.filter_by(id=post_id).first()
            m.content = content
            try:
                db.session.add(m)
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

        mission = Mission.query.filter_by(id=post_id).first()
        if mission.user.user_id != user.user_id:
            return jsonify(status='error', error='Not belonging to the user')
        error = None

        if allowed_file(picture.filename):
            p_name = secure_filename(picture.filename)
            p_name = 'a.' + p_name  # 防止全中文命名经过secure后变成没有名字
            p_name = 'post_id_' + str(post_id) + '_picture_1' + '.' + p_name.rsplit('.', 1)[1].lower()
            picture.save(os.path.join('''./app/static/mission_pictures''', p_name))
        else:
            error = 'Type error'
            return jsonify({'status': 'error', 'error': error})

        if error is None:
            m = Mission.query.filter_by(id=post_id).first()
            m.picture_url_1 = p_name
            try:
                db.session.add(m)
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

        mission = Mission.query.filter_by(id=post_id).first()
        if mission.user.user_id != user.user_id:
            return jsonify(status='error', error='Not belonging to the user')
        error = None

        if allowed_file(picture.filename):
            p_name = secure_filename(picture.filename)
            p_name = 'a.' + p_name  # 防止全中文命名经过secure后变成没有名字
            p_name = 'post_id_' + str(post_id) + '_picture_2' + '.' + p_name.rsplit('.', 1)[1].lower()
            picture.save(os.path.join('''./app/static/mission_pictures''', p_name))
        else:
            error = 'Type error'
            return jsonify({'status': 'error', 'error': error})

        if error is None:
            m = Mission.query.filter_by(id=post_id).first()
            m.picture_url_2 = p_name
            try:
                db.session.add(m)
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

        mission = Mission.query.filter_by(id=post_id).first()
        if mission.user.user_id != user.user_id:
            return jsonify(status='error', error='Not belonging to the user')
        error = None

        if allowed_file(picture.filename):
            p_name = secure_filename(picture.filename)
            p_name = 'a.' + p_name  # 防止全中文命名经过secure后变成没有名字
            p_name = 'post_id_' + str(post_id) + '_picture_3' + '.' + p_name.rsplit('.', 1)[1].lower()
            picture.save(os.path.join('''./app/static/mission_pictures''', p_name))
        else:
            error = 'Type error'
            return jsonify({'status': 'error', 'error': error})

        if error is None:
            m = Mission.query.filter_by(id=post_id).first()
            m.picture_url_3 = p_name
            try:
                db.session.add(m)
            except:
                db.session.rollback()
                return jsonify({'status': "error", 'error': 'Database error'})

            return jsonify(status='success')
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


# 改变赏金
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

        mission = Mission.query.filter_by(id=post_id).first()
        if mission.user.user_id != user.user_id:
            return jsonify(status='error', error='Not belonging to the user')
        error = None

        if error is None:
            m = Mission.query.filter_by(id=post_id).first()
            m.money = money
            try:
                db.session.add(m)
            except:
                db.session.rollback()
                return jsonify({'status': "error", 'error': 'Database error'})

            return jsonify(status='success')
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


# 给予任务评价
@bp.route('/up_evaluate', methods=('GET', 'POST'))
def up_evaluate():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            post_id = request.form['post_id']
            evaluate = int(request.form['evaluate'])
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

        mission = Mission.query.filter_by(id=post_id).first()
        if mission.user.user_id != user.user_id:
            return jsonify(status='error', error='Not belonging to the user')
        error = None

        if error is None:
            m = Mission.query.filter_by(id=post_id).first()
            m.evaluate = evaluate
            try:
                db.session.add(m)
            except:
                db.session.rollback()
                return jsonify({'status': "error", 'error': 'Database error'})

            # 接下来帮接收者更新好评率

            return jsonify(status='success')
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


# 删除或反删除任务
@bp.route('/delete_or_not', methods=('GET', 'POST'))
def delete_or_not():  # 如果删除传入is_deleted = 1, 如果恢复 = 0
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

        mission = Mission.query.filter_by(id=post_id).first()
        if mission.user.user_id != user.user_id:
            return jsonify(status='error', error='Not belonging to the user')

        error = None
        if int(post_id) < 0:
            error = 'Error Mission_id.'

        if error is None:
            mission.is_deleted = not mission.is_deleted
            try:
                db.session.add(mission)
            except:
                db.session.rollback()
                return jsonify({'status': "error", 'error': 'Database error'})
            return jsonify(status='success')
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


# 向mission表插入新的行
@bp.route('/insert', methods=('GET', 'POST'))
def insert():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            content = request.form['content']
            origin = request.form['origin']
            destination = request.form['destination']
            end_time_str = request.form['end_time']
            end_time = datetime.strptime(end_time_str, '%b %d %Y %H:%M')
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
        res = db.session.query(db.func.max(Mission.id).label('max_id')).one()
        if res.max_id is not None:
            post_id = res.max_id + 1
        else:
            post_id = 1
        # 重写文件名，保存图片
        p1_name = None
        p2_name = None
        p3_name = None
        if picture_num >= 1 and allowed_file(picture_1.filename):
            p1_name = secure_filename(picture_1.filename)
            p1_name = 'a.' + p1_name  # 防止全中文命名经过secure后变成没有名字
            p1_name = 'post_id_' + str(post_id) + '_picture_1' + '.' + p1_name.rsplit('.', 1)[1].lower()
            picture_1.save(os.path.join('''./app/static/mission_pictures''', p1_name))

        if picture_num >= 2 and allowed_file(picture_2.filename):
            p2_name = secure_filename(picture_2.filename)
            p2_name = 'a.' + p2_name  # 防止全中文命名经过secure后变成没有名字
            p2_name = 'post_id_' + str(post_id) + '_picture_2' + '.' + p2_name.rsplit('.', 1)[1].lower()
            picture_2.save(os.path.join('''./app/static/mission_pictures''', p2_name))

        if picture_num >= 3 and allowed_file(picture_3.filename):
            p3_name = secure_filename(picture_3.filename)
            p3_name = 'a.' + p3_name  # 防止全中文命名经过secure后变成没有名字
            p3_name = 'post_id_' + str(post_id) + '_picture_3' + '.' + p3_name.rsplit('.', 1)[1].lower()
            picture_3.save(os.path.join('''./app/static/mission_pictures''', p3_name))

        error = None
        if content is None:
            error = 'Error content.'
        if destination is None:
            error = 'Error destination.'
        if end_time is None:
            error = 'Error deadline.'
        if money is None:
            error = 'Error money.'

        if error is None:
            # 打开数据库连接
            try:
                m = Mission(user=user, content=content, picture_url_1=p1_name, picture_url_2=p2_name,
                            picture_url_3=p3_name, origin=origin, destination=destination, end_time=end_time,
                            money=money)
                db.session.add(m)
            except Exception:
                print(Exception.args)
                db.session.rollback()
            return jsonify(status='success')

        return jsonify({'status': "error", 'error': 'no data'})
    return jsonify({'status': "error", 'error': 'error method'})


# 刷新任务目的地点获取任务的详细信息
@bp.route('/refresh_newest', methods=('GET', 'POST'))
def refresh_newest():
    if request.method == 'POST':
        try:
            destination = request.form['destination']
            biggest_id = int(request.form['biggest_id'])
        except:
            return jsonify(status='error', error='Data obtain failure')

        # 先去取得一个最大的id,label 方法重新命名了一个字段
        res = db.session.query(db.func.max(Mission.id).label('max_id')).one()
        id = res.max_id

        error = None
        if destination is None:
            error = 'Error destination.'
        if biggest_id is None:
            error = 'Error before'

        json_data = {}
        if error is None:
            if destination == '随机' and id > biggest_id:
                json_data = list_2_json(
                    Mission.query.filter(Mission.id > biggest_id, Mission.is_received == 0).order_by(
                        Mission.id.desc()).limit(10).all())
            elif id > biggest_id:
                print(biggest_id, destination)
                json_data = list_2_json(
                    Mission.query.filter(Mission.id > biggest_id, Mission.is_received == 0,
                                         Mission.destination == destination).order_by(Mission.id.desc()).limit(
                        10).all())

            return jsonify({'status': "success", 'data': json_data})
        return jsonify({'status': "error", 'error': 'no data'})
    return jsonify({'status': "error", 'error': 'error method'})


# 获取用户发布的任务帖子
@bp.route('/get_user_posts', methods=['GET', 'POST'])
def get_user_posts():
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
        except:
            return jsonify(status='error', error='Data obtain failure')

        error = None
        if user_id is None:
            error = 'Error user.'

        if error is None:
            json_data = list_2_json(
                Mission.query.filter_by(user_id=user_id).order_by(Mission.id.desc()).all())

            return jsonify({'status': "success", 'data': json_data})
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


# 获取用户接受的任务帖子
@bp.route('/get_user_received_posts', methods=['GET', 'POST'])
def get_user_received_posts():
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
        except:
            return jsonify(status='error', error='Data obtain failure')

        error = None
        if user_id is None:
            error = 'Error user.'

        if error is None:
            json_data = list_2_json(
                Mission.query.filter_by(receiver_id=user_id, is_received=1).order_by(Mission.id.desc()).all())

            return jsonify({'status': "success", 'data': json_data})
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


# 获取用户已接收到且完成的任务
@bp.route('/get_user_received_done_posts', methods=['GET', 'POST'])
def get_user_received_done_posts():
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
        except:
            return jsonify(status='error', error='Data obtain failure')

        error = None
        if user_id is None:
            error = 'Error user.'

        if error is None:
            json_data = list_2_json(
                Mission.query.filter_by(receiver_id=user_id, is_received=1, is_finished=1).order_by(
                    Mission.id.desc()).all())

            return jsonify({'status': "success", 'data': json_data})
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


# 获取用户已接收到但未完成的任务
@bp.route('/get_user_received_ndone_posts', methods=['GET', 'POST'])
def get_user_received_ndone_posts():
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
        except:
            return jsonify(status='error', error='Data obtain failure')

        error = None
        if user_id is None:
            error = 'Error user.'

        if error is None:
            json_data = list_2_json(
                Mission.query.filter_by(receiver_id=user_id, is_received=1, is_finished=0).order_by(
                    Mission.id.desc()).all())

            return jsonify({'status': "success", 'data': json_data})
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


@bp.route('/receive_mission', methods=['GET', 'POST'])
def receive_mission():
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
            return jsonify(status='error', error='Authenticate failed')

        mission = Mission.query.filter_by(id=post_id).first()
        error = None

        if error is None:
            try:
                mission.receiver_id = user.user_id
                mission.is_received = not mission.is_received
                db.session.add(mission)
            except Exception:
                print(Exception.args)
                db.session.rollback()
                return jsonify({'status': "error", 'error': 'Database error'})
            return jsonify(status='success')
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


@bp.route('/finish_mission', methods=['GET', 'POST'])
def finish_mission():
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
            return jsonify(status='error', error='Authenticate failed')

        mission = Mission.query.filter_by(id=post_id).first()
        if mission.user.user_id != user.user_id:
            return jsonify(status='error', error='Not belonging to the user')
        error = None

        if error is None:
            try:
                mission.is_finished = not mission.is_finished
                db.session.add(mission)
            except Exception:
                print(Exception.args)
                db.session.rollback()
                return jsonify({'status': "error", 'error': 'Database error'})

            return jsonify(status='success')
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


@bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        try:
            content = request.form['content']
        except:
            return jsonify(status='error', error='Data obtain failure')

        error = None
        if content is None:
            error = 'Error content.'

        if error is None:
            post_li = Mission.query.filter(Mission.content.like('%' + content + '%')).order_by(
                Mission.id.desc()).limit(20).all()  # 标题
            post_li.extend(Mission.query.filter(Mission.origin.like('%' + content + '%')).order_by(
                Mission.id.desc()).limit(20).all())  # 起点
            post_li.extend(Mission.query.filter(Mission.destination.like('%' + content + '%')).order_by(
                Mission.id.desc()).limit(20).all())  # 终点
            post_li.extend(
                Mission.query.join(User).filter(User.nickname.like('%' + content + '%')).order_by(
                    Mission.id.desc()).limit(20).all())  # 用户

            json_data = list_2_json(post_li)

            return jsonify({'status': "success", 'data': json_data})
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


@bp.route('/load_more', methods=['GET', 'POST'])
def load_more():
    if request.method == 'POST':
        try:
            page_str = request.form['page']
        except:
            return jsonify(status='error', error='Data obtain failure')

        try:
            page = int(page_str)
        except ValueError:
            page = 1
        # 分页
        pagination = Mission.query.order_by(Mission.release_time.desc()) \
            .paginate(page=page, per_page=current_app.config['POSTS_PER_PAGE'],
                      error_out=False)
        json_data = list_2_json(pagination.items)

        # 分页对象转JSON
        pagination_json = {'has_next': pagination.has_next,
                           'has_prev': pagination.has_prev,
                           'next_num': pagination.next_num,
                           'prev_num': pagination.prev_num,
                           'page': pagination.page,
                           'pages': pagination.pages,
                           'per_page': pagination.per_page,
                           'total': pagination.total}

        data = {'status': "success", 'data': json_data, 'pagination': pagination_json}
        return jsonify(data)
    return jsonify({'status': "error", 'error': 'error method'})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
