import  os,sys,time,datetime,socket,threading
from PyQt5.QtCore import *
from PyQt5.QtGui    import *
from PyQt5.QtWidgets import *

__version__ = "V0.0.1"
__auther__ = "Lancer"

class  UI(QTabWidget):
    def  __init__(self, parent=None):
        super(UI,self).__init__(parent)
        self.initUI()
        
    def  initUI(self):
        #add  four widgets
        self.sc_cpu1  = QWidget()
        self.sc_cpu2  = QWidget()
        self.app_cpu1 = QWidget()
        self.app_cpu2 = QWidget()
        # add  top leve
        self.addTab(self.sc_cpu1  , "sc-cpu1")
        self.addTab(self.sc_cpu2  , "sc-cpu2")
        self.addTab(self.app_cpu1 , "app-cpu1 ")
        self.addTab(self.app_cpu2 , "app-cpu2 ")

        self.resize(1000,800)
        self.setWindowTitle(__version__+"   " +__auther__)

        #layout
        self.mainlayout01  =  QVBoxLayout()
        self.mainlayout02  =  QVBoxLayout()
        self.mainlayout03  =  QVBoxLayout()
        self.mainlayout04  =  QVBoxLayout()

        self.btnlayout01  =   QHBoxLayout()
        self.btnlayout02  =   QHBoxLayout()
        self.btnlayout03  =   QHBoxLayout()
        self.btnlayout04  =   QHBoxLayout()

        self.btn_clear01 =  QPushButton("clear")
        self.btn_clear02 =  QPushButton()
        self.btn_clear03 =  QPushButton()
        self.btn_clear04 =  QPushButton()

        self.lebel_01 = QLabel("一键清除")
        self.lebel_02 = QLabel()
        self.lebel_03 = QLabel()
        self.lebel_04 = QLabel()

        self.btn_frame_sc_cpu1  = QFrame()
        self.btn_frame_sc_cpu2  = QFrame()
        self.btn_frame_app_cpu1 = QFrame()
        self.btn_frame_app_cpu2 = QFrame()

        #wiget01
        self.btnlayout01.addWidget( self.lebel_01)
        self.btn_frame_sc_cpu1.setLayout( self.btnlayout01)
        self.mainlayout01.addWidget(self.btn_frame_sc_cpu1)
        self.mainlayout01.addWidget(self.btn_clear01)
        self.sc_cpu1.setLayout( self.mainlayout01)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	demo = UI() 	
	demo.show()
	sys.exit(app.exec_())
