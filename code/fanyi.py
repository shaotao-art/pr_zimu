import time
import hashlib
import requests
import random
import json

url='http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

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
def request(url):
    Form_Data = {
            'i': '喜欢',
            'from': 'zh-CHS',
            'to': 'en',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': make_salt(),
            'sign': make_sign('喜欢'),
            'ts': get_Its(),
            'bv': 'a4f4c82afd8bdba188e568d101be3f53',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION'
            }
    r=requests.post(url=url,data=Form_Data,headers=headers)
    print(r.text)
    # data=json.loads(r.text)
    # print(data["translateResult"]['tgt'])

request(url)

# define("newweb/common/docTrans", ["./form", "./md5", "./jquery-1.7", "./account", "./log", "../langSelect", "./TranslateState", "./star", "./select", "./utils"],
# function(e, t) {
#     function n() {
#         var e = p("#language").val().split("2"),
#         t = p("#docUploadFile").val(),
#         n = t.split("."),
#         r = n[n.length - 1],
#         i = t.split("\\"),
#         a = i[i.length - 1],
#         o = p("#docUploadFile")[0].files,
#         s = 1e3,
#         l = (new Date).getTime(),
#         c = p.md5("new-fanyiweb" + l + "ydsecret://newfanyiweb.doctran/sign/0j9n2{3mLSN-$Lg]K4o0N2}" + a);
#         return o && o[0] && o[0].size && (s = o[0].size),
#         {
#             from: e[0],
#             to: e[1],
#             type: r,
#             filename: a,
#             client: "docserver",
#             keyfrom: "new-fanyiweb",
#             size: s,
#             sign: c,
#             salt: l
#         }
#     }

# define("newweb/common/service", ["./utils", "./md5", "./jquery-1.7"],
# function(e, t) {
#     var n = e("./jquery-1.7");
#     e("./utils");
#     e("./md5");
#     var r = function(e) {
#         var t = n.md5(navigator.appVersion),
#         r = "" + (new Date).getTime(),
#         i = r + parseInt(10 * Math.random(), 10);
#         return {
#             ts: r,
#             bv: t,
#             salt: i,
#             sign: n.md5("fanyideskweb" + e + i + "Tbh5E8=q6U3EXe+&L[4c@")
#         }
#     };
