import os
import time

import requests
from bson import ObjectId

from Config import AUDIO_CLIENT, VOICE, CHAT_PATH, MongoDB, NLP_CLIENT, TL, TL_DATA
from uuid import uuid4

def text2audio(text):
    filename = f"{uuid4()}.mp3"
    file_path = os.path.join(CHAT_PATH,filename)
    res = AUDIO_CLIENT.synthesis(text,'zh', 1,VOICE)

    if type(res) == dict:
        print(111)
        pass
    else:
        with open(file_path,'wb') as f:
            f.write(res)

    return filename  # 用于返回生成的文件名


 #读取文本,转pcm并且读取pcm文件流
def get_file_content(filePath):
    cmd = f"ffmpeg -y  -i {filePath} -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {filePath}.pcm"  # 将传入的格式转换为pcm
    os.system(cmd)  #将录音转换格式
    try:
        with open(f"{filePath}.pcm", 'rb') as fp:
            return fp.read()  #发送的是字节流
    finally:
        os.remove(filePath)


def audio2text(filepath):
    res = get_file_content(filepath)

    # 识别本地文件并发送，最后接受返回值
    ret = AUDIO_CLIENT.asr(res, 'pcm', 16000, {
        'dev_pid': 1536,
    })

    return ret.get("result")[0]


def my_nlp_lowB(Q,toy_id):
    # 理解Q的意图
    # 点播歌曲
    print(Q)
    if "我想听" in Q or '我要听' in Q or '请播放' in Q:
        content_list = list(MongoDB.Content.find({}))
        for content in content_list:
            # 防止QPS
            time.sleep(0.5)
            print(content.get('title'))
            if NLP_CLIENT.simnet(Q,f"我想听{content.get('title')}").get('score')>=0.8:
                return {'from_user':'ai','music':content.get('music')}

    # 主动发起聊天
    if '发消息' in Q or '聊天' in Q:
        toy = MongoDB.toys.find_one({'_id':ObjectId(toy_id)})
        for friend in toy.get('friend_list'):
            if friend.get('friend_nick') in Q or friend.get('friend_remark') in Q:
                filename = text2audio(f"现在可以给{friend.get('friend_remark')}发消息")
                return {
                    'from_user':friend.get('friend_id'),  # 表向的把发送的对象改变，下次toy发消息就是发个它
                    'chat':filename,
                    'friend_type':friend.get('friend_type'),
                    'name1':friend.get('friend_remark')
                }
    else:
        TL_DATA['perception']['inputText']['text'] = Q
        TL_DATA['userInfo']['userId'] = toy_id
        res = requests.post(TL, json=TL_DATA)  # 发送字典格式

        res_json = res.json()  # requests对象的反序列化
        start_content = res_json.get("results")[0].get("values").get("text")
        filename = text2audio(start_content)
        return {
                "from_user": "ai",
                "chat": filename,
                'friend_type':'机器人',
                }