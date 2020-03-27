# -*- encoding: utf-8 -*-
#@File    : ToolsCIATS.py
#@Time    : 2020/3/15 9:30
#@Author  : Lancer

from  BaseTreeWidget import *;
from  b2vtable import *
from  public  import  *


####  小包类型 ####
AC_TIME_INFO    = 0x0201  #ATS时钟心跳包
AC_BTN_CMD_INFO = 0x0203  #按钮及控制命令包
AC_CMD_VERIFY_INFO   = 0x0207  #安全命令验证信息包
AC_CMD_SURE_INFO     = 0x0209  #安全命令执行信息包
AC_VIRTUAL_IO_INFO   = 0x020D  #虚拟IO信息包

CA_STATION_INFO  = 0x0202 #站场状态信息包
CA_WARNING_INFO  = 0x0204 #故障报警信息包
CA_FEEDBAKC_INFO = 0x0206 #命令反馈状态信息包
CA_VERIFY_BC_INFO =0x020A #安全命令验证确认信息包
CA_SURE_BC_INFO   =0x020C #安全命令执行确认信息包
CA_VIRTUAL_IO_INFO = 0x020E #虚拟IO状态信息

STATION_DEV_MAX =  19  #站场状态最大个数

ssss = "90090841000109410001 601429d10000008d01f4 000000b10000008d2e00 4D00060202010203040006020401020303 000F0206 01 05FF08410001   00FF 000000010010020A 01 050841000106FF 5501 000000010010020C 01 050841000106FF 550100000001  0006020EFFFFFFFF"

