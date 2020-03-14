#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2020/3/12 15:28
# @Author  : Lancer

import  os,sys,re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt

from  SendZCConfig import * ;
from  BaseTools import * ;
from  b2v import * ;


b2v_stream_head =bt2v(stream_head_b2v_table)
b2v_app_head =bt2v(app_head_b2v_table)

class  BaseTreeWidget(QWidget):
    def __init__(self,parent=None):
        super(BaseTreeWidget, self).__init__(parent)
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        self.resize(800, 800)  # w h
        self.setWindowTitle("模拟 wireshark 显示 ")
        self.input_data = QPlainTextEdit()
        self.input_data.setPlainText("90090841000109410001 601429d10000008d01f4 000000b10000008d2e00 16 00080203200314080808 00040204ffff00040205ffff")
        self.treewidget = QTreeWidget()
        self.btn_query = QPushButton("查询",self)
        layout = QVBoxLayout()
        layout_bt = QHBoxLayout()
        layout_bt.addWidget(self.input_data)
        layout_bt.addWidget(self.btn_query)
        #layout.addWidget(self.input_data)
        self.input_data.setFixedHeight(50)
        self.btn_query.setFixedHeight(50)
        layout.addLayout(layout_bt)
        layout.addWidget(self.treewidget)
        self.setLayout(layout)
        self.treewidget.setColumnCount(2)  # 设置列
        self.treewidget.setColumnWidth(0, 400)  # 设置树形控件的列的宽度
        self.treewidget.setHeaderLabels(['数据包信息', "value"])  # 设置控件标题
        #信号槽
        self.btn_query.clicked.connect(self.slot_btn_query_data)

    def  parser_ats_data(self,rec_data,rec_len):
        #分割大包  为小包存储
        list_data = []
        current_len = 0
        if rec_len < 31:
            print("数据长度小于包头长度请检查")
        else:
            current_len = 31
            rec_len = rec_len -31
            self.paser_stream_head(rec_data)
            #解析小包包头
            while rec_len>0:
                ret = b2v_app_head.bytes_to_var(rec_data[current_len:])
                # print("0x%04x"%ret['data_len'])
                # print("0x%04x"%ret['data_type'])
                #print_list(rec_data[current_len+4:current_len+2+ret['data_len']])
                list_data.append(rec_data[current_len:current_len+2+ret['data_len']])
                rec_len = rec_len - ret['data_len'] - 2
                current_len = current_len + ret['data_len']+2
        ###########解析小包数据###########
        for i  in range(len(list_data)):
            ret = b2v_app_head.bytes_to_var(list_data[i])
            if ret['data_type'] == 0x0203: #心跳包
                print("心跳包")
                self.paser_rec_ats_time(list_data[i])
            elif  ret['data_type'] == 0x0204: #站场状态包
                print("站场状态包")
            elif  ret['data_type'] == 0x0205: # 验证命令反馈包
                print("验证命令反馈包")
            elif  ret['data_type'] == 0x0206: # 执行命令反馈包
                print("执行命令反馈包")
            elif ret['data_type'] == 0x0207:  # 命令反馈包
                print("命令反馈包")
            elif ret['data_type'] == 0x0208:  # 报警信息包:
                print("报警信息包")
            else:
                return
    #通用包头
    def  paser_stream_head(self,src):
        root = QTreeWidgetItem(self.treewidget)
        root.setText(0, "通用包头")
        ret = b2v_stream_head.bytes_to_var(src)
        for i in range(len(stream_head)):
            child2 = QTreeWidgetItem(root)
            child2.setText(0, stream_head[i][0])
            child2.setText(1, ' 0x'+toStr( ret[stream_head_b2v_table[i][0]],16))

    def  paser_rec_ats_time(self,src):
        time_ats = bt2v(rec_ats_time_table)
        root = QTreeWidgetItem(self.treewidget)
        root.setText(0, "心跳包")
        ret = time_ats.bytes_to_var(src[4:])
        for i in range(len(rec_ats_time_table)):
            child2 = QTreeWidgetItem(root)
            child2.setText(0, rec_ats_time_table[i][0])
            child2.setText(1, ' 0x'+toStr( ret[rec_ats_time_table[i][0]],16))
        self.treewidget.expandAll()
    #解析各个小包数据

    # 删除控件树子节点/根节点
    def deleteItem(self):
        self.treewidget.clear()


    def  slot_btn_query_data(self):
        self.deleteItem()
        src_list = strtolist(self.input_data.toPlainText())
        self.parser_ats_data(src_list,len(src_list))

    def add_package_data(self,src_str,ltem_name, ):

        """
            添加每个小包显示UI
        :param src_str: 需要格式化显示字符串
        :return:
        """
        root = QTreeWidgetItem(self.treewidget)
        root.setText(0, ltem_name)
        ret = b2v_stream_head.bytes_to_var(strtolist(src_str))
        for i in range(len(stream_head)):
            child2 = QTreeWidgetItem(root)
            child2.setText(0, stream_head[i][0])
            child2.setText(1, ' 0x'+toStr( ret[stream_head_b2v_table[i][0]],16))
        pass



if __name__ == "__main__":
    app  = QApplication(sys.argv)
    demo = BaseTreeWidget()
    demo.show()
    sys.exit(app.exec_())