#!/usr/bin/python
# - * -coding: UTF - 8 - * -

import requests
import uuid
import time
import hashlib
import json
id = 'x235aa342437a4675'
key = 'xS8Yv9sToyjB5Hs93uOcMdAIO5ikTDvUf'
url = "https://openapi.youdao.com/api"

def translate(text):
    if len(text) > 20:
        input = text[0:10] + str(len(text)) + text[-10:]
    else:
        input = text
        
    salt = uuid.uuid4().hex
    curtime = str(int(time.time()))
    sha = hashlib.sha256()
    sha.update((id+input+salt+curtime+key).encode('utf-8'))
    sign = sha.hexdigest()

    querystring = {
        "q": text,
        "from": "auto",
        "to": "zh-CHS",
        "appKey": id,
        "salt": salt,
        "sign": sign,
        "signType": "v3",
        "curtime": curtime,
        "input": input
    }

    response = requests.request(
        "GET", url, params=querystring)

    json_data = json.loads(response.text)

    return json_data['translation'][0]
