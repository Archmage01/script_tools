#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @brief: 喜马拉雅声音下载

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import  (QApplication,QWidget,QProgressBar,QLabel,QLineEdit,QPushButton,QRadioButton,QGroupBox,
     QGridLayout,QVBoxLayout,QHBoxLayout,QFrame,QTableWidget,QTableWidgetItem,QMessageBox,QPlainTextEdit )
import sys ,os, re,time,random
import requests
from bs4 import BeautifulSoup

__VERSION__ = 'version: 1.0.0  time:20210407'


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.resize(500,600)
        self.setWindowTitle("喜马拉雅下载 by[Zero] "+__VERSION__)
        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.groupbox  = QGroupBox("选择类型")
        self.groupbox.setFixedHeight(50)
        hlayout = QHBoxLayout(self.groupbox)
        self.signal_m4a = QRadioButton("单个下载")
        self.mut_m4a    = QRadioButton("专辑下载")
        self.vip_signal_m4a = QRadioButton("VIP单个下载")
        self.vip_m4a    = QRadioButton("VIP专辑下载")

        hlayout.addWidget(self.signal_m4a)
        hlayout.addWidget(self.mut_m4a   )
        hlayout.addWidget(self.vip_signal_m4a)
        hlayout.addWidget(self.vip_m4a)
        self.mainlayout.addWidget(self.groupbox)

        frame01= QFrame(self)
        child_layout = QVBoxLayout()
        print(self.width())
        label01 = QLabel("链   接",self)
        label02 = QLabel("下载目录",self)
        self.url_lineedit = QLineEdit(self)
        self.dir_lineedit = QLineEdit(self)
        hlayout01 = QHBoxLayout()
        hlayout01.addWidget(label01,1)
        hlayout01.addWidget(self.url_lineedit, 9 )
        hlayout02 = QHBoxLayout()
        hlayout02.addWidget(label02,1)
        hlayout02.addWidget(self.dir_lineedit, 9 )
        child_layout.addLayout(hlayout01)
        child_layout.addLayout(hlayout02)
        child_layout.setContentsMargins(5,0,5,0) #(int left， int top， int right， int bottom)
        frame01.setLayout(child_layout)
        self.download_progressbar = QProgressBar()
        self.download_progressbar.setAlignment(QtCore.Qt.Alignment.AlignCenter)#文字居中
        self.download_progressbar.setValue(88)
        self.download_btn = QPushButton("开始下载")
        self.show_plaintextedit = QPlainTextEdit()
        self.show_plaintextedit.setMinimumHeight(400)
        self.mainlayout.addWidget(frame01)
        self.mainlayout.addWidget(self.download_progressbar)
        self.mainlayout.addWidget(self.download_btn)
        self.mainlayout.addWidget(self.show_plaintextedit)
        self.mainlayout.addStretch()
        ### 设置stylesheet
        self.download_btn.setStyleSheet('QPushButton:pressed{ text-align: center;background-color:red;}')

#html解析
class  HtmlParser(object):
    def __init__(self,url,flag=1):
        #self.url = url  #第一页
        self.url = 'https://www.ximalaya.com/youshengshu/5220851/' #
        self.base_url = 'https://www.ximalaya.com/youshengshu'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36",
        }
        self.pages_num = 0
        self.info_dict = {}  # key: ID  title  url
        # self.get_page_nums()
        # self.parser_pages()
        # self.download_m4a()

    def get_page_nums(self):
        response = requests.get(self.url, headers=self.headers)
        response.encoding = "utf-8"
        page = BeautifulSoup(response.text, "html.parser")
        try:
            pagestr = page.find_all('a', class_="page-link WJ_")[-2]
            self.pages_num = int(pagestr.find('span').text)
        except:
            pagestr = page.find_all('a', class_="page-link WJ_")[-1]
            print("只有一页")
        print("专辑页数: %d"%(self.pages_num))

    def parser_pages(self):
        for i in range(self.pages_num):
            if 0 == i:
                self.parser_page(self.url)
            else:
                self.parser_page(self.url+'p%d'%(i))
        #print(self.info_dict)

    def parser_page(self, page_url ):
        #解析单页数据
        response = requests.get( page_url, headers=self.headers)
        response.encoding = "utf-8"
        page = BeautifulSoup(response.text, "html.parser")
        try:
            pagestrs = page.find_all('li', class_="lF_")
            for pagestr in pagestrs:
                id = int(pagestr.find('span').text)
                name =  pagestr.find('a').text.strip()
                href =  self.base_url+ pagestr.find('a').get('href')
                self.info_dict[id] = [name,href]
                #print(id, name,href )
        except:
            pass

    def download_m4a(self):
        for key,values in self.info_dict.items():
            print(key, values[0], values[1] )
            try:
                nums = int(values[1].split("/")[-1])
                audio_url = 'https://www.ximalaya.com/revision/play/v1/audio?id=%d&ptype=1'%(nums)
                #print(audio_url)
                response = requests.get(audio_url, headers=self.headers)
                response.encoding = "utf-8"
                # 获得.m4a
                pattern = re.compile(r'https:.*\.m4a')
                result = pattern.findall(response.text)
                if result:
                    response = requests.get(result[0], headers=self.headers)
                    with open("mp3/%s.m4a"%(values[0]), 'wb') as f:
                        f.write(response.content)
                # print("name: ", values[0] )
                # print(result)
                time.sleep(random.randint(1, 3))
            except  FileNotFoundError as e:
                print("文件夹错误\n ")
            except Exception as ee:
                pass


#子线程
class Mythread(QtCore.QThread):
    # 定义信号,定义参数为str类型
    signal_one = QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        test = HtmlParser("=")
        print("##########")
        pass
        #while True:
        #   pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindows = MainWidget()
    mainwindows.show()
    # test = Mythread()
    # test.start()
    sys.exit(app.exec())


