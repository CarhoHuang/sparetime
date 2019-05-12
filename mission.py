# 引用包
import functools, pymysql
from flask import (
    Blueprint, flash, g, request, session, url_for, json, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from dbconfig import *

bp = Blueprint('mission', __name__, url_prefix='/mission')


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
            "isdeleted": row[10],
            "endtime": row[11],
            "money": row[12],
            "evaluate": row[13],
            "receiver_id": row[14]}})
    return json_data


# 通过任务ID获取任务的详细信息
@bp.route('/getMissionByMission_id', methods=('GET', 'POST'))
def getMissionByMission_id():
    if request.method == 'POST':
        id = request.form['id']
        error = None
        if id is None:
            error = 'Error id.'

        if error is None:
            sql = 'select * from mission where id = %s and isdeleted = 0' % (id,)
            json_data = search(sql)
            data = {'status': "success", 'posts': json_data}
            return jsonify(data)
        return jsonify(error=error)
    return 1


# 通过任务开始地点获取任务的详细信息
@bp.route('/getMissionByorigin', methods=('GET', 'POST'))
def getMissionByorgin():
    if request.method == 'POST':
        origin = request.form['origin']
        error = None
        if origin is None:
            error = 'Error origin.'

        if error is None:
            sql = 'select * from mission where origin = %s and isdeleted =0' % (origin,)
            json_data = search(sql)
            data = {'status': "success", 'posts': json_data}
            return jsonify(data)
        return jsonify(error=error)
    return 1


# 通过任务目的地点获取任务的详细信息
@bp.route('/getMissionBydestination', methods=('GET', 'POST'))
def getMissionBydestination():
    if request.method == 'POST':
        destination = request.form['destination']
        error = None
        if destination is None:
            error = 'Error destination.'

        if error is None:
            sql = 'select * from mission where destination = %s and isdeleted =0' % (destination,)
            json_data = search(sql)
            data = {'status': "success", 'posts': json_data}
            return jsonify(data)
        return jsonify(error=error)
    return 1


# # 通过任务标签获取任务的详细信息
# @bp.route('/getMissionBylabel', methods=('GET', 'POST'))
# def getMissionBylabel(label):
#     if request.method == 'POST':
#         label = request.form['label']
#         error = None
#         if Label is None:
#             error = 'Error label.'
#
#         if error is None:
#             sql = 'select * from Mission where label = %s and isdeleted = 0' % (label,)
#             json_data = search(sql)
#             data = {'status': "success", 'posts': json_data}
#             return jsonify(data)
#         return jsonify(error=error)
#     return 1


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
@bp.route('/uporigin', methods=('GET', 'POST'))
def uporigin():
    if request.method == 'POST':
        origin = request.form['origin']
        error = None
        if origin is None:
            error = 'Error origin.'

        if error is None:
            sql = 'update mission set origin = %s' % (origin,)
            success = up(sql)
            return jsonify(success=success)
        return jsonify(error=error)
    return 1


# 改变任务目的地点
@bp.route('/updestination', methods=('GET', 'POST'))
def updestination():
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
@bp.route('/upendtime', methods=('GET', 'POST'))
def upendTime():
    if request.method == 'POST':
        endtime = request.form['endtime']
        error = None
        if endtime is None:
            error = 'Error EndTime.'

        if error is None:
            sql = 'update mission set endtime = %s' % (endtime,)
            success = up(sql)
            return jsonify(success=success)
        return jsonify(error=error)
    return 1


# # 改变任务标签
# @bp.route('/uplable', methods=('GET', 'POST'))
# def uplable(label):
#     if request.method == 'POST':
#         label = request.form['label']
#         error = None
#         if label is None:
#             error = 'Error label.'
#
#         if error is None:
#             sql = 'update Mission set label = %s' % (label,)
#             success = up(sql)
#             return jsonify(success=success)
#         return jsonify(error=error)
#     return 1


# 改变任务描述
@bp.route('/upcontent', methods=('GET', 'POST'))
def upcontent():
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


# # 改变任务完成状态
# @bp.route('/upIf_finish', methods=('GET', 'POST'))
# def upIf_finish(if_finish):
#     if_finish = request.form['if_finish']
#     if request.method == 'POST':
#         error = None
#
#         if error is None:
#             sql = 'update Mission set if_finish = %s' % (if_finish,)
#             success = up(sql)
#             return jsonify(success=success)
#         return jsonify(error=error)
#     return 1


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
            sql = 'update mission set isDeleted = {this_ifShow} where id = {this_Mission_id}'.format(
                this_ifShow=isdeleted, this_Mission_id=id)
            success = up(sql)
            return jsonify(success=success)
        return jsonify(error=error)
    return 1


# 向mission表插入新的行
@bp.route('/insert', methods=('GET', 'POST'))
def insert():
    if request.method == 'POST':
        user_id = request.form['user_id']
        content = request.form['content']
        picture_url_1 = request.form['picture_url_1']
        picture_url_2 = request.form['picture_url_2']
        picture_url_3 = request.form['picture_url_3']
        origin = request.form['origin']
        destination = request.form['destination']
        like_number = request.form['like_number']
        comment_number = request.form['comment_number']
        id = request.form['id']
        isdeleted = request.form['isdeleted']
        endtime = request.form['endtime']
        money = request.form['money']
        evaluate = request.form['evaluate']
        receiver_id = request.form['receiver_id']
        error = None

        if user_id is None:
            error = 'Error user_id.'
        if content is None:
            error = 'Error content.'
        if picture_url_1 is None:
            error = 'Error picture_url_1.'
        if picture_url_2 is None:
            error = 'Error picture_url_2.'
        if picture_url_3 is None:
            error = 'Error picture_url_3.'
        if origin is None:
            error = 'Error origin.'
        if destination is None:
            error = 'Error destination.'
        if like_number is None:
            error = 'Error like_number.'
        if comment_number is None:
            error = 'Error comment_number.'
        if id is None:
            error = 'Error id.'
        if isdeleted is None:
            error = 'Error isdeleted.'
        if endtime is None:
            error = 'Error endtime.'
        if money is None:
            error = 'Error money.'
        if evaluate is None:
            error = 'Error evaluate.'
        if receiver_id is None:
            error = 'Error receiver_id.'

        if error is None:
            sql = '''INSERT INTO mission(
                user_id, 
                content, 
                picture_url_1, 
                picture_url_2, 
                picture_url_3, 
                origin, 
                destination,                           
                like_number, 
                comment_number, 
                id, 
                isdeleted, 
                endtime,
                money,
                evaluate,
                receiver_id,) VALUES(
                    {this_user_id}, 
                    {this_content}, 
                    {this_picture_url_1}, 
                    {this_picture_url_2}, 
                    {this_picture_url_3}, 
                    {this_origin}, 
                    {this_destination}, 
                    {this_like_number}, 
                    {this_comment_number}, 
                    {this_id}, 
                    {this_isdeleted}, 
                    {this_endtime}, 
                    {this_money}, 
                    {this_evaluate}, 
                    {this_receiver_id}, 
                     )'''.format(
                this_user_id=user_id,
                this_content=content,
                this_picture_url_1=picture_url_1,
                this_picture_url_2=picture_url_2,
                this_picture_url_3=picture_url_3,
                this_origin=origin,
                this_destination=destination,
                this_like_number=like_number,
                this_comment_number=comment_number,
                this_id=id,
                this_isdeleted=isdeleted,
                this_endtime=endtime,
                this_money=money,
                this_evaluate=evaluate,
                this_receiver_id=receiver_id)
            success = up(sql)
            return jsonify(success=success)
        return jsonify(error=error)
    return 1
