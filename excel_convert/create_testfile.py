#!/usr/bin/env python3.7 
# -*- coding:utf-8 -*-
# Author: Lancer  2019-09-20 10:47:58

import  os,sys,re,psutil,copy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import  templatestr 


class CreateTestFile(QWidget):
    def  __init__(self, parent=None):
        super(CreateTestFile,self).__init__(parent)
        self.cpptest = QGroupBox()
        self.v_layout01 = QVBoxLayout()
        self.h_layout01 = QHBoxLayout(self.cpptest)  
        self.cpptest.setTitle("单元测试相关")
        self.v_layout01.addStretch(1)
        self.v_layout01.addWidget(self.cpptest)
        #self.v_layout01.addStretch(1)
        self.setLayout(self.v_layout01)
        #测试相关
        self.labe_file_format =  QLabel("测试文件格式",self.cpptest)
        self.name_format      =  QComboBox(self.cpptest)
        self.name_format.addItem("test_函数名.cpp")
        self.test_casenum   =  QComboBox(self.cpptest)
        self.test_casenum.addItem("1")
        self.test_casenum.addItem("2")
        self.test_casenum.addItem("3")
        self.test_casenum.addItem("4")
        self.test_casenum.addItem("5")
        self.test_casenum.addItem("6")
        self.test_casenum.addItem("7")
        self.test_casenum.addItem("8")
        self.filename_lineedit = QLineEdit("function_name",self.cpptest)
        self.create_btn = QPushButton("生成测试文件",self.cpptest) 
        self.h_layout01.setSpacing(10)
        self.h_layout01.addWidget(self.labe_file_format)
        self.h_layout01.addWidget(self.name_format)
        self.h_layout01.addWidget(self.test_casenum)
        self.h_layout01.addWidget(self.filename_lineedit)
        self.h_layout01.addWidget(self.create_btn)
        self.cpptest.setLayout(self.h_layout01)
        #信号槽连接
        self.create_btn.clicked.connect(self.create_test_file)

    def  create_test_file(self):  #创建测试文件
        #获得配置选项
        function_name = self.filename_lineedit.text()
        test_casenum  = int(self.test_casenum.currentText())
        index  = [1,2,3,4,5,6,7,8]
        print(function_name)
        print(test_casenum)
        case = ""
        descript01 = ""
        descript02 = ""
        for i in range(test_casenum):
            c_name = {"name":function_name, "casenum": index[i] }
            temp_case  =  (templatestr.current_case%c_name)
            temp_descript01 =  (templatestr.descript_case_01%c_name)
            temp_descript02 =  (templatestr.descript_case_02%c_name)
            case = case + temp_case
            descript01 = descript01 + temp_descript01
            descript02 = descript02 + temp_descript02
        #print(case)
        
        file = "test_" + function_name +".cpp"
        name = {"name":function_name, "casenum": index[i], "case":case, "descript01":descript01, "descript02":descript02  }
        if False == os.path.exists(file):
            testfile = open(file,"a")
            testfile.write(templatestr.test_template%name)
            testfile.close()
        else:
            QMessageBox.information(self,"新建测试文件"," %s 已经存在"%file)
            print("文件:%s 已经存在"%file )


if __name__ == "__main__":
    app  = QApplication(sys.argv)
    demo = CreateTestFile()
    demo.show()
    sys.exit(app.exec_())