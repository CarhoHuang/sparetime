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


# 通过用户ID获取管理员的详细信息
@bp.route('/getAdministratorsByUser_id', methods=('GET', 'POST'))
def getAdministratorsByUser_id(user_id):
    if request.method == 'GET':
        error = None
        if user_id < 0:
            error = 'Error User_id.'

        if error is None:

            sql = 'select * from Administrators where user_id = {this_user_id} AND ifShow = 1'.format(this_user_id = user_id)
            json_data = search(sql)
            data = {"success": 1, "data": json_data}

            return jsonify(data)

        return jsonify(error=error)

    return 1


# 通过管理员ID获取管理员的详细信息
@bp.route('/getAdmByAdm_id', methods=('GET', 'POST'))
def getAdmByAdm_id(Administrators_id):
    if request.method == 'GET':
        error = None
        if Administrators_id < 0:
            error = 'Error Administrators_id.'

        if error is None:

            sql = 'select * from Administrators where Administrators_id = {this_Administrators_id} AND ifShow = 1'.format(this_Administrators_id = Administrators_id)
            json_data = search(sql)
            data = {"success": 1, "data": json_data}

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


# 删除或反删除管理员
@bp.route('/deleteOrNot', methods=('GET', 'POST'))
def deleteOrNot(Administrators_id, ifShowFlag):  # 如果删除传入ifShowFlag = 0, 如果恢复 = 1
    if request.method == 'POST':
        error = None
        if Administrators_id < 0:
            error = 'Error Administrators_id.'

        if error is None:

            sql = 'update Administrators set ifShow = {this_ifShowFlag} where Administrators_id = {this_Administrators_id}'.format(this_ifShowFlag = ifShowFlag, this_Administrators_id = Administrators_id)
            success = up(sql)

            return jsonify(success=success)

        return jsonify(error=error)

    return 1


# 向Administrators表插入新的行
@bp.route('/insert', methods=('GET', 'POST'))
def insert(user_id, Adminstrators_id):
    if request.method == 'POST':
        error = None
        if user_id < 0:
            error = 'Error user_id.'
        if Adminstrators_id < 0:
            error = 'Error Adminstrators_id.'

        if error is None:

            sql = 'INSERT INTO Administrators(user_id, Administrators, ifShow) VALUES({this_user_id}, {this_Administrators}, 1)'.format(this_user_id = user_id, this_Administrators = Adminstrators_id)
            success = up(sql)

            return jsonify(success=success)

        return jsonify(error=error)

    return 1