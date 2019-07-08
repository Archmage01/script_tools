# -*- coding: utf-8 -*-
import  os,sys,time,datetime,socket,re,psutil,sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
#from PyQt5.QtChart import *

__version__ = "V0.0.2"
__auther__  = "Lancer"
__modifytime__ = "20190708"

'''
Version 0.0.1  20190707  创建本工具: 通过读取线路数据db文件,创建UI,便于查询驱动采集码位
Version 0.0.2  20190707  重新布局UI  完善功能
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
        #self.setStyleSheet("background: lightgray; color:red; border:1px solid red; ") #border:1px solid black;
        #data
        self.index = 0
        self.value = 0
        self.name =  labelnames

    def setvalue(self):
        if  self.value == 1 :
            self.labelvalue.setPixmap (self.one_pixmap)  
        else:
            self.labelvalue.setPixmap (self.zero_pixmap) 
        

class  myscript(QWidget):
    def  __init__(self, parent=None):
        super(myscript,self).__init__(parent)
        self.resize(1300, 600)
        self.setWindowTitle("连锁IO码位查询工具: "+ __version__ + "  作者: " + __auther__ + "   "+ __modifytime__)
        self.desktop = QApplication.desktop()
        #获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        print( self.width, self.height )
        self.resize(self.width-500, self.height -200)


        dlg = QFileDialog()
        self.filenames = []

        if dlg.exec_():
            filenames= dlg.selectedFiles()
            #f = open(filenames[0], 'r') 
        print(os.getcwd())

        #
        conn = sqlite3.connect(filenames[0])
        c = conn.cursor()
        c.execute("""select * from  driverinfo""")
        self.dbdata = c.fetchall()
        #print(self.dbdata)
        print(len(self.dbdata))
        #####################################################################
        self.mainframe = QWidget(self)
        self.mainframe.resize(self.width-500,self.height -200)
        self.ioboard   = QWidget()
        self.ioboard.resize( self.width*2, self.height) #######设置滚动条的尺寸  
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.ioboard)
        self.mainlayout  = QVBoxLayout()
        self.mainlayout.addWidget(self.scroll)
        self.mainframe.setLayout(self.mainlayout)

        self.lineedit    = QLineEdit()
        self.upbtn = QPushButton("全部查询")
        self.upbtn.setFixedSize(90,25)
        self.signallineedit    = QLineEdit("0x00")
        self.signallineedit.setFixedSize(90,25)
        self.signal_byteindex   =  QComboBox()
        self.signal_byteindex.setFixedSize(90,25)
        self.signal_upbtn = QPushButton("单字节查询")
        self.signal_upbtn.setFixedSize(90,25)
        self.clear_upbtn = QPushButton("重置")
        self.clear_upbtn.setFixedSize(90,25)
        self.mainlayoutio  = QVBoxLayout(self.ioboard)
        self.inputlayout = QHBoxLayout() 
        self.inputlayout.addWidget(self.signal_upbtn)
        self.inputlayout.addWidget(self.signal_byteindex)
        self.inputlayout.addWidget(self.signallineedit) 
        self.inputlayout.addWidget(self.clear_upbtn) 
        self.inputlayout.addWidget(self.upbtn) 
        self.inputlayout.addWidget(self.lineedit) 
        self.inputlayout.setContentsMargins(0,0,0,0) #上下左右
        self.inputlayout.setStretchFactor(self.signal_upbtn,1)
        self.inputlayout.setStretchFactor(self.signal_byteindex,1)
        self.inputlayout.setStretchFactor(self.signallineedit,1)
        self.inputlayout.setStretchFactor(self.clear_upbtn,1)
        self.inputlayout.setStretchFactor(self.upbtn,1)
        self.inputlayout.setStretchFactor(self.lineedit,10)
        self.iolayout    = QGridLayout(self.ioboard)
        self.frame = QFrame()

        for  i in  range(int((len(self.dbdata)+7)/8)):
            self.signal_byteindex.addItem("%d"%(i))

        self.mainlayoutio.addLayout(self.inputlayout)
        self.mainlayoutio.addWidget(self.frame)
        self.mainlayoutio.setStretchFactor(self.inputlayout,1)
        self.mainlayoutio.setStretchFactor(self.iolayout,10)
        self.mainlayoutio.addStretch(1)
        self.ioboard.setLayout(self.mainlayoutio)

        #test
        self.byte_label_list = [] 
        for i in  range(len(self.dbdata)):
            tttbut = bitwidget("%s %s"%(i,self.dbdata[i][1]),self.ioboard) # 6  1
            self.byte_label_list.append(tttbut)
            self.byte_label_list[i].move(200*int(i/24), 20*int(i%24)+50+(int(i%24)))  #x  y 绝对布局
            #self.iolayout.addWidget(self.byte_label_list[i],i%24,int(i/24))
        self.frame.setLayout(self.iolayout)

        self.setStyleSheet("background: lightgray; color:black; ") #border:1px solid black;
        #信号槽
        self.upbtn.clicked.connect(self.updatavalue)
        self.signal_upbtn.clicked.connect(self.signal_updatavalue)
        self.clear_upbtn.clicked.connect(self.clear_io)
        
    def clear_io(self):
        for i in  range(len(self.dbdata)):
            self.byte_label_list[i].value = 0
            self.byte_label_list[i].setvalue()

    def updatavalue(self):
        for i in  range(len(self.dbdata)):
            self.byte_label_list[i].value = 1
            self.byte_label_list[i].setvalue()
    def signal_updatavalue(self):
        #print(self.signallineedit.text())
        getvalue = int(self.signallineedit.text(),16)
        index  =  int(self.signal_byteindex.currentText())
        print(getvalue, index )
        for i  in  range((index*8),(index+1)*8):
            if i < len(self.dbdata):
                bit_n = i%8
                self.byte_label_list[i].value = self.get_bit_value(getvalue,bit_n+1)
                #print((bit_n+1), self.byte_label_list[i].value )
                self.byte_label_list[i].setvalue()
            else:
                pass
        
    def  get_bit_value(self, src ,nbit):
        dst = 0
        if src>255:
            print("入参错误src大于0xFF")
        else:
            if nbit > 8 or nbit< 1:
                print("入参错误nbit大于8 or nbit 小于1")
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


