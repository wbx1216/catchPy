# -*- coding: utf-8 -*-
import requests
import urllib.request
import time
import json
import datetime
from http import cookiejar
url = 'http://118.31.113.21:8080/user/handleLogin.htm'
hea = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
data = requests.get(url, headers=hea)
data.encoding='utf-8'
def getAuthorizationCookie():
    url = 'http://118.31.113.21:8080/user/handleLogin.htm'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Connection': 'keep-alive',
        'Host': '118.31.113.21',
        'Referer': 'http://118.31.113.21:8080/user/handleLogin.htm'
    }
    params = {
        'username': 'hongda',
        'password': 'hongd123456'
    }
    data = urllib.parse.urlencode(params).encode('utf-8')
    request = urllib.request.Request(url=url, data=data, headers=headers, method='POST')
    cjar = cookiejar.CookieJar()
    # # 使用HTTPCookieProcessor创建cookie处理器，并以其为参数构建opener对象
    cookie = urllib.request.HTTPCookieProcessor(cjar)
    opener = urllib.request.build_opener(cookie)
    # # 将opener安装为全局
    urllib.request.install_opener(opener)
    response = urllib.request.urlopen(request)
    return cjar


def getYesterday():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    return yesterday
def downLoadFIle():
    cookie = getAuthorizationCookie()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    hour=time.localtime().tm_hour
    if(hour<1):
        today=getYesterday().strftime('%Y-%m-%d')
    else:
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    get_url = 'http://118.31.113.21:8080/count/queryDayPublishdata.htm?stime='+today+'&etime='+today+'&channelId=-1'
    urllib.request.install_opener(opener)
    get_request = urllib.request.Request(get_url)
    get_response = urllib.request.urlopen(get_request)
    values = get_response.read()
    data=json.loads(values)
    num=len(data) // 10
    for i in range(0,num+1):
        a=data[i*10:(i+1)*10]
        a=json.dumps(a)
        url = "https://www.e-tui.net/ring/getZumaRingData.htm"
        #url = "http://192.168.60.27:8080/yitui.server/ring/getZumaRingData.htm"
        #url="http://192.168.20.2:60001/yitui-server/ring/getZumaRingData.htm?data="+a
        res = requests.post(url,a)
        print(res.text)
downLoadFIle()


