import requests



url = 'http://xx.cn/loan-manager-front/upload'
files = {'attach': ('p5.png', open('../p5.png', 'rb'))}
r = requests.post(url, files=files)
print(requests.Request('POST', url, files=files).prepare().body.decode(
    'ascii'))  # 打印字段名和类型
print(r.text)