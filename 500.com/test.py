# -*- coding: UTF-8 -*-
# 500.com的爬虫接口--获取联赛列表部分 20170312 by XueHongyan
import re
import time
from oddsSpider import *

threads=[]
flag=0
retry = (5, 3)
def getLeagues(i):
    url = 'http://liansai.500.com/zuqiu-{0}/'.format(i)
    for j in range(0, retry[0]):
        try:
            res = requests.get(url)
            break
        except:
            print(i, '请求失败，正准备第', j, '次重试')
            time.sleep(retry[1])
            if j == 4:
                print(i, '-1')
    soup = bs4.BeautifulSoup(res.content.decode(
        'gb2312', 'ignore'), 'html5lib')
    title = soup.select('title')[0].getText()
    if title == '足球比赛_足球联赛赛事_足球赛程 - 500彩票网':
        print(i, '-1')
    else:
        match = re.match('【(.+)】', title)
        print(i, match.group(1))

t=time.time()
while flag<200:
    threads.append(thread(getLeagues,flag))
    threads[flag].start()
    threads[flag].join()
    flag+=1
t=time.time()-t
print(t)