import os
import time

from bson import ObjectId
from flask import Blueprint, jsonify, send_file, request

from Config import RET, MongoDB
from baiduAi import text2audio
from myRedis import get_msg

friend = Blueprint("friends", __name__)


@friend.route("/friend_list", methods=['POST'])
def friend_list():
    user_id = request.form.to_dict()
    # print(user_id)
    user_info = MongoDB.users.find_one({'_id': ObjectId(user_id['_id'])})

    if user_info:
        RET['CODE'] = 0
        RET['MSG'] = '好友查询'
        RET['DATA'] = user_info.get('friend_list')

    return jsonify(RET)


@friend.route("/chat_list", methods=['POST'])
def chat_list():
    chat_info = request.form.to_dict()
    chat_id = ObjectId(chat_info.get('chat_id'))

    # 查询聊天记录
    chat_window = MongoDB.chats.find_one({'_id': chat_id})
    # print(chat_id)
    # 获取聊条记录
    chat_window_list = chat_window.get('chat_list')[-5:]
    RET['CODE'] = 0
    RET['MSG'] = '好友查询'
    RET['DATA'] = chat_window_list

    # 清空列表

    get_msg(chat_info.get('from_user'),chat_info.get('to_user'))
    return jsonify(RET)


@friend.route('/recv_msg', methods=['post'])
def recv_msg():
    chat_info = request.form.to_dict()
    sender = chat_info.get('from_user')
    receiver = chat_info.get('to_user')
    count,sender = get_msg(sender,receiver)
    # print(count)

    user_list = [sender, receiver]

    # 子集查询
    chat_win = MongoDB.chats.find_one({'user_list': {'$all': user_list}})

    # 收到最后一条消息
    ch = chat_win.get('chat_list')[-count:]
    ch.reverse()

    #当收取消息时，不知道是谁发的
    #text = '以下是来自xxx的消息'

    remark = '小伙伴'
    toy = MongoDB.toys.find_one({'_id': ObjectId(receiver)})
    for friend in toy.get('friend_list'):
        if friend.get('friend_id') == sender:
            remark = friend.get('friend_remark')

    text = f'以下是来自{remark}的{count}条消息'
    hite = text2audio(text)  # 提示语音

    xx_dict = {
        'from_user':sender,
        'to_user':receiver,
        'chat':hite,
        'createTime':time.time(),
    }
    ch.append(xx_dict)

    return jsonify(ch)


@friend.route('/add_req',methods=['POST'])
def add_req():
    req_info = request.form.to_dict()
    req_info['status'] = 0
    toy = MongoDB.toys.find_one({'_id':ObjectId(req_info.get('toy_id'))})

    #根据好友类型查找不同的主动添加方的类型: toy/app
    if req_info.get('add_type') == 'toy':
        user_info = MongoDB.toys.find_one({'_id':ObjectId(req_info.get('add_user'))})
    else:
        user_info = MongoDB.users.find_one({'_id':ObjectId(req_info.get('add_user'))})

    req_info['avatar'] = user_info.get('avatar')
    req_info['nickname'] = user_info.get('nickname') if user_info.get('nickname') else user_info.get("toy_name")
    req_info['toy_name'] = toy.get('toy_name')

    MongoDB.request.insert_one(req_info)

    RET['CODE'] = 0
    RET['MSG'] = '添加好友请求成果'
    RET['DATA'] = {}

    return jsonify(RET)

@friend.route('/req_list',methods=['POST'])
def req_list():
    # user_id
    _id = request.form.get('user_id')

    user_info = MongoDB.users.find_one({'_id':ObjectId(_id)})
    bind_toys = user_info.get('bind_toys')

    # 在request表中，查询当前用户的绑定玩具，那些玩具收到好友请求
    toy_req_list = list(MongoDB.request.find({'toy_id':{'$in':bind_toys}}))

    # print(toy_req_list)
    for index,req in enumerate(toy_req_list):
        toy_req_list[index]['_id'] = str(req.get('_id'))

    RET['CODE'] = 0
    RET['MSG'] = '查询好友请求'
    RET['DATA'] = toy_req_list
    return jsonify(RET)


@friend.route("/ref_req",methods=['POST'])
def ref_req():
    req_id = request.form.get('req_id')
    MongoDB.request.update_one({'_id':ObjectId(req_id)},{'$set':{'status':2}})

    RET['CODE'] = 0
    RET['MSG'] = '拒绝好友请求'
    RET['DATA'] = {}
    return jsonify(RET)

@friend.route("/acc_req",methods=['POST'])
def acc_req():
    # 请求的id
    req_id = request.form.get('req_id')
    #对请求方的备注
    remark = request.form.get('remark')

    # 请求的具体信息
    req_info = MongoDB.request.find_one({"_id":ObjectId(req_id)})

    # 查询接收方toy的信息 -request数据表中的 toy_id
    toy_info = MongoDB.toys.find_one({'_id':ObjectId(req_info.get('toy_id'))})

    # 创建聊天窗口
    chat_window = MongoDB.chats.insert_one({'user_list':[req_info.get('add_user'),req_info.get('toy_id')],'chat_list':[]})

    #添加好友 - 双方通讯录中  相互交换名片
    # 先来制作各自的名片
    # 被加好友的名片：add_user 添加toy的名片, 即发起方添加接收方的名片

    add_user_add_toy = {  #记录接收方的信息，所以要放到发起方的friend_list中，接收方永远是toy
        "friend_id":req_info.get('toy_id'),
        'friend_nick':toy_info.get('toy_name') ,
        'friend_remark':req_info.get('remark') , # 发起方在发起时的备注
        'friend_avatar':toy_info.get('avatar') ,
        'friend_chat':str(chat_window.inserted_id),   # 新建聊天窗口
        'friend_type':'toy',
    }



    # 制作发起方信息，放到接收方friend_list中
    toy_add_add_user = {
        "friend_id":req_info.get('add_user'),
        'friend_nick':req_info.get('nickname') ,
        'friend_remark':remark, # 发起方的备注- 同意之后的备注
        'friend_avatar':req_info.get('avatar') ,
        'friend_chat':str(chat_window.inserted_id),   # 新建聊天窗口
        'friend_type':req_info.get('add_type'),
    }

    #2.将名片添加到add_user的friend_list中,接收方添加发起方的数据
    if req_info.get('add_type') == 'toy':
        MongoDB.toys.update_one({'_id':ObjectId(req_info.get('add_user'))},{'$push':{'friend_list':add_user_add_toy}})
    else:
        MongoDB.users.find_one({'_id': ObjectId(req_info.get('add_user'))},{'$push':{'friend_list':add_user_add_toy}})

    # 发起方添加接收方的数据
    MongoDB.toys.update_one({'_id': ObjectId(req_info.get('toy_id'))}, {'$push': {'friend_list':toy_add_add_user }})

    # 将request表中的记录状态改为1
    MongoDB.request.update_one({'_id': ObjectId(req_id)}, {'$set': {'status': 1}})
    RET['CODE'] = 0
    RET['MSG'] = '同意'
    RET['DATA'] = {}
    return jsonify(RET)
