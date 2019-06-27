import  os,sys,time,datetime,socket,threading,time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

__version__ = "V0.0.1"
__auther__ = "Lancer"
MAXlen=8*1024*1024    #当log日志数据长度大于时，关闭当前日志文件，并打开一个新的日志文件
MAXLINE=10000         #GUI中文本框中能显示的最大行数

#QTabWidget

class wslogger(QWidget):
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

    def  slot_port_print(self):
        print("选择port")

def runner():
    print("runner") 

def ui():
    print("ui") 
    app = QApplication(sys.argv)
    demo = wslogger() 
    demo.show()
    sys.exit(app.exec_())


def receiver():
    print("receiver") 
    skt=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    skt.bind(('',11506))
    while True:
        data,addr = skt.recvfrom(1472)
        a=[]
        for i in data:
            #print(type(i))
            a.append(i)
        #print("{}".format(self.a))
        l = [hex(int(i)) for i in a]
        print(" ".join(l))

def create_pthread():
    threads = []
    t1 = threading.Thread(target = runner)
    t2 = threading.Thread(target = ui)
    t3 = threading.Thread(target = receiver)

    threads.append(t1)
    threads.append(t2)
    threads.append(t3)

    for t in threads:
        # t.setDaemon(True)
        t.start()
        time.sleep(0.2)

if __name__ == "__main__":
    #创建线程，启动runner、start
    create_pthread()

