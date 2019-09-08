#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import threading
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication,QMainWindow
from image_spider import Ui_Form
from baidu_image_spider import BaiduImageSpider

class UIBaiduImageSpider(QMainWindow,Ui_Form):
    htmlGet = QtCore.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(UIBaiduImageSpider, self).__init__(*args,**kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_click_start)

        # 同步更新内容
        self.htmlGet.connect(lambda s: self.textBrowser.append(s))

    def on_click_start(self):
        word = self.lineEdit.text()
        if not word:
            self.log("请输入您要下载的壁纸名称")
            return

        pic_count = self.spinBox.value()
        if pic_count<1:
            self.log("下载图片数不能少于1张")
            return

        self.pushButton.setEnabled(False)
        t = threading.Thread(target=UIBaiduImageSpider.download,
                             args=(self, word, pic_count),
                             name='thread')
        t.start()

    def download(self, word, pic_count):
        spider = BaiduImageSpider()
        spider.set_keyword(word)

        # 创建下载目录
        dir_path = spider.make_dir(word)
        self.log('壁纸下载目录: '+dir_path)

        # 翻页解析图片列表
        img_url_list = []
        for page in range(10):
            img_url_list.extend(spider.parse_page(page))
            self.log("第{}页解析完成".format(page+1))
            if len(img_url_list)>pic_count:
                break

        img_count = min(len(img_url_list),pic_count)
        img_url_list = img_url_list[:img_count]
        if img_count>0:
            self.log("即将下载{}个图片文件".format(img_count))
            for img_url in img_url_list:
                # 图片下载
                if spider.download_image(img_url):
                    self.log("下载成功: "+img_url)
                else:
                    self.log("下载失败: "+img_url)
        else:
            self.log("没有可下载的文件")

        self.pushButton.setEnabled(True)
        self.log("全部下载完成！")

    def log(self, str_info):
        print(str_info)
        self.htmlGet.emit(str_info)

if __name__=='__main__':
    app = QApplication(sys.argv)
    widget = UIBaiduImageSpider()
    widget.show()
    sys.exit(app.exec_())
