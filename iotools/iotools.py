#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Author: Lancer
# @File  new_tools.py
# @Time  2019/7/21 9:15

import  os,sys,re,psutil,sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

__version__ = "V0.0.5"
__auther__  = "Lancer"
__modifytime__ = "20190724"

'''
Version 0.0.1  20190707  创建本工具: 通过读取线路数据db文件,创建UI,便于查询驱动采集码位
Version 0.0.2  20190707  重新布局UI  完善功能
Version 0.0.3  20190716  支持查询全部数据(基本功能完成)
Version 0.0.4  20190722  支持.c转DB文件  整条线路IO查询
Version 0.0.5  20190724  支持大小端查询
'''


class bitwidget(QWidget):
    def  __init__(self,labelnames, parent=None):
        super(bitwidget,self).__init__(parent)
        self.zero_pixmap = QtGui.QPixmap ("white.png")
        self.one_pixmap = QtGui.QPixmap ("green.png")
        self.resize(280,20)
        self.setFixedSize(280,20) #w h
        self.mainlayout = QHBoxLayout(self) 
        self.labelname = QLabel(labelnames,self) #
        self.labelname.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelvalue = QLabel(self) 
        self.labelvalue.setPixmap (self.zero_pixmap)  # 在label上显示图片
        self.labelvalue.setScaledContents (False)  # 不让图片自适应label大小
        self.labelvalue.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)  #QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter
        self.mainlayout.addWidget(self.labelname)
        self.mainlayout.addWidget(self.labelvalue)
        self.mainlayout.setStretchFactor(self.labelname,4)
        self.mainlayout.setStretchFactor(self.labelvalue,1)
        self.setLayout(self.mainlayout)
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setSpacing(0)
        self.index = 0
        self.value = 0
        self.name =  labelnames

    def setvalue(self):
        if  self.value == 1 :
            self.labelvalue.setPixmap (self.one_pixmap)  
        else:
            self.labelvalue.setPixmap (self.zero_pixmap) 
        

