#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#	coding:utf-8

# 语法的描述规则如下
# 成员名称, 位宽
#   [
#       ['name1', width]    # 正表示无符号数，负表示有符号数
#       ['name2', width]
#   ]
import copy

I_NAME=0    #
I_WIDTH=1   #
I_ARRAY=2   # 预留后期的数组

MAX_BYTE=4

class b2v:
    """
    # @brief 提供通用的从bit流到类的双向转换
    """
    def __init__(self, dtable=[]):
        """
        # @brief __init__ 初始化函数
        #
        # @param dtable 按照给定的格式提供的属性描述文件，属性名可用空格补齐
        #
        """
        # self._dtable = copy.copy(dtable)
        self._dtable = []
        for elem in dtable:
            self._dtable.append([elem[0].strip(), elem[1]])

    def get_bits(self, paddr, width, roffset=0):
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
        max_offset = (width+offset+7)//8

        # 先左移offset偏移量
        for i in range(max_offset):
            data = (data<<8) + ((paddr[index+i] << offset) & 0xffff)
            if (i==0):
                data = data & 0xff
        # 最后根据总移位的位数，减去width对应应保留的位数，得到需要额外移位的位数
        rest_s = max_offset*8 - (width+7//8*8)
        data = data>>rest_s
        return data

    def make_bits(self, paddr, bit_pos, data, width):
        """
         @brief 将指定宽度的data写入到指定bit偏移量处的数据中
         @param paddr 源列表
         @param roffset 原始偏移量
         @param data 数据
         @param width 数据宽度         
        """
        index = (bit_pos // 8)
        offset = (bit_pos % 8)
        woffset = width%8

        # 若roffset不对齐，第一个字节需要与已有的字节拼
        max_offset = (width+offset+7)//8

        if offset == 0: # 
            raw = 0
        else:
            raw = paddr[index]

        # 8-width%8 表示将数据向左对齐
        data = data << (8 - woffset)%8
        data = data << (8 - offset)%8
        if (8 - woffset)%8 + (8 - offset)%8 >= 8:
            data = data >> 8
        
        extra_data = [0]*max_offset

        for i in range(max_offset): # max_offset最大为4
            extra_data[max_offset-1-i] = (data&0x00ff)
            data = data >> 8

        for i in range(max_offset): # 
            if i==0:
                paddr[index] = raw + extra_data[i]
            else:
                paddr[index+i] = extra_data[i]

        return paddr[index:index+max_offset]


    def stream_to_var(self, buff, descrp=None):
        """从bit流到dict变量
        
        Arguments:
            buff {list or bytes} -- 原始bit流
        
        Keyword Arguments:
            descrp {list} -- 描述表 (default: {None})
        
        Returns:
            dict -- [生成的数据]
        """
        shift = 0
        ret = {}
        dtable = descrp if descrp else self._dtable
        for item in dtable:
            ret[item[I_NAME]] = self.get_bits(buff, item[I_WIDTH], shift)
            shift = shift + item[I_WIDTH]
        return ret

    def var_to_stream(self, dst, jd, descrp=None):
        """从dict变量到bit流
        
        Arguments:
            dst {bytes} -- 目标bytes
            jd {dict} -- 输入变量
        
        Keyword Arguments:
            descrp {list} -- 描述符 (default: {None})
        """
        shift = 0
        dtable = descrp if descrp else self._dtable
        for item in dtable:
            self.make_bits(dst, shift, jd.get(item[I_NAME], 0), item[I_WIDTH])
            shift = shift + item[I_WIDTH] 

class bt2v(b2v):

    def get_bytes(self, paddr, count, offset):
        """
         @brief 从指定地址偏移量处获取指定count的数据（MSB）
         @param paddr 源列表
         @param offset 原始偏移量, 单位字节
         @param count 数据数量，单位字节     
        """
        data = 0
        for i in range(count):
            data = data << 8
            data = data + paddr[offset + i]
        return data
    
    def make_bytes(self, paddr, offset, data, count):
        """
         @brief 从data到字节对象
         @param paddr 源列表
         @param offset 原始偏移量, 单位字节
         @param data 数据
         @param width 数据宽度，单位字节     
        """
        for i in range(count):
            paddr[offset + count-1-i] = (data&0x00ff)
            data = data >> 8
        return paddr

    def bytes_to_var(self, buff, descrp=None):
        """
        # @brief bytes_to_var 从字节流到变量
        #
        # @param buff 字节流
        #
        # @return 
        """
        shift = 0
        ret = {}
        dtable = descrp if descrp else self._dtable
        for item in dtable:
            ret[item[I_NAME]] = self.get_bytes(buff, item[I_WIDTH], shift)
            shift = shift + item[I_WIDTH]
        return ret

    def var_to_bytes(self, dst, jd, descrp=None):
        """
        # @brief var_to_bytes 从变量到字节流
        #
        # @param dst 字节流
        #
        # @return 
        """
        shift = 0
        dtable = descrp if descrp else self._dtable
        for item in dtable:
            self.make_bytes(dst, shift, jd(item[I_NAME]), item[I_WIDTH])
            shift = shift + item[I_WIDTH] 
