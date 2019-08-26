# 存储路径
COVER_PATH = "Cover"
MUSIC_PATH = "Music"
QRCODE_PATH = "QRcode"
CHAT_PATH = 'Chat'

# 数据库配置
from pymongo import MongoClient

MC = MongoClient('127.0.0.1', 27017)
MongoDB = MC['Angela']

from redis import Redis

RDB = Redis('127.0.0.1', 6379)

# 返回值配置
RET = {
    "CODE": 0,
    'MSG': '',
    'DATA': {}
}

# 联图二维码接口
LT_URL = "http://qr.liantu.com/api.php?text=%s"
# 图灵机器人
TL = "http://openapi.tuling123.com/openapi/api/v2"

TL_DATA = {
    "perception": {
        "inputText": {
            "text": "",
        }
    },
    "userInfo": {
        "apiKey": "51ff3d2dd9464ba6bba97ff1bb9427ab",
        "userId": "123456789123"
    }
}

# 百度语音接口
from aip import AipSpeech, AipNlp

""" 你的 APPID AK SK """
APP_ID = '16981704'
API_KEY = 'CeLs5zCuQwWXBhHbrnDGQhc3'
SECRET_KEY = 'HIOyvsDRcXKlP95NOY72CAUznUIC6OKZ'

AUDIO_CLIENT = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
NLP_CLIENT = AipNlp(APP_ID, API_KEY, SECRET_KEY)  # 文本相似度查询接口
VOICE = {
    'vol': 5,
    'spd': 4,
    'pit': 6,
    'per': 4
}
