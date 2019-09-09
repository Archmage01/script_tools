#!/usr/bin/env python3.7 
# -*- coding:utf-8 -*-
# Author: Lancer  2019-09-09 10:09:56


import  os,sys,re,psutil
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

__VERSION__ = "0.0.1"
__AUTHOR__ = "Lancer"

class Tools_ui(QWidget):
    def  __init__(self, parent=None):
        super(Tools_ui,self).__init__(parent)
        self.resize(800,1000)
        self.setWindowTitle("文件名批量修改工具 "+" 版本号: "+ __VERSION__ +"作者: " + __AUTHOR__ )
        #self.setFixedSize(800,600) #w h
        #add  QGroupBox
        self.top_layout = QVBoxLayout()
        self.filedir = QGroupBox()
        self.filedir.setTitle("文件名设置(不含扩展名)")
        self.file_list = QGroupBox()
        self.file_list.setTitle("当前目录下文件列表")
        self.help_btn = QPushButton("关于本工具")
        self.chage_btn = QPushButton("开始修改")
        self.file_label = QLabel("文件后缀:")
        self.filetype = QComboBox()
        self.type_name = ["c","cpp","py","lua"]
        self.filetype.addItems(self.type_name)
        self.btn_layout = QHBoxLayout()
        self.btn_layout.addWidget(self.file_label)
        self.btn_layout.addWidget(self.filetype)
        self.btn_layout.addWidget(self.help_btn)
        self.btn_layout.addWidget(self.chage_btn)
        self.btnframe = QFrame()
        self.btnframe.setLayout(self.btn_layout)
        self.top_layout.addWidget(self.filedir)
        self.top_layout.addWidget(self.file_list)
        self.top_layout.addWidget(self.btnframe)
        self.top_layout.setStretchFactor(self.filedir, 1 )
        self.top_layout.setStretchFactor(self.file_list, 8 )
        self.top_layout.setStretchFactor(self.btnframe, 1 )
        self.setLayout( self.top_layout )
        #文件名规则UI设置
        self.radiobtn_01  =  QRadioButton("格式1:")
        self.labe_01 =  QLabel("数字在前:")
        self.lineedit_01 = QLineEdit("文件名")
        self.radiobtn_02  =  QRadioButton("格式2:")
        self.labe_02 =  QLabel("数字在后:")
        self.lineedit_02 = QLineEdit("文件名")
        self.radiobtn_03  =  QRadioButton("格式3:")
        self.labe_03 =  QLabel("+数字+")
        self.lineedit_0301 = QLineEdit()
        self.lineedit_0302 = QLineEdit()
        self.radiobtn_04  =  QRadioButton("格式4:")
        self.radio_layout = QGridLayout()
        self.name_layout01 = QHBoxLayout()
        self.name_layout02 = QHBoxLayout()
        self.name_layout03 = QHBoxLayout()
        self.name_layout04 = QHBoxLayout()
        self.name_layout01.addWidget(self.radiobtn_01)
        self.name_layout01.addWidget(self.labe_01)
        self.name_layout01.addWidget(self.lineedit_01)
        self.name_layout02.addWidget(self.radiobtn_02)
        self.name_layout02.addWidget(self.labe_02)
        self.name_layout02.addWidget(self.lineedit_02)
        self.name_layout03.addWidget(self.radiobtn_03)
        self.name_layout03.addWidget(self.lineedit_0301)
        self.name_layout03.addWidget(self.labe_03)
        self.name_layout03.addWidget(self.lineedit_0302)
        self.name_layout04.addWidget(self.radiobtn_04)
        self.radio_layout.addLayout(self.name_layout01,0, 0)
        self.radio_layout.addLayout(self.name_layout02,0, 1)
        self.radio_layout.addLayout(self.name_layout03,1, 0)
        self.radio_layout.addLayout(self.name_layout04,1, 1)
        self.filedir.setLayout(self.radio_layout)
        self.radio_layout.addLayout

        # 文件列表显示
        self.filelist_layout = QVBoxLayout()
        self.listWidget = QListWidget()
        self.filedirbtn_layout = QHBoxLayout()
        self.clear_btn =  QPushButton("清空文件列表")
        self.updata_btn = QPushButton("更新文件列表")
        self.filedirbtn_layout.addWidget(self.clear_btn)
        self.filedirbtn_layout.addWidget(self.updata_btn)
        self.filedirframe = QFrame()
        self.filedirframe.setLayout(self.filedirbtn_layout)
        #self.file_list
        self.listWidget.addItem("Item 1")
        self.listWidget.addItem("Item 2")
        self.filelist_layout.addWidget(self.filedirframe)
        self.filelist_layout.addWidget(self.listWidget)
        self.file_list.setLayout(self.filelist_layout)
         
        #style
        #self.setStyleSheet("background: lightgray; color:red;")


if __name__ == "__main__":
    app  = QApplication(sys.argv)
    demo = Tools_ui()
    demo.show()
    sys.exit(app.exec_())