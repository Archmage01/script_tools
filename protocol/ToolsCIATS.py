# -*- encoding: utf-8 -*-
#@File    : ToolsCIATS.py
#@Time    : 2020/3/15 9:30
#@Author  : Lancer

from  BaseTreeWidget import *;

from  b2vtable import * ;
from  BaseTools import * ;
from  b2v import * ;



b2v_stream_head =bt2v(stream_head_b2v_table)
b2v_app_head =bt2v(app_head_b2v_table)

num8bit = bt2v(b2v_dev_num8_table)


class  ToolsCIATS(BaseTreeWidget):
    def __init__(self):
        super(ToolsCIATS, self).__init__()
        self.setWindowTitle("协议码位解析工具[ CI ATS]")
        self.input_data.setPlainText("90090841000109410001 601429d10000008d01f4 000000b10000008d2e00 1B 0019020902030840000106FF00000004 030940000106FF80000004  ")


    def  slot_btn_query_data(self):
        self.treewidget.clear()
        src_list = strtolist(self.input_data.toPlainText())
        self.parser_ats_data(src_list,len(src_list))


    def  parser_ats_data(self,rec_data,rec_len):
        #分割大包  为小包存储
        list_data = []
        current_len = 0
        if rec_len < 31:
            print("数据长度小于包头长度请检查")
        else:
            current_len = 31
            rec_len = rec_len -31
            self.paraser_stream_head(rec_data)
            #解析小包包头
            while rec_len>0:
                ret = b2v_app_head.bytes_to_var(rec_data[current_len:])
                print("0x%04x"%ret['data_len'])
                print("0x%04x"%ret['data_type'])
                #print_list(rec_data[current_len+4:current_len+2+ret['data_len']])
                list_data.append(rec_data[current_len:current_len+2+ret['data_len']])
                rec_len = rec_len - ret['data_len'] - 2
                current_len = current_len + ret['data_len']+2
        ###########解析小包数据###########
        for i  in range(len(list_data)):
            ret = b2v_app_head.bytes_to_var(list_data[i])
            if ret['data_type'] == 0x0203: #心跳包
                self.paraser_rec_ats_time(list_data[i])
            elif  ret['data_type'] == 0x0204: #站场状态包
                self.paraser_station_data(list_data[i])
            elif  ret['data_type'] == 0x0205: # 验证命令反馈包
                self.paraser_verify_cmd_data(list_data[i])
            elif  ret['data_type'] == 0x0206: # 执行命令反馈包
                self.paraser_sure_cmd_data(list_data[i])
            elif ret['data_type'] == 0x0207:  # 命令反馈包
                self.paraser_cmd_data(list_data[i])
            elif ret['data_type'] == 0x0208:  # 报警信息包:
                self.paraser_warnning_data(list_data[i])
            elif ret['data_type'] == 0x0209:  # 普通命令包:
                self.paraser_normal_cmd_data(list_data[i])
            else:
                return
    #通用包头
    def  paraser_stream_head(self,src):
        root = QTreeWidgetItem(self.treewidget)
        root.setText(0, "通用包头")
        ret = b2v_stream_head.bytes_to_var(src)
        for i in range(len(stream_head)):
            child2 = QTreeWidgetItem(root)
            child2.setText(0, stream_head[i][0])
            child2.setText(1, tohexstr(ret[stream_head_b2v_table[i][0]]))
    #解析心跳包
    def  paraser_rec_ats_time(self,src):
        time_ats = bt2v(rec_ats_time_table)
        root = QTreeWidgetItem(self.treewidget)
        root.setText(0, "心跳包")
        ret = time_ats.bytes_to_var(src[4:])
        for i in range(len(rec_ats_time_table)):
            child2 = QTreeWidgetItem(root)
            child2.setText(0, rec_ats_time_table[i][0])
            child2.setText(1, tohexstr(ret[rec_ats_time_table[i][0]]))
        self.treewidget.expandAll()

    #站场状态包
    def  paraser_station_data(self,src):
        pass


    #普通命令包
    def  paraser_normal_cmd_data(self,src):
        normal_cmd = bt2v(b2v_ats_cmd_table)
        src = src[4:]
        root = QTreeWidgetItem(self.treewidget)
        root.setText(0, "普通命令包")
        ret = num8bit.bytes_to_var(src)
        #命令个数
        child1 = QTreeWidgetItem(root)
        child1.setText(0, b2v_dev_num8_table[0][0])
        child1.setText(1, tohexstr(ret[b2v_dev_num8_table[0][0]]))
        src = src[1:]
        print("个数"+tohexstr(ret[b2v_dev_num8_table[0][0]]))
        for i  in  range(ret[b2v_dev_num8_table[0][0]]):
            temp = src[11*i:]
            ret = normal_cmd.bytes_to_var(temp)
            child_cmd = QTreeWidgetItem(root)
            child_cmd.setText(0,"命令 "+ str(i))
            for  j  in  range(len(b2v_ats_cmd_table)):
                child2 = QTreeWidgetItem(child_cmd)
                child2.setText(0, b2v_ats_cmd_table[j][0])
                child2.setText(1, tohexstr(ret[b2v_ats_cmd_table[j][0]]))
        self.treewidget.expandAll()

    #验证命令反馈包
    def  paraser_verify_cmd_data(self,src):
        time_ats = bt2v(rec_ats_time_table)
        root = QTreeWidgetItem(self.treewidget)
        root.setText(0, "验证命令反馈包")
        child2 = QTreeWidgetItem(root)
        child2.setText(0,"src: ")
        child2.setText(1,tohexstr(src[4:]))
        self.treewidget.expandAll()

    #执行命令反馈包
    def  paraser_sure_cmd_data(self,src):
        pass

    #命令反馈包
    def  paraser_cmd_data(self,src):
        pass

    #报警信息包
    def  paraser_warnning_data(self,src):
        time_ats = bt2v(rec_ats_time_table)
        root = QTreeWidgetItem(self.treewidget)
        root.setText(0, "报警信息包")
        child2 = QTreeWidgetItem(root)
        child2.setText(0,"src: ")
        child2.setText(1,tohexstr(src[4:]))
        self.treewidget.expandAll()


if __name__ == "__main__":
    app  = QApplication(sys.argv)
    demo = ToolsCIATS()
    demo.show()
    sys.exit(app.exec_())