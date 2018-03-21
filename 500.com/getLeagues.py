# -*- coding: UTF-8 -*-
# 500.com的爬虫接口--获取联赛列表部分 20170312 by XueHongyan
from api_500_com import *
import sqlite3
import time


def insert(cc, ii, tt):  # 插入无效行函数，当找不到联赛时使用
    cc.execute('''INSERT OR REPLACE INTO leagues VALUES({0},"{1}");'''.format(
        ii, tt))


conn = sqlite3.connect('data.db')  # 连接数据库
c = conn.cursor()
try:
    c.execute('''CREATE TABLE leagues(
    id INT PRIMARY KEY,
    name TEXT
    );
    ''')
    conn.commit()
except:
    pass  # 如果没有leagues表，则创建一个

start = 4500  # 设置起始。忽略之前的大部分联赛
end = 6000  # 设置终止
retry = (5, 3)  # 重试连接的次数和间隔时间
for i in range(start, end):
    c.execute('''SELECT * FROM leagues
                WHERE id={0};'''.format(i))
    temp = c.fetchall()  # 搜索并获取已有条目
    if temp and temp[0][1] != '-1':
        showProgress(i, 100)
        continue  # 如果条目存在并且不为空，则跳过
    url = 'http://liansai.500.com/zuqiu-{0}/'.format(i)
    for j in range(0, retry[0]):
        try:
            res = requests.get(url)
            break
        except:
            print(i, '请求失败，正准备第', j, '次重试')
            time.sleep(retry[1])
            if j == 4:
                insert(c, i, '-1')  # 多次重试获取联赛页面，是在收不到就放弃
    soup = bs4.BeautifulSoup(res.content.decode(
        'gb2312', 'ignore'), 'html5lib')
    title = soup.select('title')[0].getText()  # 获取网页标题
    if title == '足球比赛_足球联赛赛事_足球赛程 - 500彩票网':
        insert(c, i, '-1')  # 如果被重定向到500.com，则视为放弃
    else:
        match = re.match('【(.+)】', title)
        insert(c, i, match.group(1))  # 否则正则表达式获取联赛名并将数据写入数据库
    showProgress(i, 100)
    conn.commit()  # 执行写入操作