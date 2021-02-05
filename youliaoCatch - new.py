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
db = pymysql.connect(host= "rm-bp1d3nze222r06y54.mysql.rds.aliyuncs.com",port=3306,user="newsflow",passwd="3MvO9da9Wn",db="newsflow", charset="utf8")
#db = pymysql.connect(host= "192.168.1.168",port=3306,user="admin",passwd="123",db="newsflow", charset="utf8")
cur = db.cursor()
url="https://yiyouliao.com/rss/common/b40dcc399c8d/list/json?num=50"
headers = {'Appkey':'341f2784dc0a4253be6bba666248ac8e','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
data = requests.get(url, headers=headers)
data.encoding='uft-8'
today = time.strftime('%Y%m%d', time.localtime(time.time()))
j=json.loads(data.text)
list=j['data']
if os.path.isdir('/mountimgserver/newsflow/'+today):
     pass
else:
     os.mkdir('/mountimgserver/newsflow/'+today)
# if os.path.isdir('C:/Users/Administrator/Desktop/demo/'+today):
#     pass
# else:
#     os.mkdir('C:/Users/Administrator/Desktop/demo/'+today)

imgPath = '' + today + "/"
def switch(cate):
    if cate == '娱乐':
        return  3
    elif cate == '社会':
        return 1
    elif cate == '美食':
        return 17
    elif cate == '要闻':
        return 32
    elif cate == '健康':
        return 33
    elif cate == '搞笑':
        return 13
    elif cate == '奇趣':
        return 13
    else:
        return None
print(list)
for x in list:
    cate=x['category'][0:2]
    title = x['title']
    sql_cmd = '''select * from t_news_info where title = '%s' ''' % title
    cur.execute(sql_cmd)
    res = cur.fetchall()
    suc = True
    if (len(res) == 0):
        try:
            author=x['source']
            url = x['link']
            now = str(round(time.time() * 1000))
            uid = "youliao" + now
            info_type = "1"
            pic1 = ""
            pic2 = ""
            pic3 = ""
            if (len(x['covers']) == 1):
                info_type = "2"
            elif(len(x['covers']) == 3):
                    info_type = "3"
            if (len(x['covers'])>0):
                    i=1
                    for a in x['covers']:
                        imgName = ''.join(random.sample(string.ascii_letters + string.digits, 32))
                        imgurl = a
                        bytes = urllib.request.urlopen(imgurl)
                        size = bytes.headers['content-length']
                        size = int(size)
                        size = round(size / 1024)
                        size2 = str(size)
                        if (size < 300):
                            pic ='/mountimgserver/newsflow/' + imgPath + imgName + ".jpg"
                            if(i==1):
                                 pic1 = imgPath + imgName + ".jpg"
                            elif i ==2:
                                 pic2 = imgPath + imgName + ".jpg"
                            elif i == 3:
                                pic3 = imgPath + imgName + ".jpg"
                            f = open(pic, 'wb');
                            f.write(bytes.read());
                            f.flush();  # 将缓冲区的数据立即写入缓冲区，并清空缓冲区
                            f.close();  # 关闭文件
                            i=i+1
                        else:
                            print("图片过大")
                            break
            save_type = '1'
            source = "35"
            available_time = '30'
            level = '0'
            count = '0'
            status = '1'
            tag = '0'
            new_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            publish_t = time.time()
            publish_r = random.randint(1, 1800)
            publish_n = int(publish_t) + publish_r
            time_local = time.localtime(publish_n)
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            publish_time = str(dt)
            create_time = str(new_time)
            update_time = str(new_time)
            news_time = str(new_time)
            category = switch(cate)
            is_prepare = '0'
            is_rec = '0'
            expire_time = str((datetime.datetime.now() + datetime.timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"))
            insert_data = (
                "INSERT INTO t_news_info(uid,category,title,save_type,info_type,source,author,url,pic1,pic2,pic3,news_time,expire_time,available_time,level,count,status,tag,publish_time,create_time,update_time,is_prepare,is_rec)" "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            data_list = (uid, category, title, save_type, info_type, source, author, url, pic1, pic2, pic3, news_time, expire_time,available_time, level, count, status, tag, publish_time, create_time, update_time, is_prepare, is_rec)
            #正文
            content_data = requests.get(url, headers=headers)
            content_data.encoding = 'utf-8'
            soup = BeautifulSoup(content_data.text,'html.parser')
            list = soup.find_all('script')[0]
            text = list.get_text()
            text = text.split('{', 1)[1:][0]
            text = '{' + text
            # text = re.sub('\s+', '', text).strip()
            text = text.replace('content', '"content"', 1)
            text = text.replace('related:', '"related":', 1)
            j = json.loads(text)
            content = j['content']
            text = content['data']['content']
            content = text.replace('imgsrc', 'img  src')
            content = text.replace('imgdata', 'img data')
            if (content != "None"):
                insert_content = (
                    "INSERT INTO t_news_content(news_id,content,status,create_time,update_time)" "VALUES(%s,%s,%s,%s,%s)")
                cur.execute(insert_data, data_list)
                data_content = (cur.lastrowid, content, status, create_time, update_time)
                cur.execute(insert_content, data_content)
                db.commit()
                print("add  " + title)
        except:
            print("error")
    else:
        print("exist " + title)

