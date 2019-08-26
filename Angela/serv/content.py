import os

from flask import Blueprint, jsonify, send_file
from Config import RET, MongoDB, COVER_PATH, MUSIC_PATH, QRCODE_PATH, CHAT_PATH

content = Blueprint("content", __name__)


@content.route("/content_list", methods=['POST'])
def content_list():
    con_list = list(MongoDB.Content.find({}))
    for index, cont in enumerate(con_list):
        con_list[index]['_id'] = str(cont.get('_id'))

    RET['CODE'] = 0
    RET['MSG'] = '获取内容列表'
    RET['data'] = con_list

    return jsonify(RET)


@content.route("/get_cover/<filename>", methods=['GET'])
def cover_list(filename):
    file_path = os.path.join(COVER_PATH, filename)
    return send_file(file_path)


@content.route("/get_music/<filename>", methods=['GET'])
def music_list(filename):
    file_path = os.path.join(MUSIC_PATH, filename)
    return send_file(file_path)

@content.route("/get_qr/<filename>", methods=['GET'])
def qr_list(filename):
    file_path = os.path.join(QRCODE_PATH, filename)
    return send_file(file_path)


@content.route("/get_chat/<filename>", methods=['GET'])
def chat_list(filename):
    file_path = os.path.join(CHAT_PATH, filename)
    return send_file(file_path)