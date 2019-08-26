import os

import requests
from Config import LT_URL,QRCODE_PATH,MongoDB
from uuid import uuid4
import time, hashlib

#创建二维码，设备编号字符串

def create_qr(n):
    device_list = []
    for i in range(n):
        DeviceKey = hashlib.md5(f"{uuid4()}{time.time()}{uuid4()}".encode('utf-8')).hexdigest()
        res = requests.get(LT_URL%(DeviceKey))
        qr_name = f"{DeviceKey}.jpg"
        qr_file_path = os.path.join(QRCODE_PATH,qr_name)

        with open(qr_file_path,'wb') as f:
            f.write(res.content)


        device_key = {
            "device_key":DeviceKey
        }

        device_list.append(device_key)
    #存放在数据库中
    MongoDB.devices.insert(device_list)

create_qr(5)

