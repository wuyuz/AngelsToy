import subprocess

from aip import AipSpeech,AipNlp

 # 语音转文本  TTS技术
import os

""" 你的 APPID AK SK  获得百度云接口"""
APP_ID = '16981704'
API_KEY = 'CeLs5zCuQwWXBhHbrnDGQhc3'
SECRET_KEY = 'HIOyvsDRcXKlP95NOY72CAUznUIC6OKZ'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)   # 获取到接口，将用于我们上传语音文本
nlp_client = AipNlp(APP_ID, API_KEY, SECRET_KEY)  # 文本相似度查询接口

 #读取文本
def get_file_content(filePath):
    cmd = f"ffmpeg -y  -i {filePath} -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {filePath}.pcm"  # 将传入的格式转换为pcm
    # r = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,)  # 此方法是异步的
    # stdout = r.stdout.read().decode('gbk')
    # print(stdout)
    # stderr =  r.stderr.read().decode('gbk')
    # print(stderr)

    os.system(cmd)  #将录音转换格式
    try:
        with open(f"{filePath}.pcm", 'rb') as fp:
            return fp.read()  #发送的是字节流
    finally:
        os.remove(filePath)
 # 识别本地文件并发送，最后接受返回值
res = client.asr(get_file_content('wyn.m4a'), 'pcm', 16000, {
    'dev_pid': 1536,
})



print(res)
print(res.get("result")[0])

Q = res.get("result")[0]  #读取出我们的问题

A = "我不知道你在说什么"
if nlp_client.simnet(Q,"你的名字叫什么").get("score") >= 0.6: # 文本相似度比较,自定义的问题
    A = "我叫小猪武沛齐,哼哼哼"
else:
    tl_url = "http://openapi.tuling123.com/openapi/api/v2"  #获取到问答机器人接口

    import requests  #使用reqeust进行访问

    tl_data = {
        "perception": {
            "inputText": {
                "text": "北京今天天气怎么样"
            }
        },
        "userInfo": {
            "apiKey": "51ff3d2dd9464ba6bba97ff1bb9427ab",
            "userId": "123456789123"
        }
    }

    tl_data["perception"]["inputText"]["text"] = Q  #替换问题

    res = requests.post(tl_url, json=tl_data)  #提交json格式的数据，到指定接口

    res_json = res.json()  #获取json格式的回答
    A = res_json.get("results")[0].get("values").get("text")

print(A)

result = client.synthesis(A, 'zh', 1,  #使用语音合成技术，生成音频ASR
                          {
                              'vol': 5,
                              "spd": 4,
                              "pit": 6,
                              "per": 4
                          })

# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    with open('Answer.mp3', 'wb') as f:
        f.write(result)
else:
    print(result)

if 'Answer.mp3' in os.listdir():
    os.system("ffplay Answer.mp3")  #播放音乐
