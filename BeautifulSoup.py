#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: skyxnet
"""

import time
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree


# get_html_text(url)获取网页信息
def get_html_text(url):
    try:
        r = requests.get(url)  # 爬取完整的网页数据
        r.raise_for_status()  # 如果状态不是200，引发HTTPError异常
        return r.text  # 以字符串的形式返回爬取的网页内容
    except:
        print("访问出错")
        return ""  # 发生异常，返回空字符串


# extract_data(data)提取网页内容
def extract_data(data):
    soup = bs(data, 'html.parser')
    # 列表ls_ms回复信息
    ls_ms = []
    ls = soup.find_all("td", class_="postbody")
    n = len(ls)
    for i in range(n):
        try:
            ls_ms.append(ls[i].get_text(strip=True))
        except:
            print('出错')
            continue
    return ls_ms


# 主函数
def main():
    url = 'http://www.dxy.cn/bbs/thread/626626#626626'
    data = get_html_text(url)
    ls_ms = extract_data(data)
    for i in ls_ms:
        print(i)


# 测试时间
def count_spend_time(func):
    start_time = time.time()
    func()
    end_time = time.time()
    time_dif = (end_time - start_time)
    second = time_dif % 60
    minute = (time_dif // 60) % 60
    hour = (time_dif // 60) // 60
    print('spend ' + str(hour) + 'hours,' + str(minute) + 'minutes,' + str(second) + 'seconds')


if __name__ == '__main__':
    # count_spend_time(main)
    r = requests.get('http://www.dxy.cn/bbs/thread/626626#626626')
    tree = etree.HTML(r.text)
    user = tree.xpath('//div[@class="auth"]/a/text()')
    content = tree.xpath('//td[@class="postbody"]')
    for i in range(len(user)):
        print(user[i].strip() + "：" + content[i].xpath('string(.)').strip())
        print('-' * 80)
