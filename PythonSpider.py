#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: skyxnet
"""

import requests
import re


def get_movie_info():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6776.400 QQBrowser/10.3.2577.400"
    }
    for i in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start=%s&filter=' % i
        res = requests.get(url, headers=headers)
        pattern = re.compile(
            r'.*?<em class="">(\d+)</em>.*?<span class="title">(.*?)</span>.*?<p class="">.*?: (.*?)[&nbsp|\.\.\.].*? (\d+).*?</p>',
            re.S)
        mlist = pattern.findall(res.text)
        for m in mlist:
            moive = {
                'rank': m[0],
                'title': m[1],
                'director': m[2],
                'year': m[3]
            }
            print(moive)


if __name__ == '__main__':
    # requests get
    r = requests.get('https://www.baidu.com')
    r.encoding = 'utf-8'
    print(r.status_code)
    print(r.headers['content-type'])
    print(r.encoding)
    # print(r.text)

    # requests post
    postUrl = "https://fanyi.baidu.com/v2transapi"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6776.400 QQBrowser/10.3.2577.400",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    data = {
        "from": "zh",
        "to": "en",
        "query": "人生苦短,我用Python"
    }
    response = requests.post(postUrl, headers=headers, data=data)
    print(response.status_code)
    print(response.text)

    # douban-top250
    get_movie_info()
