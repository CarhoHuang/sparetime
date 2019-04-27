# 引用包
import functools, pymysql
from flask import (
    Blueprint, flash, g, request, session, url_for, json, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from dbconfig import *

bp = Blueprint('auth', __name__, url_prefix='/auth')


# 遍历数据库返回所有符合条件的行
@bp.route('/search', methods=('GET', 'POST'))
def search(sql):
    # 打开数据库连接
    db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cur = db.cursor()

    cur.execute(sql)
    user = cur.fetchall()
    db.close()

    json_data = []
    for row in user:
        json_data.append({
            "BeginLocation": row[0],
            "EndLocation": row[1],
            "BeginTime": row[2],
            "EndTime": row[3],
            "label": row[4],
            "description": row[5],
            "photo_location": row[6],
            "ReleaseUser_id": row[7],
            "AcceptUser_id": row[8],
            "Money": row[9],
            "if_finish": row[10],
            "evaluate": row[11],
            "Mission_id": row[12]})

    return json_data


# 通过任务ID获取任务的详细信息
@bp.route('/getMissionByMission_id', methods=('GET', 'POST'))
def getMissionByMission_id(id):
    if request.method == 'GET':
        error = None
        if id < 0:
            error = 'Error Mission_id.'

        if error is None:
            sql = 'select * from mission where id = {this_Mission_id} AND isDeleted = 0'.format(this_Mission_id=id)
            json_data = search(sql)
            data = {"success": 1, "data": json_data}

            return jsonify(data)

        return jsonify(error=error)

    return 1


# 通过任务开始地点获取任务的详细信息
@bp.route('/getMissionByBeginLocation', methods=('GET', 'POST'))
def getMissionByBeginLocation(origin):
    if request.method == 'GET':
        error = None
        if origin is None:
            error = 'Error BeginLocation.'

        if error is None:
            sql = 'select * from misson where origin = {this_BeginLocation} AND isDeleted = 0'.format(
                this_BeginLocation=origin)
            json_data = search(sql)
            data = {"success": 1, "data": json_data}

            return jsonify(data)

        return jsonify(error=error)

    return 1


# 通过任务目的地点获取任务的详细信息
@bp.route('/getMissionByEndLocation', methods=('GET', 'POST'))
def getMissionByEndLocation(destination):
    if request.method == 'GET':
        error = None
        if destination is None:
            error = 'Error EndLocation.'

        if error is None:
            sql = 'select * from misson where destination = {this_EndLocation} AND isDeleted = 0'.format(
                this_EndLocation=destination)
            json_data = search(sql)
            data = {"success": 1, "data": json_data}

            return jsonify(data)

        return jsonify(error=error)

    return 1


# # 通过任务标签获取任务的详细信息
# @bp.route('/getMissionByLabel', methods=('GET', 'POST'))
# def getMissionByLabel(Label):
#     if request.method == 'GET':
#         error = None
#         if Label is None:
#             error = 'Error Label.'
#
#         if error is None:
#             sql = 'select * from Mission where Label = {this_Label} AND ifShow = 1'.format(this_Label=Label)
#             json_data = search(sql)
#             data = {"success": 1, "data": json_data}
#
#             return jsonify(data)
#
#         return jsonify(error=error)
#
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
@bp.route('/upBeginLocation', methods=('GET', 'POST'))
def upBeginLocation(origin):
    if request.method == 'POST':
        error = None
        if origin is None:
            error = 'Error BeginLocation.'

        if error is None:
            sql = 'update misson set origin = {this_BeginLocation}'.format(this_BeginLocation=origin)
            success = up(sql)

            return jsonify(success=success)

        return jsonify(error=error)

    return 1


# 改变任务目的地点
@bp.route('/upEndLocation', methods=('GET', 'POST'))
def upEndLocation(destination):
    if request.method == 'POST':
        error = None
        if destination is None:
            error = 'Error EndLocation.'

        if error is None:
            sql = 'update misson set destination = {this_EndLocation}'.format(this_EndLocation=destination)
            success = up(sql)

            return jsonify(success=success)

        return jsonify(error=error)

    return 1


# 改变任务截止时间
@bp.route('/upEndTime', methods=('GET', 'POST'))
def upEndTime(endtime):
    if request.method == 'POST':
        error = None
        if endtime is None:
            error = 'Error EndTime.'

        if error is None:
            sql = 'update misson set endtime = {this_EndTime}'.format(this_EndTime=endtime)
            success = up(sql)

            return jsonify(success=success)

        return jsonify(error=error)

    return 1


# # 改变任务标签
# @bp.route('/upLable', methods=('GET', 'POST'))
# def upLable(label):
#     if request.method == 'POST':
#         error = None
#         if label is None:
#             error = 'Error label.'
#
#         if error is None:
#             sql = 'update Mission set label = {this_label}'.format(this_label=label)
#             success = up(sql)
#
#             return jsonify(success=success)
#
#         return jsonify(error=error)
#
#     return 1


# 改变任务描述
@bp.route('/upDescription', methods=('GET', 'POST'))
def upDescription(content):
    if request.method == 'POST':
        error = None
        if content is None:
            error = 'Error description.'

        if error is None:
            sql = 'update misson set content = {this_description}'.format(this_description=content)
            success = up(sql)

            return jsonify(success=success)

        return jsonify(error=error)

    return 1


# 改变图片1
@bp.route('/upPhoto_location', methods=('GET', 'POST'))
def upPhoto_location1(picture_url_1):
    if request.method == 'POST':
        error = None
        if picture_url_1 is None:
            error = 'Error photo_location.'

        if error is None:
            sql = 'update misson set picture_url_1 = {this_photo_location}'.format(this_photo_location=picture_url_1)
            success = up(sql)

            return jsonify(success=success)

        return jsonify(error=error)

    return 1


# 改变图片2
@bp.route('/upPhoto_location', methods=('GET', 'POST'))
def upPhoto_location2(picture_url_2):
    if request.method == 'POST':
        error = None
        if picture_url_2 is None:
            error = 'Error photo_location.'

        if error is None:
            sql = 'update misson set picture_url_2 = {this_photo_location}'.format(this_photo_location=picture_url_2)
            success = up(sql)

            return jsonify(success=success)

        return jsonify(error=error)

    return 1


# 改变图片3
@bp.route('/upPhoto_location', methods=('GET', 'POST'))
def upPhoto_location3(picture_url_3):
    if request.method == 'POST':
        error = None
        if picture_url_3 is None:
            error = 'Error photo_location.'

        if error is None:
            sql = 'update misson set picture_url_3 = {this_photo_location}'.format(this_photo_location=picture_url_3)
            success = up(sql)

            return jsonify(success=success)

        return jsonify(error=error)

    return 1


# 改变赏金
@bp.route('/upMoney', methods=('GET', 'POST'))
def upMoney(money):
    if request.method == 'POST':
        error = None
        if money < 0:
            error = 'Error Money.'

        if error is None:
            sql = 'update misson set Money = {this_Money}'.format(this_Money=money)
            success = up(sql)

            return jsonify(success=success)

        return jsonify(error=error)

    return 1


# # 改变任务完成状态
# @bp.route('/upIf_finish', methods=('GET', 'POST'))
# def upIf_finish(if_finish):
#     if request.method == 'POST':
#         error = None
#
#         if error is None:
#             sql = 'update Mission set if_finish = {this_if_finish}'.format(this_if_finish=if_finish)
#             success = up(sql)
#
#             return jsonify(succ ess=success)
#
#         return jsonify(error=error)
#
#     return 1


# 给予任务评价
@bp.route('/upEvaluate', methods=('GET', 'POST'))
def upEvaluate(evaluate):
    if request.method == 'POST':
        error = None
        if evaluate is None:
            error = 'Error evaluate.'

        if error is None:
            sql = 'update misson set evaluate = {this_evaluate}'.format(this_evaluate=evaluate)
            success = up(sql)

            return jsonify(success=success)

        return jsonify(error=error)

    return 1


# 删除或反删除任务
@bp.route('/deleteOrNot', methods=('GET', 'POST'))
def deleteOrNot(id, isDeleted):  # 如果删除传入idDeleted = 1, 如果恢复 = 0
    if request.method == 'POST':
        error = None
        if id < 0:
            error = 'Error Mission_id.'

        if error is None:
            sql = 'update misson set isDeleted = {this_ifShow} where id = {this_Mission_id}'.format(
                this_ifShow=isDeleted, this_Mission_id=id)
            success = up(sql)

            return jsonify(success=success)

        return jsonify(error=error)

    return 1


# 向Mission表插入新的行
@bp.route('/insert', methods=('GET', 'POST'))
def insert(origin, destination, endtime, content, picture_url_1, picture_url_2, picture_url_3, money, evaluate, id,
           ReleaseUser_id=0,
           AcceptUser_id=0):
    if request.method == 'POST':
        error = None
        if origin is None:
            error = 'Error BeginLocation.'
        if destination is None:
            error = 'Error EndLocation.'
        if endtime is None:
            error = 'Error EndTime.'
        if content is None:
            error = 'Error description.'
        # if ReleaseUser_id < 0:
        #     error = 'Error ReleaseUser_id.'
        # if AcceptUser_id < 0:
        #     error = 'Error AcceptUser_id.'
        if money < 0:
            error = 'Error Money.'
        if id < 0:
            error = 'Error Mission_id.'

        if error is None:
            sql = '''INSERT INTO misson(
                origin, 
                destination, 
                endtime, 
                content, 
                picture_url_1, 
                picture_url_2, 
                picture_url_3,                           
                Money, 
                if_finish, 
                evaluate, 
                id, 
                isDeleted) VALUES(
                    {this_BeginLocation}, 
                    {this_EndLocation}, 
                    {this_EndTime}, 
                    {this_description}, 
                    {this_photo_location1}, 
                    {this_photo_location2}, 
                    {this_photo_location3}, 
                    # {this_ReleaseUser_id}, 
                    # {this_AcceptUser_id}, 
                    {this_Money}, 
                    0, 
                    {this_evaluate}, 
                    {this_Mission_id}, 
                    1)'''.format(
                this_BeginLocation=origin,
                this_EndLocation=destination,
                this_EndTime=endtime,
                this_description=content,
                this_photo_location1=picture_url_1,
                this_photo_location2=picture_url_2,
                this_photo_location3=picture_url_3,
                # this_ReleaseUser_id=ReleaseUser_id,
                # this_AcceptUser_id=AcceptUser_id,
                this_Money=money,
                this_evaluate=evaluate,
                this_Mission_id=id)
            success = up(sql)

            return jsonify(success=success)

        return jsonify(error=error)

    return 1