class  ToolsCIATS(BaseTreeWidget):
    def __init__(self):
        super(ToolsCIATS, self).__init__()
        self.setWindowTitle("协议码位解析工具[ CI ATS]")
        self.input_data.setPlainText(ssss)


    def  slot_btn_query_data(self):
        self.treewidget.clear()
        src_list = strtolist(self.input_data.toPlainText())
        if  src_list == None :
            return
        self.parser_ats_data(src_list,len(src_list))
        #self.treewidget.expandAll()


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
                ret = bytes_steam_to_value(rec_data[current_len:], 0,app_head_b2v_table )
                # print("长度0x%04x"%ret['data_len'])
                # print("类型0x%04x"%ret['data_type'])
                #print_list(rec_data[current_len+4:current_len+2+ret['data_len']])
                list_data.append(rec_data[current_len:current_len+2+ret['data_len']])
                rec_len = rec_len - ret['data_len'] - 2
                current_len = current_len + ret['data_len']+2
        ###########解析小包数据###########
        for i  in range(len(list_data)):
            ret = bytes_steam_to_value(list_data[i], 0, app_head_b2v_table)
            # CI TO ATS
            if ret['data_type'] == CA_STATION_INFO: #站场状态信息包
                self.paraser_station_data(list_data[i])
            elif ret['data_type'] == CA_WARNING_INFO:  # 故障报警信息包
                self.paraser_warnning_data(list_data[i])
            elif ret['data_type'] == CA_FEEDBAKC_INFO:  # 命令反馈状态信息包
                self.paraser_cmd_bc_data(list_data[i])
            elif  ret['data_type'] == CA_VERIFY_BC_INFO:  # 安全命令验证确认信息包
                self.paraser_verify_cmd_data(list_data[i])
            elif ret['data_type'] == CA_SURE_BC_INFO:  # 安全命令执行确认信息包
                self.paraser_sure_cmd_data(list_data[i])
            elif ret['data_type'] == CA_VIRTUAL_IO_INFO:  #虚拟IO数据包
                self.paraser_ci_virtual_io_data(list_data[i])
            ##################  ATS TO CI #############
            elif ret['data_type'] == AC_TIME_INFO:  # ATS时钟心跳包
                self.paraser_rec_ats_time(list_data[i])
            elif ret['data_type'] == AC_BTN_CMD_INFO:  # 按钮及控制命令包
                self.paraser_normal_cmd_data(list_data[i])
            elif ret['data_type'] == AC_CMD_VERIFY_INFO:  # 安全命令验证信息包
                self.paraser_ats_verify_cmd_data(list_data[i])
            elif ret['data_type'] == AC_CMD_SURE_INFO:  # 安全命令执行信息包
                self.paraser_ats_sure_cmd_data(list_data[i])
            elif ret['data_type'] == AC_VIRTUAL_IO_INFO:  # 虚拟IO信息包
                self.paraser_ats_virtual_io_data(list_data[i])
            else:
                print("type err ")
                return

    #通用包头
    def  paraser_stream_head(self,src):
        root = QTreeWidgetItem(self.treewidget)
        root.setText(0, "通用包头")
        ret = bytes_steam_to_value( src, 0, stream_head_b2v_table)
        for i in range(len(stream_head)):
            child2 = QTreeWidgetItem(root)
            child2.setText(0, stream_head[i][0])
            child2.setText(1, tohexstr(ret[stream_head_b2v_table[i][0]]))


    #站场状态包
    def  paraser_station_data(self,src):
        roottreewidget = QTreeWidgetItem(self.treewidget)
        roottreewidget.setText(0,"站场状态信息包")
        roottreewidget.setText(1, "0x0202")
        child1 = QTreeWidgetItem(roottreewidget)
        child1.setText(0,"src")
        src = src[4:]
        child1.setText(1, tohexstr(src))
        child_mode = QTreeWidgetItem(roottreewidget)
        child_mode.setText(0,"模式状态")
        child_mode.setText(1, "0x%02x  [0x55:站控 0xAA中控 0xCC:非常站控]"%src[0])
        child_sysA = QTreeWidgetItem(roottreewidget)
        child_sysA.setText(0,"联锁A系工作状态")
        child_sysA.setText(1, "0x%02x "%src[1])
        child_sysB = QTreeWidgetItem(roottreewidget)
        child_sysB.setText(0,"联锁B系工作状态")
        child_sysB.setText(1, "0x%02x "%src[2])
        src = src[4:]
        ##  类型个数
        child_dev_num = QTreeWidgetItem(roottreewidget)
        child_dev_num.setText(0,"设备类型")
        child_dev_num.setText(1, "设备个数")
        num_list = []
        for  i  in  range(STATION_DEV_MAX):
            ret = bytes_steam_to_value(src, 3*i, station_type_num_table)
            child_dev_num_child = QTreeWidgetItem(child_dev_num)
            child_dev_num_child.setText(0,"0x%02x %s "% ( (ret[station_type_num_table[0][D_NAME]]),station_dev_name_table[i]  ))
            child_dev_num_child.setText(1,"0x%02x "%(ret[station_type_num_table[1][D_NAME]]))
            num_list.append(ret[station_type_num_table[1][D_NAME]])
        src = src[3*STATION_DEV_MAX:]
        ### 解析实际数据 ###

        ###  1 信号机 ###
        child_signal = QTreeWidgetItem(roottreewidget)
        child_signal.setText(0, "信号机")
        child_signal.setText(1, "红色 黄色 绿色 白色 红黄色 蓝色 亮灭 灯丝 封锁 ")
        bit_offset = 0
        for i in  range(num_list[0]):
            ### 可加码位顺序表显示(通用性不好)
            sig_ret = bit_steam_to_value(src, bit_offset, station_signal_table )
            child_signal_child = QTreeWidgetItem(child_signal)
            value_str = " "
            for j in range(len(station_signal_table)):
                value_str = value_str+"%d      "%(sig_ret[station_signal_table[j][D_NAME]])
            child_signal_child.setText(0, str(i))
            child_signal_child.setText(1, value_str)
            bit_offset = bit_offset + 9
        ###  2 道岔 ###
        child_switch = QTreeWidgetItem(roottreewidget)
        child_switch.setText(0, "道岔")
        child_switch.setText(1, "定位 左1 左2 右1 右2 四开 故障 单锁 封锁 控制权")
        for i in  range(num_list[1]):
            sw_ret = bit_steam_to_value(src, bit_offset, station_switch_table )
            child_sw_child = QTreeWidgetItem(child_switch)
            value_str = " "
            for j in range(len(station_switch_table)):
                value_str = value_str+"%d      "%(sw_ret[station_switch_table[j][D_NAME]])
            child_sw_child.setText(0, str(i))
            child_sw_child.setText(1, value_str)
            bit_offset = bit_offset + 10

        ###  3 物理区段 ###
        child_track = QTreeWidgetItem(roottreewidget)
        child_track.setText(0, "物理区段")
        child_track.setText(1, "上电锁闭 进路锁闭 防护锁闭 故障锁闭 引导锁闭 占用状态 封锁状态")
        for i in  range(num_list[1]):
            sw_ret = bit_steam_to_value(src, bit_offset, station_track_table )
            child_track_child = QTreeWidgetItem(child_track)
            value_str = " "
            for j in range(len(station_track_table)):
                value_str = value_str+"%d       "%(sw_ret[station_track_table[j][D_NAME]])
            child_track_child.setText(0, str(i))
            child_track_child.setText(1, value_str)
            bit_offset = bit_offset + 7
    #报警信息包
    def  paraser_warnning_data(self,src):
        roottreewidget = QTreeWidgetItem(self.treewidget)
        roottreewidget.setText(0,"报警信息包")
        roottreewidget.setText(1, "0x0204")
        child1 = QTreeWidgetItem(roottreewidget)
        child1.setText(0,"src")
        child1.setText(1, tohexstr(src[4:]))
        ### 解析报警数据  ####
        child2  = QTreeWidgetItem(roottreewidget)
        ret = bytes_steam_to_value(src[4:], 0, ci_version_table)
        child2.setText(0,ci_version_table[0][D_NAME])
        child2.setText(1,"0x%08x"%ret[ci_version_table[0][D_NAME]] )
        src = src[8:]
        ret_len = len(src) #剩余数据长度
        start = 0
        while ret_len> 0:
            ret = bytes_steam_to_value(src[start:], 0, warn_type_num_table )
            start = start + 3
            ret_len = ret_len -3
            child3 = QTreeWidgetItem(roottreewidget)
            child3.setText(0, warn_type_dict[ret[warn_type_num_table[0][D_NAME]]])
            child3.setText(1, "个数: 0x%04x"%ret[warn_type_num_table[1][D_NAME]])
            if  0x01 == ret[warn_type_num_table[0][D_NAME]]:
                child4 = QTreeWidgetItem(roottreewidget)
                child4.setText(1, "0x%02x [0x55：未解锁 0xAA：解锁]"%(src[start]) )
                start = start + 1
                ret_len = ret_len - 1
            elif 0x02 == ret[warn_type_num_table[0][D_NAME]]:
                child5 = QTreeWidgetItem(roottreewidget)
                child5.setText(1, "0x%02x" % (src[start]))
                start = start + 1
                ret_len = ret_len - 1
            else:
                #个数报警
                for  i  in range(ret[warn_type_num_table[1][D_NAME]]):
                    id_value = bytes_steam_to_value(src[start:], 0, id16bit_table )
                    child6 = QTreeWidgetItem(roottreewidget)
                    child6.setText(0,"      ID ")
                    child6.setText(1, "0x%04x" %(id_value[id16bit_table[0][0]]))
                    start = start + 2
                    ret_len = ret_len - 2

    #命令反馈包
    def  paraser_cmd_bc_data(self,src):
        roottreewidget = QTreeWidgetItem(self.treewidget)
        roottreewidget.setText(0,"命令反馈状态信息包")
        roottreewidget.setText(1, "0x0206")
        child1 = QTreeWidgetItem(roottreewidget)
        child1.setText(0,"src")
        child1.setText(1, tohexstr(src[4:]))
        src = src[4:]
        ###########
        child2 = QTreeWidgetItem(roottreewidget)
        child2.setText(0, b2v_dev_num8_table[0][0])
        ret = bytes_steam_to_value(src, 0, b2v_dev_num8_table)
        child2.setText(1, tohexstr(ret[b2v_dev_num8_table[0][0]]))
        src = src[1:]
        #print("个数"+tohexstr(ret[b2v_dev_num8_table[0][0]]))
        for i  in  range(ret[b2v_dev_num8_table[0][0]]):
            temp = src[12*i:]
            ret = bytes_steam_to_value(temp, 0, b2v_ats_cmd_back_table)
            child_cmd = QTreeWidgetItem(roottreewidget)
            child_cmd.setText(0,"命令 "+ str(i))
            for  j  in  range(len(b2v_ats_cmd_back_table)):
                child2 = QTreeWidgetItem(child_cmd)
                child2.setText(0, b2v_ats_cmd_back_table[j][0])
                child2.setText(1, tohexstr(ret[b2v_ats_cmd_back_table[j][0]]))

    #验证命令反馈包
    def  paraser_verify_cmd_data(self,src):
        roottreewidget = QTreeWidgetItem(self.treewidget)
        roottreewidget.setText(0,"安全命令验证确认信息包")
        roottreewidget.setText(1, "0x020A")
        child1 = QTreeWidgetItem(roottreewidget)
        child1.setText(0,"src")
        child1.setText(1, tohexstr(src[4:]))
        src = src[4:]
        ###########
        child2 = QTreeWidgetItem(roottreewidget)
        child2.setText(0, b2v_dev_num8_table[0][0])
        ret = bytes_steam_to_value(src, 0, b2v_dev_num8_table)
        child2.setText(1, tohexstr(ret[b2v_dev_num8_table[0][0]]))
        src = src[1:]
        for i  in  range(ret[b2v_dev_num8_table[0][0]]):
            temp = src[13*i:]
            ret = bytes_steam_to_value(temp, 0, b2v_ats_verify_cmd_bc_table)
            child_cmd = QTreeWidgetItem(roottreewidget)
            child_cmd.setText(0,"验证命令 "+ str(i))
            for  j  in  range(len(b2v_ats_verify_cmd_bc_table)):
                child2 = QTreeWidgetItem(child_cmd)
                child2.setText(0, b2v_ats_verify_cmd_bc_table[j][0])
                child2.setText(1, tohexstr(ret[b2v_ats_verify_cmd_bc_table[j][0]]))

    #执行命令反馈包
    def  paraser_sure_cmd_data(self,src):
        roottreewidget = QTreeWidgetItem(self.treewidget)
        roottreewidget.setText(0,"安全命令执行确认信息包")
        roottreewidget.setText(1, "0x020C")
        child1 = QTreeWidgetItem(roottreewidget)
        child1.setText(0,"src")
        child1.setText(1, tohexstr(src[4:]))
        src = src[4:]
        ###########
        child2 = QTreeWidgetItem(roottreewidget)
        child2.setText(0, b2v_dev_num8_table[0][0])
        ret = bytes_steam_to_value(src, 0, b2v_dev_num8_table)
        child2.setText(1, tohexstr(ret[b2v_dev_num8_table[0][0]]))
        src = src[1:]
        #print("执行命令个数"+tohexstr(ret[b2v_dev_num8_table[0][0]]))
        for i  in  range(ret[b2v_dev_num8_table[0][0]]):
            temp = src[13*i:]
            ret = bytes_steam_to_value(temp, 0, b2v_ats_sure_cmd_bc_table)
            child_cmd = QTreeWidgetItem(roottreewidget)
            child_cmd.setText(0,"执行命令 "+ str(i))
            for  j  in  range(len(b2v_ats_sure_cmd_bc_table)):
                child2 = QTreeWidgetItem(child_cmd)
                child2.setText(0, b2v_ats_sure_cmd_bc_table[j][0])
                child2.setText(1, tohexstr(ret[b2v_ats_sure_cmd_bc_table[j][0]]))

    #虚拟IO信息包
    def  paraser_ci_virtual_io_data(self,src):
        roottreewidget = QTreeWidgetItem(self.treewidget)
        roottreewidget.setText(0,"CI to ATS虚拟IO信息包")
        roottreewidget.setText(1, "0x020E")
        child1 = QTreeWidgetItem(roottreewidget)
        child1.setText(0,"src")
        child1.setText(1, tohexstr(src[4:]))

    #解析心跳包
    def  paraser_rec_ats_time(self,src):
        root = QTreeWidgetItem(self.treewidget)
        root.setText(0, "心跳包")
        ret = bytes_steam_to_value(src[4:], 0, rec_ats_time_table)
        for i in range(len(rec_ats_time_table)):
            child2 = QTreeWidgetItem(root)
            child2.setText(0, rec_ats_time_table[i][0])
            child2.setText(1, tohexstr(ret[rec_ats_time_table[i][0]]))
        self.treewidget.expandAll()
    #普通命令包
    def  paraser_normal_cmd_data(self,src):
        src = src[4:]
        root = QTreeWidgetItem(self.treewidget)
        root.setText(0, "普通命令包")
        ret = bytes_steam_to_value(src, 0, b2v_dev_num8_table)
        #命令个数
        child1 = QTreeWidgetItem(root)
        child1.setText(0, b2v_dev_num8_table[0][0])
        child1.setText(1, tohexstr(ret[b2v_dev_num8_table[0][0]]))
        src = src[1:]
        print("个数"+tohexstr(ret[b2v_dev_num8_table[0][0]]))
        for i  in  range(ret[b2v_dev_num8_table[0][0]]):
            temp = src[11*i:]
            ret = bytes_steam_to_value(temp, 0, b2v_ats_cmd_table)
            child_cmd = QTreeWidgetItem(root)
            child_cmd.setText(0,"命令 "+ str(i))
            for  j  in  range(len(b2v_ats_cmd_table)):
                child2 = QTreeWidgetItem(child_cmd)
                child2.setText(0, b2v_ats_cmd_table[j][0])
                child2.setText(1, tohexstr(ret[b2v_ats_cmd_table[j][0]]))
        #self.treewidget.expandAll()

    def  paraser_ats_verify_cmd_data(self,src):
        src = src[4:]
        root = QTreeWidgetItem(self.treewidget)
        root.setText(0, "安全命令验证信息包")
        ret = bytes_steam_to_value(src, 0, b2v_dev_num8_table)
        #命令个数
        child1 = QTreeWidgetItem(root)
        child1.setText(0, b2v_dev_num8_table[0][0])
        child1.setText(1, tohexstr(ret[b2v_dev_num8_table[0][0]]))
        src = src[1:]
        print("个数"+tohexstr(ret[b2v_dev_num8_table[0][0]]))
        for i  in  range(ret[b2v_dev_num8_table[0][0]]):
            temp = src[11*i:]
            ret = bytes_steam_to_value(temp , 0, b2v_ats_cmd_table)
            child_cmd = QTreeWidgetItem(root)
            child_cmd.setText(0,"命令 "+ str(i))
            for  j  in  range(len(b2v_ats_cmd_table)):
                child2 = QTreeWidgetItem(child_cmd)
                child2.setText(0, b2v_ats_cmd_table[j][0])
                child2.setText(1, tohexstr(ret[b2v_ats_cmd_table[j][0]]))

    def  paraser_ats_sure_cmd_data(self,src):
        src = src[4:]
        root = QTreeWidgetItem(self.treewidget)
        root.setText(0, "安全命令执行信息包")
        ret = bytes_steam_to_value(src, 0, b2v_dev_num8_table)
        #命令个数
        child1 = QTreeWidgetItem(root)
        child1.setText(0, b2v_dev_num8_table[0][0])
        child1.setText(1, tohexstr(ret[b2v_dev_num8_table[0][0]]))
        src = src[1:]
        print("个数"+tohexstr(ret[b2v_dev_num8_table[0][0]]))
        for i  in  range(ret[b2v_dev_num8_table[0][0]]):
            temp = src[11*i:]
            ret = normal_cmd.bytes_to_var(temp)
            ret = bytes_steam_to_value(temp, 0, b2v_ats_cmd_table)
            child_cmd = QTreeWidgetItem(root)
            child_cmd.setText(0,"命令 "+ str(i))
            for  j  in  range(len(b2v_ats_cmd_table)):
                child2 = QTreeWidgetItem(child_cmd)
                child2.setText(0, b2v_ats_cmd_table[j][0])
                child2.setText(1, tohexstr(ret[b2v_ats_cmd_table[j][0]]))

    #ATS虚拟IO信息包
    def  paraser_ats_virtual_io_data(self,src):
        roottreewidget = QTreeWidgetItem(self.treewidget)
        roottreewidget.setText(0,"ATS虚拟IO信息包")
        child1 = QTreeWidgetItem(roottreewidget)
        child1.setText(0,"src")
        child1.setText(1, tohexstr(src[4:]))


if __name__ == "__main__":
    app  = QApplication(sys.argv)
    demo = ToolsCIATS()
    demo.show()
    sys.exit(app.exec_())