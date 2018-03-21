# -*- coding: UTF-8 -*-
# 500.com的爬虫接口--获取比赛数据部分 20170312 by XueHongyan
from api_500_com import *
import sqlite3


def examStage(cc, stg):  # 检查阶段数据是否完整
    for rnd in range(stg[5]):
        cc.execute('''SELECT * FROM matches
        WHERE league="{0}" and season={1} and round={2};'''.format(
            stg[2], stg[3], rnd+1))  # 筛选该阶段每一轮的比赛
        if len(cc.fetchall()) < ((stg[5]+2)/4):
            return False  # 如果比赛数少于应有数目则返回False
    return True


def scoreToRes(h, a):  # 根据双方比分给出3/1/0的赛果
    try:
        if h > a:
            return 3
        if h < a:
            return 0
        return 1
    except:
        return 2

def writeRound(cc,stg,rnd,index):
    cc.execute('''SELECT * FROM matches
        WHERE league="{0}" and season={1} and round={2};'''.format(
            stg[2], stg[3], index+1))
    if len(cc.fetchall()) == ((stg[5]+2)/4):return
    for mth in rnd:
        dat = [mth[0], stg[2], stg[3], stg[4], index+1, mth[1],
                   mth[2], mth[3], scoreToRes(mth[4], mth[5]),
                   mth[4], mth[5], mth[6], mth[7]]  # 按场次获取基本数据
        if (not mth[6]) or (not mth[7]):
            dat[-1],dat[-2]='null','null'
        try:
            odds = getOdds(mth[0])  # 按比赛id获取赔率数据
        except:
            print(dat)
            continue
        for odd in odds:
            if odd[0] == ():
                dat.extend(('null', 'null', 'null'))  # 如果赔率为空
            else:
                dat.extend(odd[0])  # 按顺序组织赔率数据
        if dat[8]==2:
            dat[9]=dat[10]=dat[11]=dat[12]='null'
        canshu = '''{0[0]},"{0[1]}",{0[2]},"{0[3]}",{0[4]},"{0[5]}","{0[6]}","{0[7]}",{0[8]},{0[9]},{0[10]},{0[11]},{0[12]},{0[13]},{0[14]},{0[15]},{0[16]},{0[17]},{0[18]},{0[19]},{0[20]},{0[21]},{0[22]},{0[23]},{0[24]},{0[25]},{0[26]},{0[27]}'''
        sql = '''INSERT OR REPLACE INTO matches VALUES({0});'''.format(
            canshu)
        #print(sql.format(dat))
        c.execute(sql.format(dat))  # 合成并执行一个很长很长很长的SQL语句
    print(stg[2], stg[3], stg[4], index)
    conn.commit()

def writeStage(cc, stg):  # 按阶段写入函数
    if examStage(cc, stg):
        print(stg[2], stg[3], stg[4], 'ok')
        return  # 如果阶段数据完整，则直接跳过
    matches = getRounds(stg[0], stg[1], full=True)  # 否则获取该阶段所有数据
    for rnd in range(stg[5]):
        #print(rnd)
        temp = matches[rnd]  # 按轮次获取数据
        writeRound(c,stg,temp,rnd)
        '''
        for mth in temp:
            dat = [mth[0], stg[2], stg[3], stg[4], rnd+1, mth[1],
                   mth[2], mth[3], scoreToRes(mth[4], mth[5]),
                   mth[4], mth[5], mth[6], mth[7]]  # 按场次获取基本数据
            try:
                odds = getOdds(mth[0])  # 按比赛id获取赔率数据
            except:
                print(dat)
                continue
            for odd in odds:
                if odd[0] == ():
                    dat.extend(('null', 'null', 'null'))  # 如果赔率为空
                else:
                    dat.extend(odd[0])  # 按顺序组织赔率数据
            canshu = ''{0[0]},"{0[1]}",{0[2]},"{0[3]}",{0[4]},"{0[5]}","{0[6]}","{0[7]}",{0[8]},{0[9]},{0[10]},{0[11]},{0[12]},{0[13]},{0[14]},{0[15]},{0[16]},{0[17]},{0[18]},{0[19]},{0[20]},{0[21]},{0[22]},{0[23]},{0[24]},{0[25]},{0[26]},{0[27]}'
            sql = ''INSERT OR IGNORE INTO matches VALUES({0});''.format(
                canshu)
            c.execute(sql.format(dat))  # 合成并执行一个很长很长很长的SQL语句
        print(stg[2], stg[3], stg[4], rnd)
    conn.commit()  # 执行写入操作
    '''
    print(stg[2], stg[3], stg[4], 'ok')
    return


conn = sqlite3.connect('data.db')
c = conn.cursor()
try:
    c.execute('''CREATE TABLE matches(
    mid INT PRIMARY KEY,
    league TEXT,
    season INT,
    stage TEXT,
    round INT,
    time TEXT,
    home TEXT,
    away TEXT,
    result INT,
    hscore INT,
    ascore INT,
    hfhscore INT,
    hfascore INT,
    jingcaiwin REAL,
    jingcaidraw REAL,
    jingcailose REAL,
    bet365win REAL,
    bet365draw REAL,
    bet365lose REAL,
    weilianwin REAL,
    weiliandraw REAL,
    weilianlose REAL,
    libowin REAL,
    libodraw REAL,
    libolose REAL,
    interwin REAL,
    interdraw REAL,
    interlose REAL
    );
    '''
              )
    conn.commit()
except:
    pass  # 如果没有matches表，则创建一个

c.execute('''SELECT * FROM stages
    WHERE season<>2017;''')
stages = c.fetchall()  # 获取所有阶段

for stage in stages:
    writeStage(c, stage)
