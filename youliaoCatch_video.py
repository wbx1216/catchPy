# -*- coding: utf-8 -*-
import requests
import json
import os
import time
import datetime
import pymysql
import urllib.request
import random
import string
import re
from bs4 import BeautifulSoup
db = pymysql.connect(host= "rm-bp1d3nze222r06y54.mysql.rds.aliyuncs.com",port=3306,user="yitui",passwd="C8pfaKa5ZO",db="yitui", charset="utf8")
#db = pymysql.connect(host= "192.168.1.168",port=3306,user="admin",passwd="123",db="yitui", charset="utf8")
cur = db.cursor()
url="https://yiyouliao.com/rss/common/b40dcc399c8d/list/json?num=20"
headers = {'Appkey':'341f2784dc0a4253be6bba666248ac8e','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
data = requests.get(url, headers=headers)
data.encoding='uft-8'
today = time.strftime('%Y%m%d', time.localtime(time.time()))
j=json.loads(data.text)
list=j['data']
address='/mountimgserver/video/'
#address='C:/Users/Administrator/Desktop/demo/'
if os.path.isdir(address+today):
     pass
else:
     os.mkdir(address+today)
# if os.path.isdir('C:/Users/Administrator/Desktop/demo/'+today):
#     pass
# else:
#     os.mkdir('C:/Users/Administrator/Desktop/demo/'+today)
imgPath = '' + today + "/"
for x in list:
    if(x['showType']=="video"):
        title = x['title']
        print(title)
        sql_cmd = '''select * from t_video where title = '%s' ''' % title
        cur.execute(sql_cmd)
        res = cur.fetchall()
        if (len(res) == 0):
                try:
                    imgName = ''.join(random.sample(string.ascii_letters + string.digits, 32))
                    imgurl = x['covers'][0]
                    bytes = urllib.request.urlopen(imgurl)
                    pic =address+ imgPath + imgName + ".jpg"
                    f = open(pic, 'wb');
                    f.write(bytes.read());
                    f.flush();  # 将缓冲区的数据立即写入缓冲区，并清空缓冲区
                    f.close();  # 关闭文件
                    cover = imgPath + imgName + ".jpg"
                    category=x['category']
                    link=x['link']
                    print(link)
                    content_data = requests.get(link, headers=headers)
                    content_data.encoding = 'utf-8'
                    soup = BeautifulSoup(content_data.text,'html.parser')
                    titles = soup.select("script")  # CSS 选择器
                    text = str(titles[0])
                    text = text.strip('<script>')
                    text = text.strip('</')
                    text = text.split('{', 1)[1:][0]
                    text = '{' + text
                    text = text.replace('content', '"content"', 1)
                    text = text.replace('related:', '"related":', 1)
                    j = json.loads(text)
                    content = j['content']['data']['videos'][0]['mp4SdUrl']
                    videoName = ''.join(random.sample(string.ascii_letters + string.digits, 32))
                    videoUrl = content
                    print(videoUrl)
                    bytes = urllib.request.urlopen(videoUrl)
                    pic =address+ imgPath + videoName + ".mp4"
                    f = open(pic, 'wb');
                    f.write(bytes.read());
                    f.flush();  # 将缓冲区的数据立即写入缓冲区，并清空缓冲区
                    f.close();  # 关闭文件
                    video_src = imgPath + videoName + ".mp4"
                    new_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    create_time = str(new_time)
                    update_time = str(new_time)
                    status=1
                    if (content != "None"):
                        insert_content = (
                            "INSERT INTO t_video(title,category,cover,link,video_src,status,create_time,update_time)" "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)")
                        data_content = (title,category,cover,link,video_src,status,create_time,update_time)
                        cur.execute(insert_content, data_content)
                        db.commit()
                        print("add  " + title)
                except:
                    print("error")
        else:
            print("exist " + title)