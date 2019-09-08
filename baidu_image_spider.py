#!/usr/bin/env python3

import os
import time
import random
import requests
from urllib import parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class BaiduImageSpider(object):
    def __init__(self):
        self.url = 'http://image.baidu.com/search/index?ct=&tn=baiduimage&word={}&pn={}'
        self.keyword = ''
        self.path = ''
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

    def set_keyword(self,word):
        self.keyword = parse.quote('壁纸 {}'.format(word))

    def parse_page(self,page):
        url = self.url.format(self.keyword,page,1440,900)

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.get(url)

        try:
            self.browser.find_element_by_xpath('//*[@id="avfilter_msize"]/div[3]/a[2]').click()
            time.sleep(2)
        except Exception as e:
            print('没找到可点击的分辨率')

        # 把下拉菜单拉到底部,执行JS脚本
        self.browser.execute_script(
            'window.scrollTo(0,document.body.scrollHeight)'
        )
        time.sleep(4)

        img_url_list = []
        img_elements = self.browser.find_elements_by_xpath('//li[@class="imgitem"]')#
        for element in img_elements:
            img_url = element.get_attribute('data-objurl')
            img_url_list.append(img_url)

        self.browser.close()
        return img_url_list

    def download_image(self,img_url):
        try:
            html = requests.get(url=img_url,headers=self.headers,timeout=5).content
        except Exception as e:
            return False

        filename = img_url.split('/')[-1]
        with open(self.path + filename,'wb') as f:
            f.write(html)
            time.sleep(random.randint(1,3))
        return True

    def make_dir(self, word):
        self.path = word + '/'
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),self.path)
        return dir_path
