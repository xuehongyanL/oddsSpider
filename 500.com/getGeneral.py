# -*- coding: UTF-8 -*-
# 500.com的爬虫接口--获取赛季总览部分 20170312 by XueHongyan
from api_500_com import *
import sqlite3

leagueName = '法甲'  # 要提取的联赛简称

conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute('''SELECT * FROM leagues''')
leagues = c.fetchall()  # 获取全部联赛

try:
    c.execute('''CREATE TABLE general(
    name TEXT,
    season INT,
    id INT,
    stages TEXT
    );
    ''')
    conn.commit()
except:
    pass  # 如果没有general表，则创建一个

seasons = select(leagues, leagueName, 2003)  # 筛选从2003赛季起的选定联赛
for season in seasons:
    dat = [leagueName, int(season[1][:4]), season[0],
           str(getStages(season[0]))]  # 从联赛名中提取赛季，从id获取阶段
    c.execute('''INSERT OR REPLACE INTO general VALUES("{0[0]}",{0[1]},{0[2]},"{0[3]}");'''.format(
        dat))  # 依次写入联赛名，赛季，联赛id和各阶段stid的字典
    print(dat)
    conn.commit()  # 执行写入操作
