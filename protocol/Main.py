# -*- encoding: utf-8 -*-
#@File    : Main.py.py
#@Time    : 2020/3/15 9:56
#@Author  : Lancer


import  os,sys,re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt

from  ToolsCIATS import *;
from  ToolsCIZC import *;


class  ToolsMainUI(QTabWidget):
    def __init__(self):
        super(ToolsMainUI, self).__init__()
        self.resize(800,800)
        self.setWindowTitle("协议解析工具")
        self.widget_ciats = ToolsCIATS()
        self.widget_cizc = ToolsCIZC()
        self.addTab(self.widget_ciats, "协议解析CIATS")
        self.addTab(self.widget_cizc, "协议解析CIZC")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = ToolsMainUI()
    demo.show()
    sys.exit(app.exec_())