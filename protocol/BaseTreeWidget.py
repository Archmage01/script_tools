#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2020/3/12 15:28
# @Author  : Lancer

import  os,sys,re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt


class  BaseTreeWidget(QWidget):
    def __init__(self,parent=None):
        super(BaseTreeWidget, self).__init__()
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        self.resize(800, 800)  # w h
        self.setWindowTitle("模拟 wireshark 显示 ")
        self.input_data = QPlainTextEdit("")
        self.treewidget = QTreeWidget()
        self.btn_query = QPushButton("查询",self)
        layout = QVBoxLayout()
        layout_bt = QHBoxLayout()
        layout_bt.addWidget(self.input_data)
        layout_bt.addWidget(self.btn_query)
        self.input_data.setFixedHeight(50)
        self.btn_query.setFixedHeight(50)
        layout.addLayout(layout_bt)
        layout.addWidget(self.treewidget)
        self.setLayout(layout)
        self.treewidget.setColumnCount(2)  # 设置列
        self.treewidget.setColumnWidth(0, 400)  # 设置树形控件的列的宽度
        self.treewidget.setHeaderLabels(['数据包信息', "value"])  # 设置控件标题
        #信号槽
        self.btn_query.clicked.connect(self.slot_btn_query_data)


    def  slot_btn_query_data(self):
        '''
        查询按钮槽函数   须子类重写
        :return:
        '''
        pass

if __name__ == "__main__":
    app  = QApplication(sys.argv)
    demo = BaseTreeWidget()
    demo.show()
    sys.exit(app.exec_())