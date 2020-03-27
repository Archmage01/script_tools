#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2020/3/26 13:41
# @Author  : Lancer

import  os,sys,re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from  BaseTreeWidget  import *
from  ToolsCIATS import *

VERSION = "  version: 0.0.1"


class   MainUI(QWidget):
    def __init__(self):
        super(MainUI, self).__init__()
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        self.resize(self.width, self.height)
        self.resize( self.width/2,self.height/2)
        self.setWindowTitle("仿wireshark UI协议解析工具"+VERSION)
        # add bar

        layout_h_01 = QHBoxLayout()
        self.btn_ciats = QPushButton("CI ATS协议解析")
        self.btn_cizc = QPushButton("CI ZC协议解析")
        layout_h_01.addWidget(self.btn_ciats)
        layout_h_01.addWidget(self.btn_cizc)
        layout_h_01.addStretch()

        mainlayout = QVBoxLayout()
        mainlayout.addLayout(layout_h_01)
        self.setLayout(mainlayout)
        self.stack_widget = QStackedWidget()
        mainlayout.addWidget(self.stack_widget)

        widget_ciats = ToolsCIATS()
        widget_cizc  = BaseTreeWidget()
        # widget_cizc.setStyleSheet('background:red')
        # widget_ciats.setStyleSheet('background:yellow')
        self.stack_widget.addWidget(widget_ciats)
        self.stack_widget.addWidget(widget_cizc)

        self.btn_ciats.clicked.connect(self.slot_show_ui_ciats)
        self.btn_cizc.clicked.connect(self.slot_show_ui_cizc)

    def  slot_show_ui_ciats(self):
        self.stack_widget.setCurrentIndex(0)

    def  slot_show_ui_cizc(self):
        self.stack_widget.setCurrentIndex(1)


if __name__ == "__main__":
    app  = QApplication(sys.argv)
    demo = MainUI()
    demo.show()
    demo.showMaximized()
    sys.exit(app.exec_())