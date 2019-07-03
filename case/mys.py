# -*- coding: utf-8 -*-
import  os,sys,time,datetime,socket,re,psutil
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *

import  templatestr 


__version__ = "V0.0.2"
__auther__  = "Lancer"
__modifytime__ = "20190702"



class  myscript(QWidget):
    def  __init__(self, parent=None):
        super(myscript,self).__init__(parent)
        self.resize(800, 600)
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
        self.v_layout01 = QVBoxLayout()
        self.m_layout01 = QHBoxLayout()
        self.v_layout01.setSpacing(0)
        self.m_layout01.setSpacing(0)
        self.widget0101 = QWidget(self.Widget01)
        self.widget0102 = QWidget(self.Widget01)
        self.v_layout01.addWidget(self.widget0101)
        self.v_layout01.addWidget(self.widget0102)
        self.Widget01.setLayout(self.v_layout01)

        self.teeee =  QPushButton("折线图",self.widget0102)

        self.labe_file_format =  QLabel("测试文件格式",self.widget0101)
        self.name_format      =  QComboBox(self.widget0101)
        self.name_format.addItem("test_函数名.cpp")
        self.name_format.addItem("函数名_test.cpp")
        self.test_casenum   =  QComboBox(self.widget0101)
        self.test_casenum.addItem("1")
        self.test_casenum.addItem("2")
        self.test_casenum.addItem("3")
        self.test_casenum.addItem("4")
        self.test_casenum.addItem("5")
        self.test_casenum.addItem("6")
        self.filename_lineedit = QLineEdit("function_name",self.widget0101)
        self.create_btn = QPushButton("生成测试文件",self.widget0101)
        self.m_layout01.addWidget(self.labe_file_format)
        self.m_layout01.addWidget(self.name_format)
        self.m_layout01.addWidget(self.test_casenum)
        self.m_layout01.addWidget(self.filename_lineedit)
        self.m_layout01.addWidget(self.create_btn)
        self.widget0101.setLayout(self.m_layout01)

        #信号槽连接
        self.create_btn.clicked.connect(self.create_test_file)
        self.teeee.clicked.connect(self.test)
        # stylesheet  
        #self.widget0101.setStyleSheet("background: rgba(238, 232, 205,0.8);") #EEE8CD
        #self.Widget01.setStyleSheet("background: rgba(238, 232, 205,0.8);")
        self.tabWidget.setStyleSheet("background: rgba(238, 232, 205,0.8);")
        #self.Widget01.setStyleSheet("color:black; background:lightgray ;  ")
    def test(self):
        self.series_1 = QLineSeries()
        self._1_point_0 = QtCore.QPointF(0.00,0.00) #定义折线坐标点
        self._1_point_1 = QtCore.QPointF(0.80,6.00)
        self._1_point_2 = QtCore.QPointF(2.00,2.00)
        self._1_point_3 = QtCore.QPointF(4.00,3.00)
        self._1_point_4 = QtCore.QPointF(1.00,3.00)
        self._1_point_5 = QtCore.QPointF(5.00,3.00)
        self._1_point_list = [self._1_point_0,self._1_point_1,self._1_point_4,self._1_point_2,self._1_point_3,self._1_point_5] #定义折线点清单
        self.series_1.append(self._1_point_list) #折线添加坐标点清单
        self.series_1.setName("案例统计")#折线命名
        self.x_Aix = QValueAxis()#定义x轴，实例化
        self.x_Aix.setRange(0.00,5.00) #设置量程
        self.x_Aix.setLabelFormat("%0.2f")#设置坐标轴坐标显示方式，精确到小数点后两位
        self.x_Aix.setTickCount(6)#设置x轴有几个量程
        self.x_Aix.setMinorTickCount(0)#设置每个单元格有几个小的分级
        
        self.y_Aix = QValueAxis()#定义y轴
        self.y_Aix.setRange(0.00,6.00)
        self.y_Aix.setLabelFormat("%0.2f")
        self.y_Aix.setTickCount(7)
        self.y_Aix.setMinorTickCount(0)

        self.charView = QChartView(self.Widget02)  #定义charView，父窗体类型为 Window
        self.v_layout022 = QVBoxLayout()
        self.v_layout022.addWidget(self.charView)
        self.Widget02.setLayout(self.v_layout022)

        self.charView.setGeometry(0,0,self.width(),self.height())  #设置charView位置、大小
        self.charView.chart().addSeries(self.series_1)  #添加折线
        self.charView.chart().setAxisX(self.x_Aix) #设置x轴属性
        self.charView.chart().setAxisY(self.y_Aix) #设置y轴属性
        self.charView.show()#显示charView

        print("zhexiantu")
        pass


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
            #QMessageBox.information(self,"文件已经存在") QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes
            QMessageBox.information(self,"新建测试文件"," %s 已经存在"%file)
            print("文件:%s 已经存在"%file )
        


if __name__ == "__main__":
    app  = QApplication(sys.argv)
    demo = myscript()
    demo.show()
    sys.exit(app.exec_())


