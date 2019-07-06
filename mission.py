# 引用包
import os
import pymysql
import jwt
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import (
    Blueprint, request, jsonify
)

from dbconfig import *

bp = Blueprint('mission', __name__, url_prefix='/mission')
# 上传图片相关
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# 遍历数据库返回所有符合条件的行
@bp.route('/search', methods=('GET', 'POST'))
def search(sql):
    # 打开数据库连接
    db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cur = db.cursor()

    cur.execute(sql)
    posts = cur.fetchall()
    db.close()

    json_data = {}  # 每一个键值对是一个帖子
    for idx, row in enumerate(posts):  # posts列表，列表元素为元组
        json_data.update({'post_%s' % idx: {
            "user_id": row[0],
            "content": row[1],
            "picture_url_1": row[2],
            "picture_url_2": row[3],
            "picture_url_3": row[4],
            "origin": row[5],
            "destination": row[6],
            "like_number": row[7],
            "comment_number": row[8],
            "id": row[9],
            "is_deleted": row[10],
            "end_time": row[11],
            "money": row[12],
            "evaluate": row[13],
            "receiver_id": row[14],
            "is_received":row[15]}})
    return json_data


# 通过任务ID获取任务的详细信息
@bp.route('/get_mission_by_mission_id', methods=('GET', 'POST'))
def get_mission_by_mission_id():
    if request.method == 'POST':
        try:
            # 拿出auth_token，裁剪掉前两位和最后一位
            auth_token_str = str(request.form['auth_token'])[2:len(str(request.form['auth_token'])) - 1]
            auth_token = bytes(auth_token_str, 'utf8')
            id = request.form['id']
        except:
            return jsonify(status='error', error='Data acquisition failure')
        error = None

        if id is None:
            error = 'Error id.'

        if error is None:
            sql = 'select * from mission where id = %s and is_deleted = 0 ' % (id,)
            json_data = search(sql)
            data = {'status': "success", 'posts': json_data}
            return jsonify(data)
        return jsonify(error=error)
    return 1


# 通过任务开始地点获取任务的详细信息
@bp.route('/get_mission_by_origin', methods=('GET', 'POST'))
def get_mission_by_origin():
    if request.method == 'POST':
        origin = request.form['origin']
        error = None
        if origin is None:
            error = 'Error origin.'

        if error is None:
            sql = 'select * from mission where origin = %s and is_deleted =0' % (origin,)
            json_data = search(sql)
            data = {'status': "success", 'posts': json_data}
            return jsonify(data)
        return jsonify(error=error)
    return 1


# 通过任务目的地点获取任务的详细信息
@bp.route('/get_mission_by_destination', methods=('GET', 'POST'))
def get_mission_by_destination():
    if request.method == 'POST':
        destination = request.form['destination']
        error = None
        if destination is None:
            error = 'Error destination.'

        if error is None:
            sql = 'select * from mission where destination = %s and is_deleted =0' % (destination,)
            json_data = search(sql)
            data = {'status': "success", 'posts': json_data}
            return jsonify(data)
        return jsonify(error=error)
    return 1


# 更改数据
@bp.route('/up', methods=('GET', 'POST'))
def up(sql):
    # 打开数据库连接
    db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cur = db.cursor()

    cur.execute(sql)
    db.commit()
    db.close()

    return True


# 改变任务开始地点
@bp.route('/up_origin', methods=('GET', 'POST'))
def up_origin():
    if request.method == 'POST':
        origin = request.form['origin']
        error = None
        if origin is None:
            error = 'Error origin.'

        if error is None:
            sql = '''
            update mission set origin='%s' where id=1
            ''' % origin
            print(sql)
            up(sql)
            return jsonify(status='success')
        return jsonify(error=error)
    return 1


# 改变任务目的地点
@bp.route('/up_destination', methods=('GET', 'POST'))
def up_destination():
    if request.method == 'POST':
        destination = request.form['destination']
        error = None
        if destination is None:
            error = 'Error EndLocation.'

        if error is None:
            sql = 'update mission set destination = %s' % (destination,)
            success = up(sql)
            return jsonify(success=success)
        return jsonify(error=error)
    return 1


# 改变任务截止时间
@bp.route('/up_end_time', methods=('GET', 'POST'))
def up_end_time():
    if request.method == 'POST':
        end_time = request.form['end_time']
        error = None
        if end_time is None:
            error = 'Error EndTime.'

        if error is None:
            sql = 'update mission set end_time = %s' % (end_time,)
            success = up(sql)
            return jsonify(success=success)
        return jsonify(error=error)
    return 1


# 改变任务描述
@bp.route('/up_content', methods=('GET', 'POST'))
def up_content():
    if request.method == 'POST':
        content = request.form['content']
        error = None
        if content is None:
            error = 'Error content.'

        if error is None:
            sql = 'update mission set content = %s' % (content,)
            success = up(sql)
            return jsonify(success=success)
        return jsonify(error=error)
    return 1


# 改变图片1
@bp.route('/up_picture_url_1', methods=('GET', 'POST'))
def up_picture_url_1():
    if request.method == 'GET':
        picture_url_1 = request.args['picture_url_1']
        error = None
        if picture_url_1 is None:
            error = 'Error picture_url_1.'

        if error is None:
            sql = 'update mission set picture_url_1 = %s' % (picture_url_1,)
            success = up(sql)
            return jsonify(success=success)
        return jsonify(error=error)
    return 1


