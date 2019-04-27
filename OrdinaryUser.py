# 引用包
import functools, pymysql
from flask import (
    Blueprint, flash, g, request, session, url_for, json, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from dbconfig import *

bp = Blueprint('auth', __name__, url_prefix='/auth')

# 通过接受任务的用户对应的ID获取此ID所有接受任务的ID
@bp.route('/getMission_id', methods=('GET', 'POST'))
def getMission_id(ReleaseUser_id):
    if request.method == 'GET':
        error = None
        if ReleaseUser_id < 0:
            error = 'Error ReleaseUser_id.'

        if error is None:

            # 打开数据库连接
            db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
            # 使用 cursor() 方法创建一个游标对象 cursor
            cur = db.cursor()

            cur.execute('select * from ReleaseMission where ReleaseUser_id = %s AND ifShow = 1', (ReleaseUser_id,))
            user = cur.fetchall()
            db.close()

            json_data = []
            for row in user:
                json_data.append({"Mission_id": row[0], "ReleaseUser_id": row[1]})
            data = {"success": 1, "data": json_data}

            return jsonify(data)

        return jsonify(error=error)

    return 1


# 通过任务ID获取发布此任务的用户ID
@bp.route('/getUser_id', methods=('GET', 'POST'))
def getUser_id(Mission_id):
    if request.method == 'GET':
        error = None
        if Mission_id < 0:
            error = 'Error Mission_id.'

        if error is None:

            # 打开数据库连接
            db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
            # 使用 cursor() 方法创建一个游标对象 cursor
            cur = db.cursor()

            cur.execute('select * from ReleaseMission where Mission_id = %s AND ifShow = 1', (Mission_id,))
            user = cur.fetchall()
            db.close()

            json_data = []
            for row in user:
                json_data.append({"Mission_id": row[0], "ReleaseUser_id": row[1]})
            data = {"success": 1, "data": json_data}

            return jsonify(data)

        return jsonify(error=error)

    return 1


# 删除任务或反删除任务
@bp.route('/deleteOrNot', methods=('GET', 'POST'))
def deleteOrNot(Mission_id, ReleaseUser_id, ifShowFlag):  # 如果删除传入ifShowFlag = 0, 如果恢复 = 1
    if request.method == 'POST':
        error = None
        if Mission_id < 0:
            error = 'Error Mission_id.'
        if ReleaseUser_id < 0:
            error = 'Error ReleaseUser_id.'

        if error is None:
            # 打开数据库连接
            db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
            # 使用 cursor() 方法创建一个游标对象 cursor
            cur = db.cursor()

            cur.execute('Update ReleaseMission set ifShow = %s where Mission_id = %s AND ReleaseUser_id = %s', (ifShowFlag, Mission_id, ReleaseUser_id,))
            db.commit()
            db.close()

            return jsonify(success=True)

        return jsonify(error=error)

    return 1


# 向ReleaseMission表插入新的行
@bp.route('/insert', methods=('GET', 'POST'))
def insert(Mission_id, ReleaseUser_id):
    if request.method == 'POST':
        error = None
        if Mission_id < 0:
            error = 'Error Mission_id.'
        if ReleaseUser_id < 0:
            error = 'Error ReleaseUser_id.'

        if error is None:
            # 打开数据库连接
            db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
            # 使用 cursor() 方法创建一个游标对象 cursor
            cur = db.cursor()

            cur.execute('INSERT INTO ReleaseMission(Mission_id, ReleaseUser_id, ifShow) VALUES(%s, %s, 1)', (Mission_id, ReleaseUser_id,))
            db.commit()
            db.close()

            return jsonify(success=True)

        return jsonify(error=error)

    return 1