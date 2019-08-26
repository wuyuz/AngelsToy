import os
import time
import uuid
from bson import ObjectId
from flask import Blueprint, jsonify, send_file, request
from Config import RET, MongoDB, CHAT_PATH
from baiduAi import text2audio, my_nlp_lowB, audio2text
from myRedis import set_msg

uploaders = Blueprint("uploader", __name__)

@uploaders.route('/app_uploader', methods=['POST'])
def app_uploader():
    app_info = request.form.to_dict()

    user_list = [app_info.get('user_id'), app_info.get('to_user')]  # 用于查询chat
    # chat_window = MongoDB.chats.find_one({'user_list':{'$all':user_list}}) # 子集查询

    file = request.files.get('reco_file')
    file_path = os.path.join(CHAT_PATH, file.filename)
    file.save(file_path)

    os.system(f'ffmpeg -i {file_path} {file_path}.mp3')  # 修改格式
    os.remove(file_path)

    chat_info = {
        "from_user": app_info.get('user_id'),
        "to_user": app_info.get('to_user'),
        'friend_type': app_info.get('friend_type'),
        "chat": f"{file.filename}.mp3",
        "createTime": time.time()
    }

    MongoDB.chats.update_one({'user_list': {'$all': user_list}}, {'$push': {'chat_list': chat_info}})
    set_msg(app_info.get('user_id'), app_info.get('to_user'))

    # user = MongoDB.users.find_one({'_id': ObjectId(app_info.get('user_id'))})
    # text = f"你有一条来自{user['nickname']}的消息"
    # hite = text2audio(text)  # 提示语音

    # 收取语音的永远是玩具
    remark = '小伙伴'
    toy = MongoDB.toys.find_one({'bind_user': app_info.get('user_id')})
    for friend in toy.get('friend_list'):
        if friend.get('friend_id') == app_info.get('user_id'):
            remark = friend.get('friend_remark')

    text = f'你有来自{remark}的新消息'
    hite = text2audio(text)  # 提示语音

    RET['CODE'] = 0
    RET['MSG'] = '上传成功'
    RET['DATA'] = {
        'filename': hite,
        'friend_type': 'app',
        'name1':remark,
    }

    return jsonify(RET)


@uploaders.route('/toy_uploader', methods=['POST'])
def toy_uploader():
    app_info = request.form.to_dict()
    # 接收app传递的消息
    # print(app_info)  # {'user_id': '5d5a59d1663d3980814ddffb', 'friend_type': 'undefined', 'to_user': '5d5a59a7663d3980814ddff9'}

    file = request.files.get('reco')
    file_path = os.path.join(CHAT_PATH, file.filename)
    file.save(file_path)

    file_name = uuid.uuid4()
    os.system(f'ffmpeg -i {file_path} {CHAT_PATH}/{file_name}.mp3')  # 修改格式
    os.remove(file_path)
    user_list = [app_info.get('user_id'), app_info.get('to_user')]

    chat_info = {
        "from_user": app_info.get('user_id'),
        "to_user": app_info.get('to_user'),
        "chat": f"{file_name}.mp3",
        "createTime": time.time()
    }
    MongoDB.chats.update_one({'user_list': {'$all': user_list}}, {'$push': {'chat_list': chat_info}})
    set_msg(app_info.get('user_id'), app_info.get('to_user'))
    # 替换返回值中的filename 可以让toy 播放不同的内容


    # 获取自己的好友类型 app/toy
    user = MongoDB.toys.find_one({'_id':ObjectId(app_info.get('user_id'))})
    print(user)
    if user:
        friend_type = 'toy'
    else:
        friend_type = 'app'

    filename = f"{file_name}.mp3"
    # 合成语音提示 - 接收语音语音接收的是toy，意思是发给app就不用合成前一段
    remark = '小伙伴'
    if app_info.get('friend_type') == 'toy':
        toy = MongoDB.toys.find_one({'_id': ObjectId(app_info.get('user_id'))})
        print(toy)
        for friend in toy.get('friend_list'):
            if friend.get('friend_id') == app_info.get('to_user'):
                remark = friend.get('friend_nick')

        text = f'你有来自{remark}的新消息'
        filename = text2audio(text)  # 提示语音


    RET['CODE'] = 0
    RET['MSG'] = '上传成功'
    RET['DATA'] = {
        'filename':filename,
        'friend_type': friend_type,
        'name1': remark,
    }

    return jsonify(RET)


@uploaders.route('/ai_uploader', methods=['POST'])
def ai_uploader():
    toy_info = request.form.to_dict()
    file = request.files.get('reco')

    filename = f"{uuid.uuid4()}.wav"
    file_path = os.path.join(CHAT_PATH, filename)
    file.save(file_path)

    # ai 人工智能, 语音转文字，识别成问题
    Q = audio2text(file_path)

    # 点播音乐，可使用短文本相似度
    ret = my_nlp_lowB(Q, toy_info.get('toy_id'))

    # 主动发起消息
    return jsonify(ret)