class  myscript(QScrollArea):
    def  __init__(self, dbdata, parent=None):
        super(myscript,self).__init__(parent)
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        self.resize(self.width*3/4, self.height*3/4) #w h
        self.mainwidget = QWidget()
        self.setWidget(self.mainwidget)
        self.mode = 1  #大端模式   0:小端模式
        self.dbdata = dbdata

        #UI 创建处理UI分布
        self.lineedit    = QLineEdit(self.mainwidget)
        self.lineedit.setFixedSize(self.width*3/4 -230,25)
        self.upbtn = QPushButton("查询IO码位",self.mainwidget)
        self.upbtn.setFixedSize(90,25)
        self.clear_upbtn = QPushButton("重置",self.mainwidget)
        self.clear_upbtn.setFixedSize(90,25)  #w h
        self.mode_btn = QPushButton("大端",self.mainwidget)
        self.mode_btn.setFixedSize(60,25)  #w h
        self.clear_upbtn.move(10, 10)
        self.mode_btn.move(100, 10)
        self.upbtn.move(170, 10)
        self.lineedit.move(260, 10)

         #每个小单元存储24 io  计算个数
        self.iobitnum = int(len(self.dbdata))
        self.boardnum = (self.iobitnum + 23)/24 
        if self.boardnum*280 <  self.width*3/4:
            self.mainwidget.resize(self.width*3/4, self.height*3/4) #reset size
        else:
            self.mainwidget.resize(self.boardnum*280,self.height) #reset size

        self.byte_label_list = []
        for i in  range(len(self.dbdata)): 
            tttbut = bitwidget("%s %s"%(i,self.dbdata[i][1]),self.mainwidget) # 6  1
            self.byte_label_list.append(tttbut)
            self.byte_label_list[i].move(10+280*int(i/24), 20*int(i%24)+50+(int(i%24)))
        #信号槽
        self.upbtn.clicked.connect(self.updatavalue)
        self.clear_upbtn.clicked.connect(self.clear_io)
        self.mode_btn.clicked.connect(self.set_mode)

    def set_mode(self):
        if 1 == self.mode:
            self.mode = 0 
            self.mode_btn.setText("小端")
            self.mode_btn.setStyleSheet("background: green")
        else:
            self.mode = 1
            self.mode_btn.setText("大端")
            self.mode_btn.setStyleSheet("background: red")
    #大小端转化
    def valuechage(self,src):
        ret = str(bin(src))[2:]
        ret = ret[::-1]
        length = 8 - len(ret)
        for i in range(length):
            ret = ret + "0"
        return int(str(int(ret, 2)))

    def clear_io(self):
        for i in  range(self.iobitnum):
            self.byte_label_list[i].value = 0
            self.byte_label_list[i].setvalue()

    def updatavalue(self):
        bytelen =  (int(len(self.lineedit.text().strip()))//2)
        expect_len =  len(self.dbdata)
        expect_len = int((expect_len + 7)/8)
        regex_input = '^[0-9a-fA-F]+$'
        inputstr = self.lineedit.text().strip()
        rr1 = re.compile(regex_input)
        if rr1.search(inputstr) is  None:
            self.lineedit.setText('请填写正确输入IO码位值(0-9 a-f A-F)')
            QMessageBox.warning(self, '错误提示信息',"请输入合法的16进制数据(无0x)")
            return
        else:
            pass
        data = []
        valuestr = self.lineedit.text().strip()
        for i in range(len(valuestr)):
            if i%2 == 0 :
                data.append(valuestr[i:i+2])

        for i  in  range(len(data)):
            data[i] = int(data[i],16)
            if self.mode == 0: #小端模式
                data[i] = self.valuechage(data[i])
        if  bytelen  ==  expect_len  :
            if  0 == (int(len(self.lineedit.text().strip()))%2):
                print("iput len OK")
                for  k in  range(expect_len):
                    for i  in range(0,8):
                        temp  = 8*k+i
                        if  temp < len(self.dbdata):
                            self.byte_label_list[8*k+i].value = self.get_bit_value(data[k], i+1)
                            self.byte_label_list[8*k+i].setvalue()
            else:
                QMessageBox.warning(self, '错误提示信息',"输入多4bit")
        else:
            if  1 == ( expect_len- bytelen):
                if  1 == (int(len(self.lineedit.text().strip()))%2):
                    QMessageBox.warning(self, '错误提示信息',"输入少4bit")
                else:
                    QMessageBox.warning(self, '错误提示信息',"输入码位长度不对:%d 实际配置:%d 字节"%(bytelen,expect_len))
            else:
                QMessageBox.warning(self, '错误提示信息',"输入码位长度不对:%d 实际配置:%d 字节"%(bytelen,expect_len))


    def  get_bit_value(self, src ,nbit):
        dst = 0
        if src>255:
            print("入参错误src大于0xFF")
        else:
            if nbit > 8 or nbit< 1:
                print("入参错误nbit大于8 or nbit 小于1: %d"%nbit)
            else:
                #print((2**(8-nbit)), dst)
                dst = src & (2**(8-nbit))
                if dst == (2**(8-nbit)):
                    dst = 1
                else:
                    dst = 0
        return (dst)


class  ToolsUi(QScrollArea):
        def  __init__(self, parent=None):
            super(ToolsUi,self).__init__(parent)
            self.desktop = QApplication.desktop()
            self.screenRect = self.desktop.screenGeometry()
            self.height = self.screenRect.height()
            self.width = self.screenRect.width()
            self.resize(self.width*3/4, self.height*3/4) #w h
            self.setWindowTitle("连锁IO码位查询工具: "+ __version__ + "  作者: " + __auther__ + "   "+ __modifytime__)
            #加载数据库文件
            dlg = QFileDialog()
            self.filenames = []
            self.db_table_name_list = [ ]
            self.all_dbdata = []
            if dlg.exec_():
                filenames= dlg.selectedFiles()
            #print(os.getcwd())
            conn = sqlite3.connect(filenames[0])
            c = conn.cursor()
            c.execute("select name from sqlite_master where type='table' order by name")
            t_table_head = c.fetchall()
            for  i  in  range(len(t_table_head)):
                self.db_table_name_list.append(t_table_head[i][0])
            #存储.db文件中  所有表数据
            for  i  in  range(len(self.db_table_name_list)):
                c.execute("""select * from  %s"""%(self.db_table_name_list[i]))
                per_dbdata =  c.fetchall()
                self.all_dbdata.append(per_dbdata)

            #布局UI
            self.mainwidget = QTabWidget(self)
            self.main_layout = QVBoxLayout()
            self.resize(self.width*3/4, self.height*3/4)
            self.setWidget(self.mainwidget)
            print("数据表个数:%d "%(len(self.all_dbdata)))
            for  i  in  range(len(self.all_dbdata)):
                self.widget_i = myscript(self.all_dbdata[i], self)
                self.mainwidget.addTab(self.widget_i, self.db_table_name_list[i])
            self.mainwidget.setTabShape(QTabWidget.TabShape.Triangular )
            self.main_layout.addWidget(self.mainwidget)
            self.setLayout(self.main_layout)
        #设置当前标签颜色
        def  paintEvent(self,QPaintEven):
            count   =  self.mainwidget.count()
            index  = self.mainwidget.currentIndex()
            for  i  in  range(count):
                if  i == index:
                    self.mainwidget.tabBar().setTabTextColor(index, QtGui.QColor(255, 0, 0))
                else:
                    self.mainwidget.tabBar().setTabTextColor(i, QtGui.QColor(0, 0, 0))

if __name__ == "__main__":
    app  = QApplication(sys.argv)
    demo = ToolsUi()
    demo.show()
    sys.exit(app.exec_())