import  os,sys,time,datetime,socket,threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

__version__ = "V0.0.1"
__auther__ = "Lancer"

#QTabWidget

class wslogger(QWidget):
    def  __init__(self, parent=None):
        super(wslogger,self).__init__(parent)
        self.resize(1000, 800)
        self.setWindowTitle("wslogger 版本号: "+ __version__ + "  作者: " + __auther__ )

        self.tabWidget =  QTabWidget()
        self.btnWidget =  QTabWidget()
        self.main_layout =  QVBoxLayout()

        self.textEdit01 =  QTextEdit()
        self.textEdit02 =  QTextEdit()
        self.textEdit03 =  QTextEdit()
        self.textEdit04 =  QTextEdit()

        self.tabWidget.addTab(self.textEdit01  , "APP-CPU1")
        self.tabWidget.addTab(self.textEdit02  , "APP-CPU2")
        self.tabWidget.addTab(self.textEdit03  , "SC-CPU1")
        self.tabWidget.addTab(self.textEdit04  , "SC-CPU2")
        
        
        self.main_layout.addWidget(self.tabWidget)
        self.main_layout.addWidget(self.btnWidget)
        self.main_layout.setStretch(0,30)
        self.main_layout.setStretch(1,1)
        self.setLayout(self.main_layout)

        self.btnlayout  =   QHBoxLayout(self.btnWidget)
        self.clear_label =  QLabel("一键清除",self.btnWidget)
        self.clear_btn   =  QPushButton("清除",self.btnWidget)
        self.stop_label =   QLabel("底行追踪",self.btnWidget)
        self.stop_btn   =   QPushButton("Stop",self.btnWidget)
        self.font_label =   QLabel("字体大小",self.btnWidget)
        self.fontbox    =   QComboBox(self.btnWidget)
        self.fontbox.addItem("14")
        self.fontbox.addItem("15")
        self.port_label =   QLabel("监听端口",self.btnWidget)
        self.portbox    =   QComboBox(self.btnWidget)
        self.portbox.addItem("10100")
        self.portbox.addItem("10200")
        self.portbox.addItem("10300")

        self.btnlayout.addWidget(self.clear_label)
        self.btnlayout.addWidget(self.clear_btn)
        self.btnlayout.addWidget(self.stop_label)
        self.btnlayout.addWidget(self.stop_btn)
        self.btnlayout.addWidget(self.font_label)
        self.btnlayout.addWidget(self.fontbox)
        self.btnlayout.addWidget(self.port_label)
        self.btnlayout.addWidget(self.portbox)
        self.btnlayout.setContentsMargins(0, 0, 0, 0)
        self.btnlayout.setSpacing(5)
        self.btnWidget.setLayout(self.btnlayout)
        #self.btnWidget.setStyleSheet("background:rgba(0,0,0,0.2)")
        self.setStyleSheet(".QLabel{color:red;} ")



if __name__ == '__main__':
	app = QApplication(sys.argv)
	demo = wslogger() 
	demo.show()
	sys.exit(app.exec_())
