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
def getMission_id(AcceptUser_id):
    if request.method == 'GET':
        error = None
        if AcceptUser_id < 0:
            error = 'Error User_id.'

        if error is None:

            # 打开数据库连接
            db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
            # 使用 cursor() 方法创建一个游标对象 cursor
            cur = db.cursor()

            cur.execute('select * from AcceptMission where AcceptUser_id = %s AND ifShow = 1', (AcceptUser_id,))
            user = cur.fetchall()
            db.close()

            json_data = []
            for row in user:
                json_data.append({"Mission_id": row[0], "AcceptUser_id": row[1]})
            data = {"success": 1, "data": json_data}

            return jsonify(data)

        return jsonify(error=error)

    return 1


# 通过任务ID获取接受此任务的用户ID
@bp.route('/getAcceptUser_id', methods=('GET', 'POST'))
def getAcceptUser_id(Mission_id):
    if request.method == 'GET':
        error = None
        if Mission_id < 0:
            error = 'Error Mission_id.'

        if error is None:

            # 打开数据库连接
            db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
            # 使用 cursor() 方法创建一个游标对象 cursor
            cur = db.cursor()

            cur.execute('select * from AcceptMission where Mission_id = %s AND ifShow = 1', (Mission_id,))
            user = cur.fetchall()
            db.close()

            json_data = []
            for row in user:
                json_data.append({"Mission_id": row[0], "AcceptUser_id": row[1]})
            data = {"success": 1, "data": json_data}

            return jsonify(data)

        return jsonify(error=error)

    return 1


# 删除任务或反删除任务
@bp.route('/deleteOrNot', methods=('GET', 'POST'))
def deleteOrNot(Mission_id, AcceptUser_id, ifShowFlag):  # 如果删除传入ifShowFlag = 0, 如果恢复 = 1
    if request.method == 'POST':
        error = None
        if Mission_id < 0:
            error = 'Error Mission_id.'
        if AcceptUser_id < 0:
            error = 'Error AcceptUser_id.'

        if error is None:
            # 打开数据库连接
            db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
            # 使用 cursor() 方法创建一个游标对象 cursor
            cur = db.cursor()

            cur.execute('Update AcceptMission set ifShow = %s where Mission_id = %s AND AcceptUser_id = %s', (ifShowFlag, Mission_id, AcceptUser_id,))
            db.commit()
            db.close()

            return jsonify(success=True)

        return jsonify(error=error)

    return 1


# 向AcceptMission表插入新的行
@bp.route('/insert', methods=('GET', 'POST'))
def insert(Mission_id, AcceptUser_id):
    if request.method == 'POST':
        error = None
        if Mission_id < 0:
            error = 'Error Mission_id.'
        if AcceptUser_id < 0:
            error = 'Error AcceptUser_id.'

        if error is None:
            # 打开数据库连接
            db = pymysql.connect("localhost", DBUser, DBPassword, DBName)
            # 使用 cursor() 方法创建一个游标对象 cursor
            cur = db.cursor()

            cur.execute('INSERT INTO AcceptMission(Mission_id, AcceptUser_id, ifShow) VALUES(%s, %s, 1)', (Mission_id, AcceptUser_id,))
            db.commit()
            db.close()

            return jsonify(success=True)

        return jsonify(error=error)

    return 1