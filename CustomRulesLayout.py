#!/usr/bin/env python
# -*- coding:utf-8 -*-
#自定义UI解析规则 便于处理繁琐重复布局

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  ( QMainWindow,QApplication,QMenu,QAction,QStatusBar,QStackedWidget,QWidget,QDialog,
                               QLayout,QVBoxLayout,QHBoxLayout,QGridLayout,QPushButton,QRadioButton,QLineEdit,QFrame,QLabel,
                               QGroupBox,QTextEdit,QButtonGroup,QFileDialog,QProgressBar,QTabWidget,QComboBox,QTableWidget )
from PyQt5.QtCore import Qt
import sys,os


'''
QLabel("Label01"), QLineEdit(""), QPushButton("发送"), "A1:B1:B1#4",
三个控件布局比例 1:1:1
    A: 子布局addStretch
    B: 子布局前addStretch
    #: 顶层布局所占比例
    A: 顶层布局后addStretch
    B: 顶层布局前addStretch
QLabel("Label01"),  "1#1T",
'''

class LayoutAnalysisV(object):
    '''
    整体垂直布局,childlayout水平布局(从上到下,从左到右)
    '''
    def __init__(self, base, rulestab ):
        '''
        :param     base: Widget
        :param rulestab: 自定义待解析规则表格
        '''
        self.basewidget , self.rulestab = base , rulestab

    def child_item_parsing(self, childuilist, toplayout , rules ):
        childlayout =  QHBoxLayout()
        childlayout.setContentsMargins(0,0,0,0)
        if (rules.count(":") + 1) != len(childuilist):
            print("布局配置错误, 请检查...")
        childnums, topnum = rules.split("#")
        childnums = childnums.split(":")
        for i in range(len(childuilist)):
            if childnums[i].startswith("A"):
                num = int(childnums[i].replace('A',''))
                childlayout.addWidget(childuilist[i], num )
                childlayout.addStretch(1)
            elif childnums[i].startswith("B"):
                num = int(childnums[i].replace('B', ''))
                childlayout.addStretch(1)
                childlayout.addWidget(childuilist[i], num)
            else:
                childlayout.addWidget(childuilist[i], int(childnums[i]))
        # add childlayout
        if topnum.endswith("A"):
            topnum = int(topnum.replace("A",""))
            toplayout.addLayout( childlayout, topnum )
            toplayout.addStretch(1)
        elif topnum.endswith("B"):
            topnum = int(topnum.replace("B", ""))
            toplayout.addStretch(1)
            toplayout.addLayout(childlayout, topnum)
        else:
            toplayout.addLayout( childlayout, int(topnum))

    def transform(self):
        self.toplayout  = QVBoxLayout()
        self.toplayout.setContentsMargins(2, 2, 2, 2)
        #实际解析
        childuilist = []  # 布局控件
        for item in self.rulestab:
            if isinstance(item, str):  # 判断是否是字符串
                self.child_item_parsing(childuilist, self.toplayout,item )
                pass
                #清空
                childuilist.clear()
            else:
                childuilist.append(item)
        self.basewidget.setLayout(self.toplayout)
        return  self.basewidget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    rules01 = [
        QLabel("Label01"), QLineEdit(""), QPushButton("发送"), QPushButton("发1送"), "1:1:1:1#10",
        QPushButton("垂垂老矣"), QPushButton("垂垂老矣"), "1:1#3",
        QLabel("Label02"), QLineEdit(""), QPushButton("1发送"), QPushButton("发送2"), "1:1:1:1#1A",
    ]
    ui  = LayoutAnalysisV( QWidget(), rules01 ).transform()
    ui.show()
    ui.resize(400,300)
    sys.exit(app.exec_())
