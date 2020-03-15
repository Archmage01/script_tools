#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2020/3/12 15:44
# @Author  : Lancer


#
from  b2v import * ;

stream_head =[
    [ '接口信息类型',2, 0xFFFF ],
    [ '发送方标识ID',4, 0xFFFFFFFF ],
    [ '接收方标识ID',4, 0xFFFFFFFF ],
    [ '电子地图CRC',4, 0xFFFFFFFF ],
    [ '本周期序列号',4, 0xFFFFFFFF ],
    [ '设备通讯周期',2, 0xFFFF ],
    [ '回复对方序列号',4, 0xFFFFFFFF ],
    [ '回复本方序列号',4, 0xFFFFFFFF ],
    [ '协议版本号',1, 0x00 ],
    [ '数据包总长度',2, 0xFFFF ],
]

stream_head_b2v_table = [
    [ '接口信息类型',2  ],
    [ 'sender_id',4  ],
    [ 'receiver_id',4  ],
    [ 'map_version_crc32',4   ],
    [ 'send_num',4, ],
    [ 'com_period',2  ],
    [ 'opposite_num',4 ],
    [ 'rcv_num',4 ],
    [ 'protocol_version',1 ],
    [ 'package_len',2 ],
]

app_head_b2v_table = [
    [ 'data_len',2  ],
    [ 'data_type',2  ],
]

b2v_dev_num8_table = [
    ["个数", 1]
]

b2v_dev_num16_table = [
    ["个数", 16]
]

####################  b2v table  CI ATS #########################

#心跳包
rec_ats_time_table = [
    ["年",1],
    ["月",1],
    ["日",1],
    ["时",1],
    ["分",1],
    ["秒",1],
]

b2v_ats_cmd_table = [
    ["命令类型",1],
    ["命令设备ID",4],
    ["设备类型",1],
    ["其他",1],
    ["客户端编号",4],
]


#################### end b2v table  CI ATS #########################
