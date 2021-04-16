import time
import hashlib
import requests
import random
import json

url='http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'

headers={   'Cookie': 'OUTFOX_SEARCH_USER_ID=1389460813@123.125.1.12',
            'Referer': 'http://fanyi.youdao.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OSX10_14_2) AppleWebKit/537.36(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
       }

def make_salt():
    # 根据当前时间戳获取salt参数
    s = int(time.time() * 1000) + random.randint(0, 10)
    return str(s)

def get_Its():
    # 根据当前时间戳获取ts参数
    s = int(time.time() * 1000)
    return str(s)

def make_sign(origin_input):
    # 使用md5函数和其他参数，得到sign参数
    words = "fanyideskweb" + origin_input + make_salt() + "n%A-rKaT5fb[Gy?;N5@Tj"
    # 对words进行md5加密
    hashlib.md5()
    m = hashlib.md5()
    m.update(words.encode('utf-8'))
    return m.hexdigest()


'''
data的其他值没加就一直出不来
'''
def get_res(msg):
    Form_Data = {
            'i': msg,
            'from': 'zh-CHS',
            'to': 'en',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': make_salt(),
            'sign': make_sign(msg),
            'ts': get_Its(),
            'bv': 'a4f4c82afd8bdba188e568d101be3f53',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION'
            }
    r=requests.post(url=url,data=Form_Data,headers=headers)
    data=json.loads(r.text)
    return data['translateResult'][0][0]['tgt']









