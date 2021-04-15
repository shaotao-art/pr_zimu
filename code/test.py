import json

a=r'{"translateResult":[[{"tgt":"start","src":"开始"}]],"errorCode":0,"type":"zh-CHS2en","smartResult":{"entries":["","[计] begin\r\n","start\r\n","initiate\r\n"],"type":1}}'
res=json.loads(a)
print(res['translateResult'][0][0]['tgt'])