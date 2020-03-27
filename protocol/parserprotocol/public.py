#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2020/3/26 14:37
# @Author  :

D_NAME  = 0   #名字
D_VALUE = 1   #值
D_WITH  = 1   #宽度字节或者bit

def toStr(num,base):
    '''
        将数字转化为任意进制的字符串
    :param num:   待转化数字
    :param base:  进制
    :return:      转化后字符串
    '''
    convertString = "0123456789ABCDEF"#最大转换为16进制
    if num < base:
        return convertString[num]
    else:
        return toStr(num//base,base)  + convertString[num%base]

def  tohexstr(src_arr):
    if True == isinstance(src_arr, list):
        hex_array = ["0x"]
        for item in src_arr:
            hex_array.append('%02X' % item)
        return "".join(hex_array)
    elif True == isinstance(src_arr, int):
        #补齐2 4 8位
        hex_array = ["0x"]
        if src_arr<= 0xFF:
            hex_array.append('%02X' % src_arr)
        elif  src_arr<= 0xFFFF and src_arr > 0xFF :
            hex_array.append('%04X' % src_arr)
        elif src_arr<= 0xFFFFFFFF and src_arr > 0xFFFF:
            hex_array.append('%08X' % src_arr)
        else:
            hex_array.append('%X' % src_arr)
        return "".join(hex_array)

def strtolist(src_str):
    '''
    将协议数据流字符串转化为列表
    :param src_str: 原始字符串
    :return:  列表
    '''
    ret = []
    src_str = src_str.strip().replace(' ','')
    src_str = src_str.strip().replace('\n','')
    if 1 == (len(src_str)%2):
        print("输入错误!")
        print(len(src_str))
        return
    for i  in range( (len(src_str)+1)//2 ):
        temp = 0
        if 0 == i:
            temp = int( src_str[0:2],16)
        else:
            temp = int(src_str[2*i:2*(i+1)], 16) #[开始索引：结束索引：步长]
        ret.append(temp)
    return ret


def   print_list(src):
    print("length= %d  "%len(src),end="")
    if True == isinstance(src,tuple):
        print("( ", end="")
        for i in range(len(src)):
            print("%02x " % src[i], end="")
        print(" )")
    elif True == isinstance(src,list):
        print("[ ", end="")
        for i in range(len(src)):
            print("%02x " % src[i], end="")
        print(" ]")

def get_bytes( paddr, width, roffset=0):
    data = 0
    src_data = paddr[roffset:]
    for  i  in  range(width):
        data = (data<<8) + ( src_data[i] & 0xFF )
    return  data



def  bytes_steam_to_value(src_list , offset, desc_table ):
    """
        将数据流转为变量值(字节版本)
    :param src_list: 待解析数据流 list
    :param offset  : 起始偏移位置
    :param desc_table: 变量描述表变量
    :return:   解析后的数据 {}
    """
    ret = {}
    base_offset = offset
    for item in desc_table:
        ret[item[0]] =  get_bytes(src_list, item[1], base_offset )
        base_offset = base_offset + item[1]
    return ret


def get_bit( paddr, width, roffset=0):
    """
     @brief 获取指定原始偏移量（bit为单位）处指定宽度的数据
     @param  paddr 源列表
     @param width 数据宽度
     @param roffset 原始偏移量
    """
    index = (roffset // 8)
    offset = (roffset % 8)
    data = 0

    # 根据初始偏移量和总宽度，计算需要拼接的最大字节
    max_offset = (width + offset + 7) // 8

    # 先左移offset偏移量
    for i in range(max_offset):
        data = (data << 8) + ((paddr[index + i] << offset) & 0xffff)
        if (i == 0):
            data = data & 0xff
    # 最后根据总移位的位数，减去width对应应保留的位数，得到需要额外移位的位数
    rest_s = max_offset * 8 - (width + 7 // 8 * 8)
    data = data >> rest_s
    return data

def  bit_steam_to_value(src_list , bit_offset_start, desc_table ):
    """
        将数据流bit转为变量值
    :param src_list: 待解析数据流 list
    :param bit_offset_start:  bit的起始偏移位置
    :param desc_table:        变量描述表变量
    :return:   解析后的数据 {}
    """
    ret = {}
    base_offset =  bit_offset_start
    for item in desc_table:
        ret[item[0]] =  get_bit(src_list, item[D_WITH] ,base_offset)
        base_offset = base_offset + item[D_WITH]
    return  ret


if __name__ == '__main__':
    print(strtolist("   40 ff 55aa"))
    # print_list([9,3])
    # print_list((8,9))
    print(tohexstr(0x1))
    print(tohexstr(0x121))