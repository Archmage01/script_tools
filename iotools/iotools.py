# -*- coding: utf-8 -*-
import  os,sys,re,psutil,sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
#import numpy as np

__version__ = "V0.0.3"
__auther__  = "Lancer"
__modifytime__ = "201907016"

'''
Version 0.0.1  20190707  创建本工具: 通过读取线路数据db文件,创建UI,便于查询驱动采集码位
Version 0.0.2  20190707  重新布局UI  完善功能
Version 0.0.3  20190716  支持查询全部数据(基本功能完成)
'''


class bitwidget(QWidget):
    def  __init__(self,labelnames, parent=None):
        super(bitwidget,self).__init__(parent)
        self.zero_pixmap = QtGui.QPixmap ("white.png")
        self.one_pixmap = QtGui.QPixmap ("green.png")
        self.resize(200,20)
        self.setFixedSize(200,20) #w h
        self.mainlayout = QHBoxLayout(self) 
        self.labelname = QLabel(labelnames,self) #
        self.labelname.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelvalue = QLabel(self) 
        self.labelvalue.setPixmap (self.zero_pixmap)  # 在label上显示图片
        self.labelvalue.setScaledContents (False)  # 不让图片自适应label大小
        self.labelvalue.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)  #QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter
        self.mainlayout.addWidget(self.labelname)
        #self.mainlayout.addStretch(1)
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
    def  __init__(self, parent=None):
        super(myscript,self).__init__(parent)
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        self.resize(self.width*3/4, self.height*3/4) #w h
        self.setWindowTitle("连锁IO码位查询工具: "+ __version__ + "  作者: " + __auther__ + "   "+ __modifytime__)
        self.mainwidget = QWidget()
        self.setWidget(self.mainwidget)
        #读取db文件
        dlg = QFileDialog()
        self.filenames = []

        if dlg.exec_():
            filenames= dlg.selectedFiles()
        print(os.getcwd())
        conn = sqlite3.connect(filenames[0])
        c = conn.cursor()
        c.execute("""select * from  driverinfo""")
        self.dbdata = c.fetchall()
        #UI 创建处理UI分布
        self.lineedit    = QLineEdit()
        self.upbtn = QPushButton("查询IO码位")
        self.upbtn.setFixedSize(90,25)
        self.clear_upbtn = QPushButton("重置")
        self.clear_upbtn.setFixedSize(90,25)
        self.inputlayout = QHBoxLayout() 
        self.inputlayout.addWidget(self.clear_upbtn)
        self.inputlayout.addWidget(self.upbtn)
        self.inputlayout.addWidget(self.lineedit)

        self.boardlayout = QGridLayout() 
        self.mainlayout  = QVBoxLayout()
        self.mainlayout.addLayout(self.inputlayout)
        self.mainlayout.addLayout(self.boardlayout)
        self.mainlayout.addStretch(1)
        self.setLayout(self.mainlayout)
         #每个小单元存储24 io  计算个数
        self.iobitnum = int(len(self.dbdata))
        self.boardnum = (self.iobitnum + 23)/24 
        if self.boardnum*200 <  self.width*3/4:
            self.mainwidget.resize(self.width*3/4, self.height*3/4) #reset size
        else:
            self.mainwidget.resize(self.boardnum*200,self.height) #reset size

        self.byte_label_list = []
        for i in  range(len(self.dbdata)): 
            tttbut = bitwidget("%s %s"%(i,self.dbdata[i][1]),self.mainwidget) # 6  1
            self.byte_label_list.append(tttbut)
            self.byte_label_list[i].move(200*int(i/24), 20*int(i%24)+50+(int(i%24)))
        #信号槽
        self.upbtn.clicked.connect(self.updatavalue)
        self.clear_upbtn.clicked.connect(self.clear_io)

    def clear_io(self):
        for i in  range(self.iobitnum):
            self.byte_label_list[i].value = 0
            self.byte_label_list[i].setvalue()

    def updatavalue(self):
        bytelen =  (int(len(self.lineedit.text().strip())+1)//2)
        expect_len =  len(self.dbdata)
        expect_len = int((expect_len + 7)/8)
        print(self.lineedit.text())
        regex_input = '(([0-9]|[A-F]|[a-f])+)'
        inputstr = self.lineedit.text().strip()
        rr1 = re.compile(regex_input)
        if rr1.match(inputstr) is  None:
            self.lineedit.setText('请填写正确输入IO码位值(0-9 a-f A-F)')
            print(rr1.match(inputstr))
            return
        else:
            print(rr1)
            if len(self.lineedit.text().strip()) != len(rr1.match(inputstr)[0]):
                self.lineedit.setText('请填写正确输入IO码位值(0-9 a-f A-F)')
                return
        data = []
        valuestr = self.lineedit.text().strip()
        print(valuestr)
        for i in range(len(valuestr)):
            if i%2 == 0 :
                data.append(valuestr[i:i+2])

        for i  in  range(len(data)):
            data[i] = int(data[i],16)
        if  bytelen  ==  expect_len:
            print("iput len OK")
            for  k in  range(expect_len):
                for i  in range(0,8):
                    print(i)
                    temp  = 8*k+i
                    if  temp < len(self.dbdata):
                        self.byte_label_list[8*k+i].value = self.get_bit_value(data[k], i+1)
                        self.byte_label_list[8*k+i].setvalue()
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

if __name__ == "__main__":
    app  = QApplication(sys.argv)
    demo = myscript()
    demo.show()
    sys.exit(app.exec_())


