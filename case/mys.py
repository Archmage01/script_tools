# -*- coding: utf-8 -*-
import  os,sys,time,datetime,socket,re,psutil
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import  templatestr 


__version__ = "V0.0.2"
__auther__  = "Lancer"
__modifytime__ = "20190702"



class  myscript(QWidget):
    def  __init__(self, parent=None):
        super(myscript,self).__init__(parent)
        self.resize(1000, 800)
        self.setWindowTitle("自用tools 版本号: "+ __version__ + "  作者: " + __auther__ + "   "+ __modifytime__)
        self.tabWidget  =  QTabWidget()
        self.Widget01   =  QWidget()
        self.Widget02   =  QWidget()
        self.tabWidget.addTab(self.Widget01  , "单元测试")
        self.tabWidget.addTab(self.Widget02  , "预留")
        self.main_layout01 = QVBoxLayout()
        self.main_layout01.addWidget(self.tabWidget)
        self.setLayout(self.main_layout01)
        #widgets01 布局
        self.m_layout01 = QHBoxLayout()
        self.labe_file_format =  QLabel("测试文件格式",self.Widget01)
        self.name_format      =  QComboBox(self.Widget01)
        self.name_format.addItem("test_函数名.cpp")
        self.name_format.addItem("函数名_test.cpp")
        self.test_casenum   =  QComboBox(self.Widget01)
        self.test_casenum.addItem("1")
        self.test_casenum.addItem("2")
        self.test_casenum.addItem("3")
        self.test_casenum.addItem("4")
        self.test_casenum.addItem("5")
        self.test_casenum.addItem("6")
        self.filename_lineedit = QLineEdit("function_name",self.Widget01)
        self.create_btn = QPushButton("生成测试文件",self.Widget01)
        self.m_layout01.addWidget(self.labe_file_format)
        self.m_layout01.addWidget(self.name_format)
        self.m_layout01.addWidget(self.test_casenum)
        self.m_layout01.addWidget(self.filename_lineedit)
        self.m_layout01.addWidget(self.create_btn)
        self.Widget01.setLayout(self.m_layout01)

        #信号槽连接
        self.create_btn.clicked.connect(self.create_test_file)

    def  create_test_file(self):  #创建测试文件
        #获得配置选项
        function_name = self.filename_lineedit.text()
        test_casenum  = int(self.test_casenum.currentText())
        index  = [1,2,3,4,5,6]
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
            print("文件:%s 已经存在"%file )
        pass


if __name__ == "__main__":
    app  = QApplication(sys.argv)
    demo = myscript()
    demo.show()
    sys.exit(app.exec_())


