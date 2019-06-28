import  os,sys,time,datetime,socket,threading,time,re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

__version__ = "V0.0.1"
__auther__ = "Lancer"
MAXlen=8*1024*1024    #当log日志数据长度大于时，关闭当前日志文件，并打开一个新的日志文件
MAXLINE=10000         #GUI中文本框中能显示的最大行数

count_num = 0 

#QTabWidget

class wslogger(QWidget):
    emit_signal = QtCore.pyqtSignal(str)
    def  __init__(self, parent=None):
        super(wslogger,self).__init__(parent)
        self.resize(1000, 800)
        self.setWindowTitle("wslogger 版本号: "+ __version__ + "  作者: " + __auther__ )
        self.tabWidget =  QTabWidget()
        self.btnWidget =  QTabWidget()
        self.main_layout = QVBoxLayout()
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
        self.font_btn   =   QPushButton("设置字体大小",self.btnWidget)
        self.fontbox    =   QComboBox(self.btnWidget)
        self.fontbox.addItem("14")
        self.fontbox.addItem("15")
        self.fontbox.addItem("16")
        self.fontbox.addItem("17")
        self.port_btn   =   QPushButton("设置监听端口",self.btnWidget)
        self.portbox    =   QComboBox(self.btnWidget)
        self.portbox.addItem("10100")
        self.portbox.addItem("10200")
        self.portbox.addItem("10300")
        self.btnlayout.addWidget(self.clear_label)
        self.btnlayout.addWidget(self.clear_btn)
        self.btnlayout.addWidget(self.stop_label)
        self.btnlayout.addWidget(self.stop_btn)
        self.btnlayout.addWidget(self.font_btn)
        self.btnlayout.addWidget(self.fontbox)
        self.btnlayout.addWidget(self.port_btn)
        self.btnlayout.addWidget(self.portbox)
        self.btnlayout.setContentsMargins(0, 0, 0, 0)
        self.btnlayout.setSpacing(5)
        self.btnWidget.setLayout(self.btnlayout)
        #self.btnWidget.setStyleSheet("background:rgba(0,0,0,0.2)")
        self.setStyleSheet(".QLabel{color:red;} .QPushButton{color:green;} ")
        self.port_btn.clicked.connect(self.slot_port_print)
        self.stop_btn.clicked.connect(self.stop_flag_set )
        self.clear_btn.clicked.connect(self.clear )
        #stop_flag
        self.stop_flag  = 0 
        #更新线程
        self.t=threading.Thread(target=self.udp_receive)
        self.t.start() 
        self.emit_signal.connect(self.main_loop)


    def  stop_flag_set(self):
        if  0 == self.stop_flag:
            self.stop_flag  = 1
            self.stop_btn.setText("开始")
        else:
            self.stop_flag = 0 
            self.stop_btn.setText("停止")

    def  clear(self):
        self.textEdit01.clear()

    def udp_receive(self):
        #UDP通信接受报文
        self.skt=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.skt.bind(('',11506))
        while True:
            data,addr=self.skt.recvfrom(1472)
            self.a=[]
            for i in data:
                #print(type(i))
                self.a.append(i)
            l = [hex(int(i)) for i in self.a]
            print(" ".join(l))
            if  0 == self.stop_flag:
                self.emit_signal.emit(" ".join(l)+"\n")
            

    def  slot_port_print(self):
        global count_num 
        count_num = count_num -1
        print("选择port  %d "%count_num)

    def  main_loop(self,data):
        print(data)
        self.textEdit01.insertPlainText(data)
        pass   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = wslogger()
    demo.show()
    sys.exit(app.exec_())

