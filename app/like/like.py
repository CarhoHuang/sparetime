import jwt
from flask import (
    request, jsonify, current_app
)
from . import bp
from .. import db
from ..models import IdleThing, Mission, Study, SearchThing, User, Like


@bp.route('', methods=['GET', 'POST'])
def like():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            post_type = request.form['post_type']
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
        post = None
        if int(post_type) == 0:
            post = Mission.query.filter_by(id=post_id).first()
        elif int(post_type) == 1:
            post = IdleThing.query.filter_by(id=post_id).first()
        elif int(post_type) == 2:
            post = Study.query.filter_by(id=post_id).first()
        elif int(post_type) == 3:
            post = SearchThing.query.filter_by(id=post_id).first()

        error = None
        if post_type is None:
            error = 'Error type.'
        if user is None:
            error = 'Error user.'

        dislike = False
        if len(Like.query.filter_by(post_type=post_type,
                                    post_id=post_id, user=user, is_cancel=0).all()) >= 1:
            dislike = True

        # 验证token是否一致，不一致就return
        if str(request.form['auth_token']) != user.auth_token:
            return jsonify(status='error', error='Authenticate failed')

        if error is None:
            # 打开数据库连接
            try:
                if dislike:
                    praise = Like.query.filter_by(
                        post_type=post_type, post_id=post_id, user=user, is_cancel=0).first()
                    praise.is_cancel = 1
                    post.like_number -= 1
                else:
                    praise = Like.query.filter_by(
                        post_type=post_type, post_id=post_id, user=user).first()
                    if praise is None:
                        praise = Like(post_type=post_type, post_id=post_id, user=user)
                    praise.is_cancel = 0
                    post.like_number += 1
                db.session.add_all([praise, post])
                db.session.commit()
            except:
                db.session.rollback()
                return jsonify({'status': "error", 'error': 'Database error'})

            return jsonify(status='success')
        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})


@bp.route('/is_like', methods=['GET', 'POST'])
def is_like():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            post_type = request.form['post_type']
            post_id = request.form['post_id']
        except:
            return jsonify(status='error', error='Data obtain failure')

        # 通过token获取用户
        try:
            key = current_app.config['SECRET_KEY']
            user_json = jwt.decode(auth_token, key, algorithms=['HS256'])
        except:
            return jsonify(status='error', error='decode failed')
        user_id = user_json.get('user_id')

        # 打开数据库连接
        user = User.query.filter_by(user_id=user_id).first()
        # 验证token是否一致，不一致就return
        if str(request.form['auth_token']) != user.auth_token:
            return jsonify(status='error', error='Authenticate failed')

        error = None
        if post_type is None:
            error = 'Error type.'
        if user is None:
            error = 'Error user.'

        dislike = False
        if len(Like.query.filter_by(post_type=post_type,
                                    post_id=post_id, user=user, is_cancel=0).all()) < 1:
            dislike = True

        if error is None:
            try:
                if dislike:
                    return jsonify({'status': "success", 'is_like': 'dislike'})
                else:
                    return jsonify({'status': "success", 'is_like': 'like'})
            except:
                return jsonify({'status': "error", 'error': 'Database error'})

        return jsonify({'status': "error", 'error': error})
    return jsonify({'status': "error", 'error': 'error method'})