# 改变图片2
@bp.route('/up_picture_url_2', methods=('GET', 'POST'))
def up_picture_url_2():
    if request.method == 'GET':
        picture_url_2 = request.args['picture_url_2']
        error = None
        if picture_url_2 is None:
            error = 'Error picture_url_2.'

        if error is None:
            sql = 'update mission set picture_url_2 = %s' % (picture_url_2,)
            success = up(sql)
            return jsonify(success=success)
        return jsonify(error=error)
    return 1


# 改变图片3
@bp.route('/up_picture_url_3', methods=('GET', 'POST'))
def up_picture_url_3(picture_url_3):
    if request.method == 'GET':
        picture_url_3 = request.args['picture_url_3']
        error = None
        if picture_url_3 is None:
            error = 'Error picture_url_3.'

        if error is None:
            sql = 'update mission set picture_url_3 = %s' % (picture_url_3,)
            success = up(sql)
            return jsonify(success=success)
        return jsonify(error=error)
    return 1


# 改变赏金
@bp.route('/upmoney', methods=('GET', 'POST'))
def upmoney():
    if request.method == 'POST':
        money = request.form['money']
        error = None
        if money < 0:
            error = 'Error money.'

        if error is None:
            sql = 'update mission set Money = %s' % (money,)
            success = up(sql)
            return jsonify(success=success)
        return jsonify(error=error)
    return 1


# 给予任务评价
@bp.route('/upevaluate', methods=('GET', 'POST'))
def upevaluate():
    if request.method == 'POST':
        evaluate = request.form['evaluate']
        error = None
        if evaluate is None:
            error = 'Error evaluate.'

        if error is None:
            sql = 'update mission set evaluate = %s' % (evaluate,)
            success = up(sql)
            return jsonify(success=success)
        return jsonify(error=error)
    return 1


# 删除或反删除任务
@bp.route('/deleteorNot', methods=('GET', 'POST'))
def deleteorNot(id, isdeleted):  # 如果删除传入ideleted = 1, 如果恢复 = 0
    if request.method == 'POST':
        error = None
        if id < 0:
            error = 'Error Mission_id.'

        if error is None:
            sql = 'update mission set is_deleted = {this_ifShow} where id = {this_Mission_id}'.format(
                this_ifShow=isdeleted, this_Mission_id=id)
            success = up(sql)
            return jsonify(success=success)
        return jsonify(error=error)
    return 1


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
            return jsonify(status='error', error='Data acquisition failure')

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

        # 获取帖子的id用来命名图片
        cur.execute('''select max(id) from mission''')
        post_id = int(cur.fetchone()[0]) + 1
        db.close()
        # 重写文件名，保存图片
        p1_name = None
        p2_name = None
        p3_name = None
        if picture_num >= 1 and allowed_file(picture_1.filename):
            p1_name = secure_filename(picture_1.filename)
            p1_name = 'post_id_' + str(post_id) + '_picture_1' + '.' + p1_name.rsplit('.', 1)[1].lower()
            picture_1.save(os.path.join('''./static/mission_pictures''', p1_name))

        if picture_num >= 2 and allowed_file(picture_2.filename):
            p2_name = secure_filename(picture_2.filename)
            p2_name = 'post_id_' + str(post_id) + '_picture_2' + '.' + p2_name.rsplit('.', 1)[1].lower()
            picture_2.save(os.path.join('''./static/mission_pictures''', p2_name))

        if picture_num >= 3 and allowed_file(picture_3.filename):
            p3_name = secure_filename(picture_3.filename)
            p3_name = 'post_id_' + str(post_id) + '_picture_3' + '.' + p3_name.rsplit('.', 1)[1].lower()
            picture_3.save(os.path.join('''./static/mission_pictures''', p3_name))

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
            db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
            # 使用 cursor() 方法创建一个游标对象 cursor
            cur = db.cursor()
            try:
                cur.execute('''INSERT INTO mission(
                    user_id, 
                    content, 
                    picture_url_1, 
                    picture_url_2, 
                    picture_url_3, 
                    origin, 
                    destination,                           
                    like_number, 
                    comment_number, 
                    end_time,
                    money) VALUES(
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s,
                        %s
                         )''', (user_id,
                                content,
                                p1_name,
                                p2_name,
                                p3_name,
                                origin,
                                destination,
                                0,
                                0,
                                end_time,
                                money
                                ))
                db.commit()
            except:
                db.rollback()
            db.close()
            return jsonify(status='success')
        return jsonify(status=error)
    return 1


# 刷新任务目的地点获取任务的详细信息
@bp.route('/refresh_newest', methods=('GET', 'POST'))
def refresh():
    if request.method == 'POST':
        try:
            destination = request.form['destination']
            tempid = int(request.form['biggest_id'])
        except:
            return jsonify(status='error', error='Data acquisition failure')

        # 打开数据库连接
        db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
        # 使用 cursor() 方法创建一个游标对象 cursor，获取对应的user
        cur = db.cursor()
        # 获取帖子的最大id
        cur.execute('''select max(id) from mission''')
        id = int(cur.fetchone()[0])
        db.close()
        error = None
        if destination is None:
            error = 'Error destination.'
        if tempid is None:
            error = 'Error before'

        if error is None:
            if destination == '随机':
                if id > tempid:
                    json_data2 = search('select * from mission where id > '+str(tempid)+' and is_received = 0 and end_time > current_timestamp limit 40')
                else:
                    data = {'status': "false"}
                    return jsonify(data)

            else:
                print(tempid,destination)
                if id > tempid:
                    json_data2 = search('select * from mission where id > '+str(tempid)+' and destination = '+'destination'+' and is_received = 0 and end_time > current_timestamp limit 40')
                else:
                    data = {'status': "false"}
                    return jsonify(data)

            data={'status': "success", 'data': json_data2}
            return jsonify(data)
        return jsonify(error=error)
    return 1


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
