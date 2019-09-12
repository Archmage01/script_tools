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
        self.setWindowTitle("文件名批量修改工具")
        self.current_dir = os.getcwd()
        self.filename_list =  os.listdir(self.current_dir)
        #print(self.current_dir)
        #print(self.filename_list )
        self.type_name = []
        self.dict_type_name = {}
        for i  in  range(len(self.filename_list)):
            file_type = self.filename_list[i].split(".")[-1]
            if  file_type not in  self.type_name:
                self.type_name.append(file_type)

        print(self.type_name)
        for  i  in  range(len(self.type_name)):
            for j  in  range(len(self.filename_list)):
                file_type = self.filename_list[j].split(".")[-1]
                file_name = self.filename_list[j].split(".")[0]
                if file_type ==  self.type_name[i]:
                    self.dict_type_name.setdefault(self.type_name[i],[]).append(file_name)
        print(self.dict_type_name)
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
        self.lineedit_01 = QLineEdit()
        self.radiobtn_02  =  QRadioButton("格式2:")
        self.labe_02 =  QLabel("数字在后:")
        self.lineedit_02 = QLineEdit()
        self.radiobtn_03  =  QRadioButton("格式3:")
        self.labe_03 =  QLabel("+数字+")
        self.lineedit_0301 = QLineEdit()
        self.lineedit_0302 = QLineEdit()
        self.labe_04  =  QLabel("数字位数")
        self.btn_grounp = QButtonGroup(self)
        self.btn_grounp.addButton(self.radiobtn_01)
        self.btn_grounp.addButton(self.radiobtn_02)
        self.btn_grounp.addButton(self.radiobtn_03)

        self.numcheckbox_01 = QRadioButton("1位(0)")
        self.numcheckbox_02 = QRadioButton("2位(00)")
        self.numcheckbox_03 = QRadioButton("3位(000)")
        self.numcheckbox_04 = QRadioButton("4位(0000)")
        self.btn_check_grounp = QButtonGroup(self)
        self.btn_check_grounp.addButton(self.numcheckbox_01)
        self.btn_check_grounp.addButton(self.numcheckbox_02)
        self.btn_check_grounp.addButton(self.numcheckbox_03)
        self.btn_check_grounp.addButton(self.numcheckbox_04)

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
        self.name_layout04.addWidget(self.labe_04)
        self.name_layout04.addWidget(self.numcheckbox_01)
        self.name_layout04.addWidget(self.numcheckbox_02)
        self.name_layout04.addWidget(self.numcheckbox_03)
        self.name_layout04.addWidget(self.numcheckbox_04)
        self.radio_layout.addLayout(self.name_layout01,0, 0)
        self.radio_layout.addLayout(self.name_layout02,0, 1)
        self.radio_layout.addLayout(self.name_layout03,1, 0)
        self.radio_layout.addLayout(self.name_layout04,1, 1)
        self.filedir.setLayout(self.radio_layout)

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
        self.listWidget.addItems(self.dict_type_name[self.type_name[0]])
        #self.listWidget.addItem("Item 2")
        self.filelist_layout.addWidget(self.filedirframe)
        self.filelist_layout.addWidget(self.listWidget)
        self.file_list.setLayout(self.filelist_layout)
         
        #style
        #self.setStyleSheet("background: lightgray; color:red;")
        #连接信号槽
        self.chage_btn.clicked.connect(self.chage_file_name)
        self.help_btn.clicked.connect(self.about_tools)
    #
    def get_name_type(self,file_num):
        dst_name_list = []
        #print("获得命名规则 本类文件个数 %d "%file_num)
        #print(self.numcheckbox_01.isChecked())
        if True == self.radiobtn_01.isChecked():
            for i  in range(file_num):
                name =  str(i) + self.lineedit_01.text() 
                dst_name_list.append(name)
        if True == self.radiobtn_02.isChecked():
            for i  in range(file_num):
                name =   self.lineedit_02.text() + str(i)
                dst_name_list.append(name)
        if True == self.radiobtn_03.isChecked():
            for i  in range(file_num):
                name =   self.lineedit_0301.text() + str(i) + self.lineedit_0302.text()
                dst_name_list.append(name)
        return dst_name_list
        
    def chage_file_name(self):
        _file_type = self.filetype.currentText()
        num = len(self.dict_type_name[_file_type])
        new_name_list = self.get_name_type(num)
        print(new_name_list)
        print(self.dict_type_name[_file_type])
        for i in range(len(self.dict_type_name[_file_type])):
            os.rename( self.dict_type_name[_file_type][i]+".%s"%_file_type, new_name_list[i]+".%s"%_file_type  )
        #os.rename(old,new)
        print("修改文件名")
    #提示本工具信息
    def about_tools(self):
        QMessageBox.about(self,"关于","版本号:%s 作者:%s \n 发布时间:%s"%(__VERSION__,__AUTHOR__,"20190912" ))
    

if __name__ == "__main__":
    app  = QApplication(sys.argv)
    demo = Tools_ui()
    demo.show()
    sys.exit(app.exec_())