# -*- coding: utf-8 -*-
import  os,sys,time,datetime,socket,re,psutil,sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *

__version__ = "V0.0.2"
__auther__  = "Lancer"
__modifytime__ = "20190707"

'''
Version 0.0.1  20190707  创建本工具: 通过读取线路数据db文件,创建UI,便于查询驱动采集码位

'''

class bitwidget(QFrame):
    def  __init__(self,labelnames, parent=None):
        super(bitwidget,self).__init__(parent)
        self.zero_pixmap = QtGui.QPixmap ("white.png")
        self.one_pixmap = QtGui.QPixmap ("green.png")
        self.resize(100,20)
        self.setFixedSize(100,20) #w h
        self.mainlayout = QHBoxLayout(self) 
        self.labelname = QLabel(labelnames,self) #
        #self.labelname.setText("%s  %s"%(i,dbdata[i][1]))
        self.labelname.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        self.labelvalue = QLabel(self) #C:\Users\Administrator\Desktop\script_tools\iotools
        #self.labelvalue.setFixedSize(50,50) #w h
        self.labelvalue.setPixmap (self.zero_pixmap)  # 在label上显示图片
        self.labelvalue.setScaledContents (False)  # 不让图片自适应label大小
        self.labelvalue.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        self.mainlayout.addWidget(self.labelname)
        #self.mainlayout.addStretch(1)
        self.mainlayout.addWidget(self.labelvalue)
        self.mainlayout.setStretchFactor(self.labelname,2)
        self.mainlayout.setStretchFactor(self.labelvalue,1)
        self.setLayout(self.mainlayout)
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setSpacing(0)
        #self.setStyleSheet("background: lightgray; color:red; border:1px solid red; ") #border:1px solid black;
        #data
        self.index = 0
        self.value = 0
        self.name =  labelnames

    def setvalue(self):
        if  self.value == 1 :
            self.labelvalue.setPixmap (self.one_pixmap)  # 在label上显示图片
        else:
            self.labelvalue.setPixmap (self.zero_pixmap)  # 在label上显示图片
        

class  myscript(QWidget):
    def  __init__(self, parent=None):
        super(myscript,self).__init__(parent)
        self.resize(1000, 800)
        self.setWindowTitle("连锁IO码位查询工具: "+ __version__ + "  作者: " + __auther__ + "   "+ __modifytime__)
        #
        conn = sqlite3.connect('io.db')
        c = conn.cursor()
        c.execute("""select * from  driveIO""")
        self.dbdata = c.fetchall()
        print(self.dbdata)
        print(len(self.dbdata))
        
        #
        self.lineedit    = QLineEdit()
        self.upbtn = QPushButton("查询")
        self.mainlayout  = QVBoxLayout()
        self.inputlayout = QHBoxLayout() 
        self.inputlayout.addWidget(self.lineedit) 
        self.inputlayout.addWidget(self.upbtn) 
        self.inputlayout.setContentsMargins(0,0,0,0) #上下左右
        self.inputlayout.setStretchFactor(self.lineedit,10)
        self.inputlayout.setStretchFactor(self.upbtn,1)
        self.iolayout    = QGridLayout()
        self.frame = QFrame()

        self.mainlayout.addLayout(self.inputlayout)
        self.mainlayout.addWidget(self.frame)

        #self.mainlayout.addLayout(self.iolayout)
        self.mainlayout.setStretchFactor(self.inputlayout,1)
        self.mainlayout.setStretchFactor(self.iolayout,10)
        self.mainlayout.addStretch(1)
        self.setLayout(self.mainlayout)

        #test
        self.byte_label_list = [] 
        for i in  range(len(self.dbdata)):
            tttbut = bitwidget("%s %s"%(i,self.dbdata[i][1]),self)
            self.byte_label_list.append(tttbut)
            self.byte_label_list[i].move(100*int(i/24), 20*int(i%24)+50+(int(i%24)))  #x  y 绝对布局
            #self.iolayout.addWidget(self.byte_label_list[i],i%24,int(i/24))
        self.frame.setLayout(self.iolayout)
        #滚动条
        self.frame.resize(1200,800)
        self.scroll = QScrollArea(self.frame)
        #self.scroll.setWidget(self.frame)
 
        #style
        self.setStyleSheet("background: lightgray; color:red; ") #border:1px solid black;
        #信号槽
        self.upbtn.clicked.connect(self.updatavalue)
    def updatavalue(self):
        for i in  range(len(self.dbdata)):
            self.byte_label_list[i].value = 1
            self.byte_label_list[i].setvalue()

if __name__ == "__main__":
    app  = QApplication(sys.argv)
    demo = myscript()
    demo.show()
    sys.exit(app.exec_())


