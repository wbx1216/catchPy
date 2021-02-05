import requests,json
import pymysql
import time
from bs4 import BeautifulSoup
#db = pymysql.connect(host="rm-bp1d3nze222r06y54zo.mysql.rds.aliyuncs.com",port=3306,user="newsflow",passwd="3MvO9da9Wn",db="newsflow", charset="utf8")
db = pymysql.connect(host= "192.168.1.168",port=3306,user="admin",passwd="123",db="newsflow", charset="utf8")
cur = db.cursor()
url=['http://top.baidu.com/buzz?b=1&c=513&fr=topbuzz_b11_c513','http://top.baidu.com/buzz?b=341&c=513&fr=topbuzz_b1_c513','http://top.baidu.com/buzz?b=42&c=513&fr=topbuzz_b341_c513','http://top.baidu.com/buzz?b=342&c=513&fr=topbuzz_b42_c513','http://top.baidu.com/buzz?b=344&c=513&fr=topbuzz_b342_c513']
hea = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
'Connection': 'keep-alive',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
a=0
for i in url:
    a=a+1
    print(a)
    data = requests.get(i, headers=hea)
    data.encoding='gb2312'
    soup = BeautifulSoup(data.text,'html.parser')
    list = soup.find_all("a",{'class':'list-title'})
    for x in list:
        keyword = x.text
        sql_cmd = '''select * from t_keyword_adv where keyword = '%s' ''' % keyword
        cur.execute(sql_cmd)
        res = cur.fetchall()
        suc = True
        if (len(res) == 0):
            new_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            create_time = str(new_time)
            update_time = str(new_time)
            feature=a
            source=1
            type=1
            status=1
            insert_content = (
                "INSERT INTO t_keyword_adv(keyword,feature,source,type,status,create_time,update_time)" "VALUES(%s,%s,%s,%s,%s,%s,%s)")
            data_content = (keyword,feature,source,type,status,create_time,update_time)
            cur.execute(insert_content, data_content)
            db.commit()
        else:
            print(keyword+"已经抓取")