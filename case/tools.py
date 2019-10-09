#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: yang.gan  2019-9-8 19:45:56# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tools.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *


css = """
    QPushButton{background-color:#1E1E1E; color:#6a9955; border-color:green; border-width:1px; }  
    QPushButton:hover{background-color:#1E1E1E; color:#6a9955;  border: 1px solid #008B00;  }  
    QPushButton:pressed{background-color:red; color:white;  }  
    QLabel{background-color:#1E1E1E; color:#6a9955 } 
    QLabel:hover{background-color:#1E1E1E; color: red;   }  
    QWidget{background-color:#1E1E1E; color:#6a9955 } 
    QComboBox{background-color:#1E1E1E; color:#6a9955 } 
    QComboBox:hover{background-color:#1E1E1E; color: red;   }  
    QLineEdit{background-color:#1E1E1E; color:#6a9955; border: 0px solid #008B00; border-bottom-width:1px  } 
"""

'''
css = """
    QPushButton:pressed{background-color:red; color:white;  }  
"""
'''

__VERSION__ = "版本号:0.0.3"
__AUTHOR__ = "作者:Lancer "

class Ui_tools(QWidget):
    def __init__(self):
        super(Ui_tools,self).__init__()
        self.resize(800,200)
        self.setWindowTitle("Tools"+"   "+ __VERSION__ + " " + __AUTHOR__ )
        mainlayout = QVBoxLayout()

        self.cfilechose_btn =  QPushButton("待处理C文件选择")
        self.function_num_label = QLabel("函数个数:")
        self.function_num_label.setAlignment(QtCore.Qt.AlignCenter)
        self.notfind_label =   QLabel("未找到测试文件函数个数:")
        self.case_num_label =  QLabel("测试案例总个数统计:")
        self.notfind_label.setAlignment(QtCore.Qt.AlignCenter)
        self.case_num_label.setAlignment(QtCore.Qt.AlignCenter)
        self.filestyle_label = QLabel("测试文件格式:test_函数名.cpp")
        self.pdfchose_btn =  QPushButton("parasoft测试报告选择")
        self.excel_create_btn =  QPushButton("生成单元测试详细设计追溯表")
        self.allfile_btn =  QPushButton("批量测试文件生成")
        self.sigfile_btn =  QPushButton("单个测试文件生成")
        self.funname_lineEdit =  QLineEdit("function_name")
        self.funname_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.one_casenum_spin =  QSpinBox(self)
        self.one_casenum_spin.setMinimum(1)
        self.one_casenum_spin.setMaximum(10)
        self.n_casenum_spin = QSpinBox(self)
        self.n_casenum_spin.setMinimum(1)
        self.n_casenum_spin.setMaximum(10)
        self.one_casenum_spin.setFixedWidth(40)
        self.n_casenum_spin.setFixedWidth(40)

        hlayout01 = QHBoxLayout()
        hlayout02 = QHBoxLayout()
        hlayout03 = QHBoxLayout()
        hlayout04 = QHBoxLayout()

        hlayout01.addWidget(self.cfilechose_btn)
        hlayout01.addWidget(self.function_num_label)
        hlayout01.addWidget(self.one_casenum_spin)
        hlayout01.addWidget(self.allfile_btn)
        hlayout01.setStretchFactor(self.cfilechose_btn, 1 )
        hlayout01.setStretchFactor(self.function_num_label, 1)
        hlayout01.setStretchFactor(self.one_casenum_spin, 1)
        hlayout01.setStretchFactor(self.allfile_btn, 1 )
        hlayout02.addWidget(self.filestyle_label)
        hlayout02.addWidget(self.funname_lineEdit)
        hlayout02.addWidget(self.n_casenum_spin)
        hlayout02.addWidget(self.sigfile_btn)
        hlayout03.addWidget(self.pdfchose_btn)
        hlayout03.addWidget(self.excel_create_btn)
        hlayout03.setStretchFactor(self.pdfchose_btn, 1 )
        hlayout03.setStretchFactor(self.excel_create_btn, 1)
        hlayout04.addWidget(self.case_num_label)
        hlayout04.addWidget(self.notfind_label)
        mainlayout.addLayout(hlayout01)
        mainlayout.addSpacing(7)
        mainlayout.addLayout(hlayout02)
        mainlayout.addSpacing(7)
        mainlayout.addLayout(hlayout03)
        mainlayout.addSpacing(7)
        mainlayout.addLayout(hlayout04)
        mainlayout.addStretch(0)
        self.setLayout(mainlayout)
        self.setStyleSheet(css)


if __name__ == "__main__":
    import sys
    app  = QApplication(sys.argv)
    main_widget = QWidget()
    demo = Ui_tools()
    demo.show()
    sys.exit(app.exec_())




