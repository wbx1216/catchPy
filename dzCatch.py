# # -*- coding: utf-8 -*-
import requests
import json
import os
import time
import datetime
import pymysql
import urllib.request
import random
import string
db = pymysql.connect(host= "rm-bp1d3nze222r06y54.mysql.rds.aliyuncs.com",port=3306,user="newsflow",passwd="3MvO9da9Wn",db="newsflow", charset="utf8")
#db = pymysql.connect(host= "192.168.1.168",port=3306,user="admin",passwd="123",db="newsflow", charset="utf8")
cur = db.cursor()
for i in range(1,226):
    i=str(i)
    url = 'http://ad.chntid.com/api/v1/reptile/duanzi?page='+i
    print(url)
    response = requests.get(url)
    data=json.loads(response.text)
    data=data['data']['data']
    #address='G:\duanzi'
    address='/mountimgserver/newsflow/dz/'
    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    if os.path.isdir(address+today):
        pass
    else:
        os.mkdir(address+today)
    imgPath = '' + today + "/"
    for i in data:
        id=i['id']
        author=i['title']
        sql_cmd = '''select * from t_crosstalk where id = '%s' ''' % id
        cur.execute(sql_cmd)
        res = cur.fetchall()
        suc = True
        if (len(res) == 0):
            type=i['type']
            content=i['content']
            likes=i['likes']
            share=i['share']
            status=i['status']
            publish_time=i['create_time'] 
            icon=""
            try:
                imgName = ''.join(random.sample(string.ascii_letters + string.digits, 32))
                imgurl = i['file']
                bytes = urllib.request.urlopen(imgurl)
                icon = address + imgPath + imgName + ".jpg"
                f = open(icon, 'wb');
                f.write(bytes.read());
                f.flush();  # 将缓冲区的数据立即写入缓冲区，并清空缓冲区
                f.close();  # 关闭文件
                print("有图")
            except:
                print("无图")
            insert_content = (
                "INSERT INTO t_crosstalk(id,author,type,content,likes,share,status,publish_time,icon)" "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            data_list=(id,author,type,content,likes,share,status,publish_time,icon)
            cur.execute(insert_content, data_list)
            db.commit()
            print("add  " + author)
        else:
            print("exist 已存在" + author)