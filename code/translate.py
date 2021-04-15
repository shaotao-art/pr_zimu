import time
import hashlib
import requests
import random
import json

class Youdao:
    def __init__(self, msg):
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.msg = msg
        self.ts=self.get_ts()
        self.salt=self.get_salt()
        self.res=self.get_result()

    def get_ts(self):
        # 根据当前时间戳获取ts参数
        s = int(time.time() * 1000)
        return str(s)

    def get_salt(self):
        # 根据当前时间戳获取salt参数
        s = int(time.time() * 1000) + random.randint(0, 10)
        return str(s)

    def get_sign(self):
        # 使用md5函数和其他参数，得到sign参数
        words = "fanyideskweb" + self.msg + self.salt + "n%A-rKaT5fb[Gy?;N5@Tj"

        # 对words进行md5加密
        hashlib.md5()
        m = hashlib.md5()
        m.update(words.encode('utf-8'))
        return m.hexdigest()

    def get_result(self):
        Form_Data = {
            'i': self.msg,
            'from': 'zh-CHS',
            'to': 'en',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': self.salt,
            'sign': self.get_sign(),
            'ts': self.ts,
            'bv': 'a4f4c82afd8bdba188e568d101be3f53',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION'
        }

        headers = {
            'Cookie': 'OUTFOX_SEARCH_USER_ID=1389460813@123.125.1.12',
            'Referer': 'http://fanyi.youdao.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OSX10_14_2) AppleWebKit/537.36(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        #解析返回的json信息  取得结果
        r = requests.post(self.url, data=Form_Data, headers=headers)
        res=json.loads(r.text)
        res=res['translateResult'][0][0]['tgt']
        return res


# test=Youdao('我现在很开心').res



