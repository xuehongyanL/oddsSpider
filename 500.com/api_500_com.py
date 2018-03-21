# -*- coding: UTF-8 -*-
# 500.com的爬虫接口--函数部分 20170309 by XueHongyan
import re
import bs4
import requests
from operator import itemgetter


def showProgress(ii, delta):  # 只是为了每隔一定数目显示进度
    if ii % delta == 0:
        print(ii)


def select(DATA, leagueName, startYear=2000):  # 筛选联赛函数：输入数据列表，联赛简称和起始年份
    ans = []
    pattern = re.compile('_' + leagueName + '_')  # 识别如 _英超_ _德甲_ 等字段
    for data in DATA:  # 原始数据是（联赛id，联赛名）的元组
        if re.search(pattern, data[1])and int(data[1][0:4]) >= startYear:  # 识别年份
            ans.append(data)
    return sorted(ans, key=itemgetter(1))  # 将结果按年份排序输出


def getStages(id):  # 获取比赛阶段函数：输入联赛id. 杯赛经常不同阶段有不同的stid
    url = 'http://liansai.500.com/zuqiu-{0}'.format(id)
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content.decode(
        'gb2312', 'ignore'), 'html5lib')
    url = 'http://liansai.500.com' + \
        soup.select('div[class="lcol_tit_r"]')[0].a['href']  # 寻找‘查看完整赛程’的链接
    stid = int(re.findall('\d+', url)[-1])  # 暂时获取当前页面的rid
    res = requests.get(url)
    try:
        pattern = '<a href="/zuqiu-\d+/jifen-\d+/" class="ltab_btn .*?" data-id="(\d+)">(.+?)</a>'
        temp = re.findall(pattern, res.text)  # 寻找所有阶段的链接按钮
        ans = {}
        for tem in temp:
            ans[tem[1]] = tem[0]  # 输出阶段名到stid的字典
        return ans
    except:
        return {'全赛季': stid}  # 如果找不到链接按钮，就视为只有一个阶段


def getRounds(id, stid, full=False):  # 获取轮次信息函数：输入联赛id，阶段的stid和是否请求完整数据
    url = 'http://liansai.500.com/zuqiu-{0}/jifen-{1}/'.format(id, stid)
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content.decode(
        'gb2312', 'ignore'), 'html5lib')
    rounds = len(soup.select('a[data-group]'))  # 寻找所有轮次的链接按钮，以获得总轮次
    if not full:
        return rounds  # 如果full参数为False则直接返回总轮次
    ans = []
    for r in range(0, rounds):
        url = 'http://liansai.500.com/index.php?c=score&a=getmatch&stid={0}&round={1}'.format(
            stid, r+1)
        res = requests.get(url)
        j = res.json()  # 否则按轮次GET得到轮次信息的json
        temp = []
        for tem in j:
            temp.append((tem['fid'], tem['stime'], tem['hname'], tem['gname'], tem['hscore'],
                         tem['gscore'], tem['hhalfscore'], tem['ghalfscore']))  # 按场次提取场次id（我称作mid）并按轮次组成集合
        ans.append(temp)
    return ans  # 将轮次再次组成集合返回


def getOdds(mid):  # 获取赔率函数：输入场次的mid
    url = 'http://odds.500.com/fenxi/ouzhi-{0}.shtml'.format(mid)
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content.decode(
        'gb2312', 'ignore'), 'html5lib')
    comps = [1, 3, 293, 2, 4]  # 0竞彩1[bet365]2威廉3立博4Interwetten
    ans = []
    for comp in comps:  # 枚举bocai公司
        try:
            zhuang = soup.select('tr[id={0}]'.format(comp))[0]  # 寻找该公司的一行
            odds = zhuang.select('td')[2].select('tr')  # 寻找赔率的数据行
            origin = odds[0]  # 第一行为初赔
            latest = odds[1]  # 第二行为即时赔率/终赔
            originGot = origin.select('td')
            latestGot = latest.select('td')  # 分别依次选取主胜/平手/客胜的赔率
            originOdds = []
            latestOdds = []
            for i in range(3):
                originOdds.append(originGot[i].getText().strip())
                latestOdds.append(latestGot[i].getText().strip())  # 去掉空格
            originOdds = tuple(originOdds)
            latestOdds = tuple(latestOdds)  # 转换为元组（心血来潮）
            ans.append((originOdds, latestOdds))
        except:
            ans.append(((), ()))  # 如果出现问题就放弃
    return ans
