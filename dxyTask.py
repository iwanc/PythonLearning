#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@File    :   dxyTask.py
@Time    :   2019/04/13 09:49:27
@Author  :   skyXnet
@Version :   1.0
@Contact :   skyxnet@vip.qq.com
@License :   (C)Copyright 2019-2019, skyxnet-lian
@Desc    :   None
"""

import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def login_dxy(browser, username, password):
    try:
        # 点击“登录”
        browser.find_element_by_link_text('登录').click()
        # 点击“电脑登录”
        browser.find_element_by_class_name('ico_pc').click()
        # 输入账号
        element = browser.find_element_by_name('username')
        element.clear()
        element.send_keys(username)
        # 输入密码
        element = browser.find_element_by_name('password')
        element.clear()
        element.send_keys(password)
        # 点击“登录按钮”
        browser.find_element_by_class_name('button').click()
    except TimeoutException:
        print('Time out')
    except NoSuchElementException:
        print('No Element')


def get_content(browser):
    print("登录成功")
    time.sleep(10)
    auth = browser.find_elements_by_class_name('auth')  # 姓名
    level = browser.find_elements_by_class_name('info')  # 级别
    user_atten = browser.find_elements_by_class_name('user_atten')  # 积分-得票-丁当
    content = browser.find_elements_by_class_name('postbody')  # 回复内容
    fw = open('data.txt', 'a', encoding='utf-8')
    for i in range(len(content)):
        num = user_atten[i].find_elements_by_tag_name('a')
        data = str(
            {'num': i + 1, 'name': auth[i].text, 'level': level[i].text, 'score': num[0].text, 'vote': num[2].text,
             'dingdang': num[4].text,
             'content': content[i].text.replace(" ", "").replace("\n", "")}) + "\n"  # 去除空格和换行符\n
        fw.writelines(data)
    print("写入成功")
    fw.close()


if __name__ == '__main__':
    browser = webdriver.Firefox(executable_path="geckodriver")
    browser.get('http://www.dxy.cn/bbs/thread/626626#626626')
    login_dxy(browser, 'zywpbexk@mail.bccto.me', '******')
    get_content(browser)
    browser.quit()
