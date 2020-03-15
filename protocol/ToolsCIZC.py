# -*- encoding: utf-8 -*-
#@File    : ToolsCIATS.py
#@Time    : 2020/3/15 9:30
#@Author  : Lancer

from  BaseTreeWidget import *;

from  b2vtable import * ;
from  BaseTools import * ;
from  b2v import * ;


class  ToolsCIZC(BaseTreeWidget):
    def __init__(self):
        super(ToolsCIZC, self).__init__()
        self.setWindowTitle("协议码位解析工具[ CI ZC]")
        #self.input_data.setPlainText("90090841000109410001 601429d10000008d01f4 000000b10000008d2e00 16 00080203200314080808 00040204ffff00040205ffff")


    def  slot_btn_query_data(self):
        pass



if __name__ == "__main__":
    app  = QApplication(sys.argv)
    demo = ToolsCIZC()
    demo.show()
    sys.exit(app.exec_())