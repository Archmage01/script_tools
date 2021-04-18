#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time :2021/3/30 11:14

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import  ( QApplication,QWidget,QProgressBar,QLabel,QLineEdit,QPushButton,
     QGridLayout,QVBoxLayout,QFrame,QTableWidget,QTableWidgetItem,QMessageBox )
import sys ,os, re
import requests
from bs4 import BeautifulSoup

class MainUi(QWidget):
    def __init__(self):
        super(MainUi, self).__init__()
        self.setFixedSize(600,500)
        self.setWindowTitle("妹子图爬虫工具  version: 1.0.0 ")
        self.download_progressbar = QProgressBar()
        self.download_progressbar.setAlignment(QtCore.Qt.Alignment.AlignCenter)#文字居中
        self.download_progressbar.setStyleSheet(".QProgressBar::chunk { background-color: red;}")#背景
        self.download_progressbar.setValue(100)
        label01 = QLabel("下载URL:")
        label02 = QLabel("下载目录:")
        self.url_input    = QLineEdit()
        self.url_input.setText("https://www.mzitu.com/221746")
        self.url_input.setContentsMargins(0,0,0,0)
        self.download_dir = QLineEdit()
        self.download_dir.setContentsMargins(0,0,0,0)
        self.start_btn    = QPushButton("开始爬虫")
        self.start_btn.setFixedHeight(50)
        self.start_btn.setContentsMargins(0,0,0,0)
        inputlayout = QGridLayout()
        inputlayout.addWidget(label01, 0, 0) #第0行 0列
        inputlayout.addWidget(label02, 1, 0)
        inputlayout.addWidget(self.url_input, 0, 1)
        inputlayout.addWidget(self.download_dir, 1, 1)
        inputlayout.addWidget(self.start_btn, 0, 2, 2,1,QtCore.Qt.Alignment.AlignRight) #起始行,起始列, 占行数，占列数
        inputlayout.setColumnStretch(0, 1)  #设置每一列比例
        inputlayout.setColumnStretch(1, 10)
        inputlayout.setColumnStretch(2, 1)
        vlayout = QVBoxLayout()
        vlayout.addLayout(inputlayout)
        vlayout.addWidget(self.download_progressbar)
        self.frame = QFrame()
        self.frame.setFixedHeight(400)
        vlayout.addWidget(self.frame)
        vlayout.addStretch()
        inputlayout.setContentsMargins(0,0,0,0)
        vlayout01 = QVBoxLayout()
        self.frame.setLayout(vlayout01)
        self.qtablewidget = QTableWidget(1,3)
        self.qtablewidget.setHorizontalHeaderLabels(['目录','下载图片总数目', '删除'])
        vlayout01.addWidget(self.qtablewidget)
        self.qtablewidget.setColumnWidth(0, 358)  # 将第0列的单元格，设置成300宽度
        self.qtablewidget.setColumnWidth(1, 100 )  # 将第0列的单元格，设置成50宽度
        self.qtablewidget.verticalHeader().setVisible(False) #隐藏水平表头
        #self.qtablewidget.setDisabled(True) #设置不可编辑
        self.setLayout(vlayout)
        self.current_index = 0


    def tableupdate(self,dir, pic_num, pushbtn  ) -> None:
        self.qtablewidget.setRowCount(self.current_index+1)  #设置行
        diritem = QTableWidgetItem(str(dir))
        self.qtablewidget.setItem( self.current_index, 0, diritem)
        pic_numitem = QTableWidgetItem(str(pic_num))
        self.qtablewidget.setItem( self.current_index, 1, pic_numitem)
        self.qtablewidget.setCellWidget( self.current_index, 2, pushbtn )
        self.current_index += 1

#子线程
class Mythread(QtCore.QThread):
    # 定义信号,定义参数为str类型
    signal_one = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "Referer": "https://www.mzitu.com/"
        }
        self.url = None
        self.max_page_num = 0
        self.dir = None

    def get_max_page_num(self,url):
        response = requests.get(url, headers=self.headers)
        response.encoding = "utf-8"
        page = BeautifulSoup(response.text, "html.parser")
        ### 获得节点的src属性
        img_url = page.find('div', class_="pagenavi")
        try:
            lasturl = img_url.find_all('a')[-2].get('href')
            self.max_page_num = int(lasturl.split("/")[-1])
            return  self.max_page_num
        except:
            print("查找照片个数失败")

    def download_current_img(self,url):
        #下载图片
        response = requests.get(url,headers=self.headers)
        response.encoding = "utf-8"
        #print(response.text)
        page = BeautifulSoup(response.text,"html.parser")
        ### 获得节点的src属性
        img_url = page.find('div',class_='main-image').img['src']
        #下载
        img_name= img_url.split("/")[-1]
        response_img = requests.get(img_url, headers=self.headers)
        with open("%s/%s"%(self.dir,img_name), 'wb') as f:
            f.write(response_img.content)  # 图片内容写入文件
            f.close()
            print("url: %s  图片抓取成功：%s"%(img_url, img_name))


    def run(self):
        while True:
            # 爬虫图片
            if self.url:
                print("开始爬虫")
                self.signal_one.emit(0)
                num = self.get_max_page_num(self.url)
                for i in range(0,num+1):
                    if i == 0:
                        self.download_current_img(self.url)
                    elif i<100:
                        self.download_current_img(self.url + "/%02d" % (i))
                    else:
                        self.download_current_img(self.url + "/%03d" % (i))
                    self.signal_one.emit(int(i*100//num))
                self.url = None
                self.signal_one.emit(100)
                print("爬取完成")


#业务逻辑类(绑定相应的signal和slot，实现业务逻辑)
class MainWindow(MainUi):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.thread = Mythread()
        self.thread.start()
        self.download_progressbar.setValue(0)
        self.start_btn.clicked.connect(self.start_clicked)
        self.thread.signal_one.connect(self.download_finished)
        self.dict = {}

    def start_clicked(self):
        dir = self.download_dir.text()
        if not dir:
            QMessageBox.information(self, "错误","请输入存储目录")
            return
        if not os.path.exists(dir):
            os.mkdir(dir)
        self.thread.dir = dir
        url = self.url_input.text()
        print(url)
        self.thread.url = url
        pwd = '/'.join(os.getcwd().split('\\'))+'/'+dir
        btn = QPushButton("删除图片")
        if pwd not in self.dict:
            btn.clicked.connect(self.del_pic)
            self.dict[pwd] = btn
            self.tableupdate(pwd , self.thread.max_page_num , self.dict[pwd] )


    def download_finished(self,num):
        self.download_progressbar.setValue(num)

    def del_pic(self):
        _btn = self.sender() # btn
        for dir,btn in self.dict.items():
            if _btn is btn:
                print(dir.split("/")[-1])
                try:
                    os.system("del /q %s"%(dir.split("/")[-1]))
                    os.system("rmdir /q %s"%(dir.split("/")[-1]))
                    print("删除目录：%s 成功"%(dir.split("/")[-1]))
                except:
                    pass
                #os.remove(dir.split("/")[-1])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindows = MainWindow()
    mainwindows.show()
    sys.exit(app.exec())