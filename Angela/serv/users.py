import json
import os
from bson import ObjectId
from flask import Blueprint, jsonify, send_file, request
from Config import RET, MongoDB, QRCODE_PATH, RDB
from myRedis import get_msg

user = Blueprint("users", __name__)


@user.route("/reg", methods=['POST'])
def reg():
    user_info = request.form.to_dict()
    user_info['avatar'] = 'baba.jpg' if user_info.get('gender') == '2' else 'mama.jpg'
    user_info['bind_toys'] = []
    user_info['friend_list'] = []
    MongoDB.users.insert_one(user_info)

    RET['CODE'] = 0
    RET['MSG'] = '注册成功'
    RET['DATA'] = {}

    return jsonify(RET)


def get_chat(receiver):
    msg_count = RDB.get(receiver)
    msg_count_dict = {'count':0}
    if msg_count:
        msg_count_dict = json.loads(msg_count)
        msg_count_dict['count'] = sum(msg_count_dict.values())

    return msg_count_dict


@user.route('/login', methods=['POST'])
def login():
    user_dict = request.form.to_dict()
    user_info = MongoDB.users.find_one(user_dict, {'password': 0})  # 将查询的对象的password字段排除
    user_info['_id'] = str(user_info.get('_id'))
    user_dict['chat'] = get_chat(user_info['_id'])

    RET['CODE'] = 0
    RET['MSG'] = '登陆成功'
    RET['DATA'] = user_info

    return jsonify(RET)


@user.route('/auto_login', methods=['POST'])
def auto_login():
    user_info = request.form.to_dict()

    user_info['_id'] = ObjectId(user_info.pop('_id'))

    user_dict = MongoDB.users.find_one(user_info)

    if user_dict:
        user_dict['_id'] = str(user_dict['_id'])

    user_dict['chat'] = get_chat(user_dict['_id'])

    RET['DATA'] = user_dict


    return jsonify(RET)
