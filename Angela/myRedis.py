import json

from Config import RDB

def set_msg(sender,receiver):
    #设置未读消息
    #1.当前没有receiver的数据，创建receiver的字典
    #2。当receiver收到sender的消息，对应当前sender + 1
    #数据结构： receiver ： {sender1:1,sender2；0}
    #sener 向receiver 发起消息时， 向receiver的数据中 +1 或创建
    msg_count = RDB.get(receiver)
    if msg_count:
        # 当前数据已经存在
        msg_count_dict = json.loads(msg_count)
        if msg_count_dict.get(sender):
            # sender是不是第一次给receiver发消息
            msg_count_dict[sender] += 1
        else:
            msg_count_dict[sender] = 1
        msg_count = json.dumps(msg_count_dict)
    else:
        #没有数据
        msg_count = json.dumps({sender:1})

    RDB.set(receiver,msg_count)


def get_msg(sender,receiver,count=0):
    #获取未读消息
    msg_count = RDB.get(receiver)

    if msg_count:
        msg_count_dict = json.loads(msg_count)
        count = msg_count_dict.get(sender,0)

        #如果一个用户的消息读完了，就找下一个不为0的
        if count == 0:
            for k, v in msg_count_dict.items():
                if v != 0:
                    sender = k
                    count = v

        msg_count_dict[sender] = 0
    else:
        msg_count_dict = {sender:0}

    RDB.set(receiver,json.dumps(msg_count_dict))
    return count,sender
