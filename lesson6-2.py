#!usr/bin/python3
# -*- coding: UTF-8 -*-

# lesson6-2---如何读写json数据

# 案例：在wev应用中常用JSON格式传输数据，例如我们利用Baidu语音识别服务做语音识别，将本地音频数据post到Baidu语音识别
# 服务器，服务器响应结果为json字符串。在python中如何读写json数据？

# 方案：使用标准库中的json模块，其中loads，dumps函数可以完成json数据的读写。

import requests
import json

# 读取本地音频文件
with open('16k.wav', 'rb') as demo:
    audioData = demo.read()

# 获取百度语音的token值
API_KEY = 'EvF5LfCW49uqQBOMg9ogzD2K'
SECRET_KEY = 'fb66f5df6953e16edb11c78a52505985'
Url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id='\
      + API_KEY + '&client_secret=' + SECRET_KEY
response = requests.get(Url)
token = json.loads(response.content.decode('utf-8'))['access_token']

# 向百度请求语音识别并获取结果

svrUrl = 'http://vop.baidu.com/server_api?lan=zh&cuid=xxxxxxxxx&token=' + token
httpHeader = {'Content-Type': 'audio/wav;rate=16000'}
response = requests.post(svrUrl, headers=httpHeader, data=audioData)
text = json.loads(response.content.decode('utf-8'))['result']
print('识别结果是：', text)


# 课后小结&拓展：
#     1.百度语音在线识别，需要两个步骤。 先用get请求获取token，再用post请求传输音频文件和其他信息，最后返回一个
#     json格式的文本，反序列化后可获得包含结果信息的序列。
#     2.json.dump(obj, fp, skipkeys=False, ensure_ascii=Ture,check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False,**kw)
#     使用json格式序列化对象，并保存在fp文件。json.load()是其逆向操作。
#     3.json.dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw)
#     使用json格式序列化对象。
#     3.json.loads(s, encoding=None, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw）
#     json.dumps()的逆向操作。注意参数s，不能是字节。本例中，百度传回的json数据是字节，需要用decode('utf-8')解码
