#!/usr/bin/env python3.7 
# -*- coding:utf-8 -*-
# Author: Lancer  2019-09-19 19:52:40

import  os,sys,re,psutil,copy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from  count_testcase   import *
from  create_testfile  import *
import css 

__Version__ = "V0.0.1"
__Author__  = "Lancer"
__Modifytime__ = "20190919"


class  MainWidows(QMainWindow):
    def  __init__(self, parent=None):
        super(MainWidows,self).__init__(parent)
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        self.resize(1000,800)
        self.setWindowTitle("Tools")
        # 整体布局
        self.basewidget = QFrame(self)
        self.workspace_layout =  QVBoxLayout()
        self.workspace_frame =  QFrame(self.basewidget)
        #self.workspace_frame.setStyleSheet("QFrame{border: 1px solid #000000}")
        self.show_choice = QGroupBox()
        self.show_choice.setTitle("界面切换")
        self.theme_choice = QGroupBox()
        self.theme_choice.setTitle("主题切换")
        self.tools_choice = QGroupBox()
        self.tools_choice.setTitle("工具栏")
        self.workspace_layout.addWidget(self.show_choice)
        self.workspace_layout.addWidget(self.theme_choice)
        self.workspace_layout.addWidget(self.tools_choice)
        self.show_layout  = QVBoxLayout()
        self.totestcase_btn = QPushButton("测试文件生成")
        self.tocase_count_btn = QPushButton("测试案例统计")
        self.show_layout.addWidget(self.totestcase_btn)
        self.show_layout.addWidget(self.tocase_count_btn)
        self.show_layout.addStretch(1)  #弹簧   空白填充的感觉
        self.show_choice.setLayout(self.show_layout)
        self.black_css = QPushButton("炫酷黑")
        self.blue_css = QPushButton("天空蓝")
        self.css_layout = QVBoxLayout()
        self.css_layout.addWidget(self.black_css)
        self.css_layout.addWidget(self.blue_css)
        self.css_layout.addStretch(1)
        self.theme_choice.setLayout(self.css_layout)
        self.about_btn = QPushButton("关于")
        self.help_btn  = QPushButton("工具使用介绍")
        self.other_layout = QVBoxLayout()
        self.other_layout.addStretch(1)
        self.other_layout.addWidget(self.about_btn)
        self.other_layout.addWidget(self.help_btn)
        self.tools_choice.setLayout(self.other_layout)
        #添加工作面板
        self.stackedWidget = QStackedWidget()
        self.createcasewidget = CreateTestFile(self.basewidget)
        self.countcasewidget  = CountTestCase(self.basewidget)
        self.stackedWidget.addWidget(self.createcasewidget)
        self.stackedWidget.addWidget(self.countcasewidget)

        self.workspace_frame.setLayout(self.workspace_layout)
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.stackedWidget)
        self.main_layout.addWidget(self.workspace_frame)
        self.main_layout.setStretchFactor(self.workspace_frame, 1)  #设置布局比例
        self.main_layout.setStretchFactor(self.stackedWidget, 9 )
        self.basewidget.setLayout(self.main_layout)
        self.setCentralWidget(self.basewidget)
        #状态栏
        self.datetime = QtCore.QDateTime.currentDateTime()  
        self.statusbar =  self.statusBar().showMessage(self.datetime.toString(QtCore.Qt.DefaultLocaleLongDate))
        #定时器
        self.timer = QtCore.QTimer(self) #初始化一个定时器
        self.timer.timeout.connect(self.app_loop) 
        self.timer.start(1000) #设置计时间隔并启动

        #信号槽
        self.totestcase_btn.clicked.connect(self.set_workwidget_01)
        self.tocase_count_btn.clicked.connect(self.set_workwidget_02)
        self.about_btn.clicked.connect(self.about_tools)
        self.help_btn.clicked.connect(self.help_ui)
        self.black_css.clicked.connect(self.set_black_css)
        self.stackedWidget.setCurrentIndex(1)
        self.setStyleSheet(css.black)
        #self.createcasewidget.setStyleSheet(css.black)
    def set_black_css(self):
        #self.workspace_frame.setStyleSheet(css.black)
        self.setStyleSheet(css.black)
        #self.statusbar.setStyleSheet("background-color:#363636; color:#FFFFFF")

    def set_workwidget_01(self):
        self.stackedWidget.setCurrentIndex(0)
    def set_workwidget_02(self):
        self.stackedWidget.setCurrentIndex(1)
    
    def about_tools(self):
        QMessageBox.about(self,"关于","版本号:%s \n作者:%s \n发布时间:%s   \n"%(__Version__,__Author__ , __Modifytime__ ))

    def help_ui(self):
        help_str = """\
        A   生成测试文件: 输入函数名 可以选则测试案例个数 点击生成按钮  会生成固定格式 test_函数名.cpp  \n
        B   测试案例统计：
        步骤   1. 点击按钮【测试报告文档选择】选择模块parasoft报告(.pdf)
               2. 点击按钮【查询具体函数按钮个】可以显示每个函数的测试案例统计个数
               3. 点击按钮【详细设计单元测试追溯表生成】 可以生成详细设计单元测试追溯表 (Excel)
        """
        QMessageBox.about(self,"帮助信息","帮助信息:\n%s "%(help_str))

    def app_loop(self):
        self.datetime = QtCore.QDateTime.currentDateTime()  
        self.statusbar =  self.statusBar().showMessage(self.datetime.toString(QtCore.Qt.DefaultLocaleLongDate))

if __name__ == "__main__":
    app  = QApplication(sys.argv)
    demo = MainWidows()
    demo.show()
    sys.exit(app.exec_())