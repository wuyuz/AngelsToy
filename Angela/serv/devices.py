import os
from bson import ObjectId
from flask import Blueprint, jsonify, send_file, request
from Config import RET, MongoDB, QRCODE_PATH

devices = Blueprint("device", __name__)


@devices.route('/scan_qr', methods=['POST'])
def scan_qr():
    device_key = request.form.to_dict()
    device = MongoDB.devices.find_one(device_key)
    if device:
        RET["CODE"] = 0
        RET["MSG"] = "二维码扫描成功"
        RET["DATA"] = device_key

        # 在玩具表中查找是否存在，如果存在，则是绑定好友过程
        toy = MongoDB.toys.find_one(device_key)
        if toy:
            RET["CODE"] = 2
            RET["MSG"] = "设备已经进行绑定"
            RET["DATA"] = {'toy_id':str(toy.get('_id'))}

    else:
        RET["CODE"] = 1
        RET["MSG"] = "二维码扫描失败"
        RET["DATA"] = {}

    return jsonify(RET)


@devices.route('/bind_toy', methods=['POST'])
def bind_toy():
    toy_info = request.form.to_dict()
    user_id = toy_info.pop('user_id') # 找出用户id
    user_info = MongoDB.users.find_one({'_id':ObjectId(user_id)}) #通过用户id找出用户信息

    chat_window = MongoDB.chats.insert_one({'user_list':[],'chat_list':[]})
    chat_id = str(chat_window.inserted_id)  # 获取插入的数据的object_id

    # 创建toy在friendlist的名片
    toy_add_user = {
        'friend_id': user_id,
        'friend_nick':user_info.get('username'),  # 绑定的是用户的信息
        'friend_remark':toy_info.get('remark'),
        'friend_avatar':user_info.get('avatar'),
        'friend_chat':chat_id,
        'friend_type':'app',
    }
    if not toy_info.get('friend_list'):
        toy_info['friend_list'] = []

    toy_info['friend_list'].append(toy_add_user)
    toy_info['bind_user'] = user_id
    toy_info['avatar'] = 'toy.jpg'

    # 创建玩具
    toy = MongoDB.toys.insert_one(toy_info)
    toy_id = str(toy.inserted_id)


    user_info['bind_toys'].append(toy_id)

    # 创建user在friend_list的名片
    user_add_toy = {
        "friend_id":toy_id,
        'friend_nick':toy_info.get('toy_name'),
        'friend_remark':toy_info.get('baby_name'),
        'friend_avatar':toy_info.get('avatar'),
        'friend_chat':chat_id,
        'friend_type':'toy',
    }

    user_info['friend_list'].append(user_add_toy)

    # 更新user
    MongoDB.users.update_one({'_id':ObjectId(user_id)},{'$set':user_info})

     #聊天窗口
    MongoDB.chats.update_one({'_id':ObjectId(chat_id)},{'$set':{'user_list':[toy_id,user_id]}})

    RET['CODE'] = 0
    RET['MSG'] = '绑定完成'
    RET['DATA'] = {}

    return jsonify(RET)


@devices.route('/toy_list', methods=['post'])
def toy_list():
    user_id = request.form.get('_id')
    user_bind_toy_list = list(MongoDB.toys.find({'bind_user': user_id}))
    for index, item in enumerate(user_bind_toy_list):
        user_bind_toy_list[index]['_id'] = str(item.get('_id'))

    RET['CODE'] = 0
    RET['MSG'] = '绑定完成'
    RET['DATA'] = user_bind_toy_list

    return jsonify(RET)



@devices.route('/open_toy', methods=['post'])
def toy_open():
    device_key = request.form.to_dict()

    device_toy = MongoDB.toys.find_one(device_key)
    device = MongoDB.devices.find_one(device_key)
    # print(device,device_toy,device_key)

    RET = {}
    if device_toy: # 正在使用的设备
        RET['code'] = 0
        RET['music'] = 'success.mp3'
        RET['toy_id'] = str(device_toy['_id'])
        RET['name'] = device_toy['toy_name']
        return jsonify(RET)

    elif device:  # 未绑定的设备
        RET['code'] = 2
        RET['music'] = 'nil.mp3'
        return jsonify(RET)

    else:  #  没有绑定的设备，且没有使用的
        RET['code'] = 1
        RET['music'] = 'nodev.mp3'
        return jsonify(RET)




