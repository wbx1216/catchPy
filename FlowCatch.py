# -*- coding: utf-8 -*-
import requests
import urllib.request
import time
import json
import datetime
from http import cookiejar
url = 'https://agentsys.freelynet.com/sellermanager/#/login'
hea = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
data = requests.get(url, headers=hea)
data.encoding='utf-8'
token=''
def getAuthorizationCookie():
    url = 'https://agentservice.freelynet.com/staffManager/login'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Connection': 'keep-alive',
        'Host': 'agentservice.freelynet.com',
        'Referer': 'https://agentsys.freelynet.com/sellermanager/login'
    }
    params = {
        'account': 'hongda',
        'password': 'hongda123'
    }
    data = urllib.parse.urlencode(params).encode('utf-8')
    # request = urllib.request.Request(url=url, data=data, headers=headers, method='POST')
    response = requests.post(url, data=data, headers=headers)
    cjar = cookiejar.CookieJar()
    # # 使用HTTPCookieProcessor创建cookie处理器，并以其为参数构建opener对象
    cookie = urllib.request.HTTPCookieProcessor(cjar)
    opener = urllib.request.build_opener(cookie)
    # # 将opener安装为全局
    urllib.request.install_opener(opener)
    # response = urllib.request.urlopen(request)
    text=json.loads(response.text)
    token=text['data']
    return cjar,token


def getYesterday():
    today=datetime.date.today()
    now =datetime.datetime.now()
    # print(now.hour,now.minute,now.second)
    if(now.hour==0 and  now.minute<5):
        oneday=datetime.timedelta(days=1)
        startday=today-oneday
        hour="23"
    else:
        startday=today
        if(now.minute<5):
            hour=now.hour-1
        else:
            hour=now.hour
    if (hour < 10):
        hour = str(hour)
        realHour = "0" + hour
    else:
        realHour=str(hour)
    startday=str(startday)
    timeStart = startday+'+'+realHour+':00:00'
    timeEnd=startday+'+'+realHour+':59:59'
    timeStruct = time.strptime(startday, "%Y-%m-%d")
    strTime = time.strftime("%Y%m%d", timeStruct)
    newHour=strTime+realHour
    return strTime,newHour,timeStart,timeEnd
def downLoadFIle():
    cookie = getAuthorizationCookie()[0]
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    time=getYesterday()
    get_url = 'https://agentservice.freelynet.com/userTable/get5GpackageList?pageSize=1000&curPage=1&staff=hongda&level=all&channel=&status=all&timeStart='+time[2]+'&timeEnd='+time[3]
    print(get_url)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Connection': 'keep-alive',
        'Host': 'agentservice.freelynet.com',
        'token':getAuthorizationCookie()[1]
    }
    urllib.request.install_opener(opener)
    get_request = urllib.request.Request(get_url, headers=headers)
    get_response = urllib.request.urlopen(get_request)
    values = get_response.read()
    data=json.loads(values)
    data=data['data']
    list=[]
    fromAccount=[]
    for i in data:
            if(i['fromAccount'] not in fromAccount):
                fromAccount.append(i['fromAccount'])
    for i in  fromAccount:
        a=[]
        for s in data:
            if(s['fromAccount']==i):
                a.append(s)
        list.append(a)
    array=[]
    a=0

    for i in list:
        new={}
        new['all']=len(i)
        new['channelName']=fromAccount[a]
        b=0
        for s in i:
            if(s['status']==1):
                b=b+1
        new['success']=b
        new['day']=time[0]
        new['hour']=time[1]
        array.append(new)
        a=a+1
    url = "https://www.e-tui.net/ring/getHxzhTrafficData.htm"
    #     #url = "http://192.168.60.27:8080/yitui.server/ring/getZumaRingData.htm"
    # url="http://192.168.20.2:10020/ring/getHxzhTrafficData.htm"
    array = json.dumps(array)
    print(array)
    res = requests.post(url,array)
    print(res.text)
downLoadFIle()
