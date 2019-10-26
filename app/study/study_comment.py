import jwt
from flask import (
    request, jsonify, current_app
)

from . import bp
from .. import db
from ..models import Study, User, StudyComment, Permission


@bp.route('/comment/add', methods=['GET', 'POST'])
def add_mission_comment():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            content = request.form['content']
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
        post = Study.query.filter_by(id=post_id).first()

        error = None
        if content is None:
            error = 'Error content.'
        if user is None:
            error = 'Error user.'
        if post is None:
            error = 'Error post.'

        if error is None:
            # 打开数据库连接
            mc = StudyComment(user=user, post=post, content=content)
            post.comment_number += 1
            try:
                db.session.add_all([mc, post])
                db.session.commit()
            except:
                db.session.rollback()
                return jsonify({'status': "error", 'error': 'Database error'})

            mc_json = {
                "id": mc.id,
                "user_email": mc.user.email,
                "user_avatar": mc.user.avatar_url,
                "user_nickname": mc.user.nickname,
                "user_id": mc.user.user_id,
                "post_id": mc.post.id,
                "content": mc.content,
                "time": mc.time,
                "disabled": mc.disabled}
            return jsonify(status='success', data=mc_json)

        return jsonify({'status': "error", 'error': 'no data'})
    return jsonify({'status': "error", 'error': 'error method'})


@bp.route('/comment/delete', methods=['GET', 'POST'])
def delete_mission_comment():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            id = request.form['id']
        except:
            return jsonify(status='error', error='Data obtain failure')

        # 通过token获取用户
        try:
            key = current_app.config['SECRET_KEY']
            user_json = jwt.decode(auth_token, key, algorithms=['HS256'])
        except:
            return jsonify(status='error', error='Decode failed')
        # 判断该token是否跟解析出来的用户token一致
        user_id = user_json.get('user_id')

        # 打开数据库连接
        user = User.query.filter_by(user_id=user_id).first()

        mc = StudyComment.query.filter_by(id=id, disabled=0).first()
        if user != mc.user \
                and not user.can(Permission.MODERATE_COMMENTS):
            return jsonify(status='error', error='Permission deny')

        error = None
        if user is None:
            error = 'Error user.'

        if mc is None:
            error = 'Error id.'

        if error is None:
            # 打开数据库连接
            post = mc.post
            try:
                post.comment_number -= 1
                mc.disabled = True
                db.session.add_all([post, mc])
            except:
                db.session.rollback()
                return jsonify({'status': "error", 'error': 'Database error'})
            return jsonify(status='success')
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})
