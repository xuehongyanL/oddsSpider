# -*- coding: UTF-8 -*-
# 500.com的爬虫接口--获取阶段列表部分 20170312 by XueHongyan
from api_500_com import *
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()
try:
    c.execute('''CREATE TABLE stages(
    id INT,
    stid INT PRIMARY KEY,
    league TEXT,
    season INT,
    stage TEXT,
    rounds INT
    );
    ''')
    conn.commit()
except:
    pass  # 如果没有stages表，则创建一个

c.execute('''SELECT * FROM general''')
data = c.fetchall()  # 获取所有的联赛
for dat in data:
    stgs = eval(dat[3])  # 解析出阶段列表
    for key in stgs:
        c.execute('''INSERT OR IGNORE INTO stages VALUES({5},{0},"{1}",{2},"{3}",{4});'''.format(
            int(stgs[key]), dat[0], dat[1], key, getRounds(dat[2], stgs[key]),
            dat[2])) #对每个键（阶段）分别创建条目
        print('...')
    c.commit()
print('ok')
