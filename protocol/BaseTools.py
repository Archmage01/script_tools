#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2020/3/14 15:36
# @Author  : Lancer


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

def strtolist(src_str):
    '''
    将协议数据流字符串转化为列表
    :param src_str: 原始字符串
    :return:  列表
    '''
    ret = []
    src_str = src_str.strip().replace(' ','')
    if 1 == (len(src_str)%2):
        print("输入错误!")
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



if __name__ == '__main__':
    print(strtolist("   40 ff 55aa"))
    print_list([9,3])
    print_list((8,9))