#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @brief: 爬虫M3U8链接识别
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import  ( QApplication,QWidget,QProgressBar,QLabel,QLineEdit,QPushButton,
     QGridLayout,QVBoxLayout,QFrame,QTableWidget,QTableWidgetItem,QMessageBox,QPlainTextEdit )
import sys ,os, re
import requests
from bs4 import BeautifulSoup

class MainUi(QWidget):
    def __init__(self):
        super(MainUi, self).__init__()
        self.setWindowTitle("M3U8识别工具 [by: Zero]")
        self.resize(400,300)
        mainlayout = QVBoxLayout(self)
        self.setLayout(mainlayout)
        self.frame = QFrame()
        grid = QGridLayout(self.frame)
        label01 = QLabel("链 接")
        label02 = QLabel("文件名")
        self.url_lineedit = QLineEdit()
        self.filename_lineedit = QLineEdit()
        grid.addWidget(label01, 0,0,1,1,alignment=QtCore.Qt.Alignment.AlignCenter)
        grid.addWidget(label02, 1,0,1,1,alignment=QtCore.Qt.Alignment.AlignCenter)
        grid.addWidget(self.url_lineedit, 0, 1,1,5)
        grid.addWidget(self.filename_lineedit, 1, 1,1,5)
        grid.setContentsMargins(1,1,1,1)
        self.start_btn = QPushButton("开始识别")
        self.copy_btn = QPushButton("复制内容")
        grid.addWidget(self.start_btn, 2, 0,1,3)
        grid.addWidget(self.copy_btn, 2, 3,1,3)
        self.show_plaintextedit = QPlainTextEdit()
        mainlayout.addWidget(self.frame)
        mainlayout.addWidget(self.show_plaintextedit)
        mainlayout.addStretch()
        self.start_btn.clicked.connect(self.start_clicked)
        self.copy_btn.clicked.connect(self.copy_m3u8)



    def start_clicked(self):
        self.m3u8_set = set()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        }
        url = self.url_lineedit.text()
        response = requests.get(url, headers= headers)
        response.encoding = "utf-8"
        #print(response.text)
        pattern  = re.compile(r'https:.*\.m3u8')
        results = pattern.findall(response.text)
        for result in results:
            self.m3u8_set.add(result)
        # print(results)
        # print(self.m3u8_set,type(self.m3u8_set))
        showstr = ''
        self.show_plaintextedit.clear()
        for c in self.m3u8_set:
            showstr+= c+"\n"
        self.show_plaintextedit.setPlainText(showstr)

    def copy_m3u8(self):
        self.show_plaintextedit.selectAll()
        self.show_plaintextedit.copy()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindows = MainUi()
    mainwindows.show()
    sys.exit(app.exec())