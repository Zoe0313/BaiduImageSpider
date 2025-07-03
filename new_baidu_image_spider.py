#!/usr/bin/env python3

import os
import requests
from urllib import parse
from lxml import etree
from PIL import Image

class BaiduImageSpider(object):
    def __init__(self):
        # 最热优先，超大图1080px以上，横图，高清，30张
        self.url = 'https://image.baidu.com/search/index?tn=resulttagjson&word={}&ie=utf-8&fp=result&fr=&ala=0&pn=0&rn=30&nojc=0&gsm=5a&newReq=1&hot=1&z=7&imgratio=4&hd=1&data_type=json'
        self.keyword = ''
        self.path = ''
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def set_keyword(self,word):
        self.keyword = parse.quote(word)

    def parse_page(self):
        url = self.url.format(self.keyword)
        result = requests.get(url, headers=self.headers)
        data = result.json()['data']
        images = data['images']
        print(len(images))
        # json_str = json.dumps(images, indent=4)
        # print(json_str)
        img_url_list = []
        for image in images:
            img_url = image['objurl']
            img_name = image['titleShow']
            byte_data = bytes(ord(char) for char in img_name)
            img_name = byte_data.decode('utf-8')
            img_url_list.append(img_url)
            print('title: %s, url: %s' % (img_name, img_url))
        print(len(img_url_list))
        return img_url_list

    def download_image(self, img_url):
        try:
            res = requests.get(url=img_url,headers=self.headers,timeout=5)
            if not 200 <= res.status_code < 300:
                return False
        except Exception as e:
            return False

        filename = img_url.split('/')[-1][-10:]
        img_path = os.path.join(self.path, filename)
        with open(img_path, 'wb') as f:
            f.write(res.content)
        if not self.is_image(img_path):
            os.remove(img_path)
        return True

    def make_dir(self, word):
        self.path = word
        dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        return dir_path

    def is_image(self, img_path):
        try:
            image = Image.open(img_path)
            width, height = image.size
            print('{0}x{1}'.format(width, height))
            image.close()
            return True
        except:
            pass
        return False

if __name__ == "__main__":
    search_name = "4K高清 名侦探柯南"
    spider = BaiduImageSpider()
    spider.make_dir(search_name)
    spider.set_keyword(search_name)
    image_url_list = spider.parse_page()
    for image_url in image_url_list:
        spider.download_image(image_url)

