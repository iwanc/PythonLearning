#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup


def open_baidu():
    # driver = webdriver.Chrome("C:\\Python37\\chromedriver.exe")
    driver = webdriver.Firefox(executable_path="geckodriver")
    driver.get("https://www.baidu.com")
    assert '百度一下，你就知道' in driver.title
    print("当前URL：", driver.current_url)
    driver.quit()


def login_163mail(username, passwd):
    browser = webdriver.Firefox(executable_path="geckodriver")
    browser.get("https://mail.163.com/")
    time.sleep(3)
    browser.maximize_window()  # 最大化浏览器窗口
    time.sleep(3)
    browser.switch_to.frame(
        browser.find_element_by_xpath("//iframe[starts-with(@id,'x-URS-iframe')]"))  # 找到邮箱账号登录框对应的iframe
    email = browser.find_element_by_name('email')  # 找到邮箱账号输入框
    email.send_keys(username)  # 输入邮箱账号
    password = browser.find_element_by_name('password')  # 找到登陆密码输入框
    password.send_keys(passwd)  # 输入邮箱密码
    browser.find_element_by_id('dologin').click()


class XiciDaili:
    url = 'https://www.xicidaili.com/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6776.400 QQBrowser/10.3.2577.400"}

    def get_url_text(self):
        try:
            r = requests.get(self.url, headers=self.headers, timeout=20)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            print('无法访问网页：' + self.url)

    def get_proxy_ip(self, data):
        proxy_ip_list = []
        soup = BeautifulSoup(data, 'html.parser')
        proxy_ips = soup.find(id='ip_list').find_all('tr')
        for proxy_ip in proxy_ips:
            if len(proxy_ip.select('td')) >= 8:
                ip = proxy_ip.select('td')[1].text
                port = proxy_ip.select('td')[2].text
                protocol = proxy_ip.select('td')[5].text
                if protocol in ('HTTP', 'HTTPS', 'http', 'https'):
                    proxy_ip_list.append(f'{protocol}://{ip}:{port}')
        return proxy_ip_list

    def open_url_using_proxy(self, url, proxy):
        proxies = {}
        if proxy.startswith('HTTPS'):
            proxies['https'] = proxy
        else:
            proxies['http'] = proxy

        try:
            r = requests.get(url, headers=self.headers, proxies=proxies, timeout=10)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text, r.status_code
        except:
            print('无法访问网页：' + url)
            return False

    def check_proxy_avaliability(self, proxy):
        result = self.open_url_using_proxy('http://www.baidu.com', proxy)
        if result:
            text, status_code = result
            if status_code == 200:
                print('有效代理IP: ' + proxy)
            else:
                print('无效代理IP: ' + proxy)


if __name__ == '__main__':
    # open_baidu()
    # login_163mail('zhyld0409@163.com','******')
    xici = XiciDaili()
    print(xici.url)
    data = xici.get_url_text()
    proxy_ip_list = xici.get_proxy_ip(data)
    for proxy in proxy_ip_list:
        xici.check_proxy_avaliability(proxy)
