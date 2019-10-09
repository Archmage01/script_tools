#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: yang.gan  2019-8-29 09:31:22

import  os,sys,re

# 各种函数定义的格式
cfun_pattern_01 = re.compile("\w+\s+\w+\(.+\)")  # uint8_t  test()
cfun_pattern_02 = re.compile("\w+\s+\w+\s+\(.+\)")  # uint8_t  test ()
cfun_pattern_03 = re.compile("\w+\s+\*+\w+\(.+\)")  # uint8_t **test() uint8_t *test()
cfun_pattern_04 = re.compile("\w+\s+\*+\w+\s+\(.+\)")  # uint8_t ** test() uint8_t * test()
cfun_pattern_05 = re.compile("\w+\*+\s+\w+\(.+\)")  # uint8_t** test() uint8_t* test()
cfun_pattern_06 = re.compile("\w+\*+\s+\w+\s+\(.+\)")  # uint8_t** test ()  uint8_t* test ()

def   get_cfun_pattern_str(line, cfun_pattern ):
    """获得满足一种格式的函数名"""
    function_name = None
    functionstr = cfun_pattern.search(line)#格式1
    if  functionstr is not None and 0 == functionstr.span()[0] :
        #print(functionstr)
        functionstr = functionstr.group()
        #定义中不可能有 比较运算符 == > <  >=  <=  != 
        patter_cmpare_01 = re.compile("==")
        patter_cmpare_02 = re.compile(">")
        patter_cmpare_03 = re.compile("<")
        patter_cmpare_04 = re.compile(">=")
        patter_cmpare_05 = re.compile("<=")
        patter_cmpare_06 = re.compile("!=")
        temp_functionstr_01 = patter_cmpare_01.search(functionstr)
        temp_functionstr_02 = patter_cmpare_02.search(functionstr)
        temp_functionstr_03 = patter_cmpare_03.search(functionstr)
        temp_functionstr_04 = patter_cmpare_04.search(functionstr)
        temp_functionstr_05 = patter_cmpare_05.search(functionstr)
        temp_functionstr_06 = patter_cmpare_06.search(functionstr)
        if  temp_functionstr_01 is None and temp_functionstr_02 is None and temp_functionstr_03 is None and temp_functionstr_04 is None and temp_functionstr_05 is None and temp_functionstr_06 is None  :
            function_name  = functionstr 
    return function_name


def   get_cfun_pattern_01_str(line):
    """获得满足第一种格式的函数名"""
    function_name = get_cfun_pattern_str(line, cfun_pattern_01 )
    return function_name

def   get_cfun_pattern_02_str(line):
    """获得满足第2种格式的函数名"""
    function_name = get_cfun_pattern_str(line, cfun_pattern_02 )
    return function_name

def   get_cfun_pattern_03_str(line):
    """获得满足第3种格式的函数名"""
    function_name = get_cfun_pattern_str(line, cfun_pattern_03 )
    return function_name

def   get_cfun_pattern_04_str(line):
    """获得满足第4种格式的函数名"""
    function_name = get_cfun_pattern_str(line, cfun_pattern_04 )
    return function_name

def   get_cfun_pattern_05_str(line):
    """获得满足第5种格式的函数名"""
    function_name = get_cfun_pattern_str(line, cfun_pattern_05 )
    return function_name

def   get_cfun_pattern_06_str(line):
    """获得满足第6种格式的函数名"""
    function_name = get_cfun_pattern_str(line, cfun_pattern_06 )
    return function_name


def  get_cfile_function_name(filepath):
    function_name_list = [ ]
    function_name = None
    with  open(filepath,encoding='gbk') as file:
        lines = file.readlines()
    for line  in  lines:
        #print(lines)function_name
        line = line.strip()
        # 格式1
        function_name = None
        function_name = get_cfun_pattern_01_str(line)
        if function_name is not None:
            function_name_list.append(function_name)
        else:
            function_name = get_cfun_pattern_02_str(line)  #格式2
            if function_name is not None:
                function_name_list.append(function_name)
            else:
                function_name = get_cfun_pattern_03_str(line)  #格式3
                if function_name is not None:
                    function_name_list.append(function_name)
                else:
                    function_name = get_cfun_pattern_04_str(line)  #格式4
                    if function_name is not None:
                        function_name_list.append(function_name)
                    else:
                        function_name = get_cfun_pattern_05_str(line)  #格式5
                        if function_name is not None:
                            function_name_list.append(function_name)
                        else:
                            function_name = get_cfun_pattern_06_str(line)  #格式6
                            if function_name is not None:
                                function_name_list.append(function_name)

    for  i  in range(len(function_name_list)):
        print(function_name_list[i])
    print(len(function_name_list))
    return function_name_list

if __name__ == "__main__":
    pass
    #get_cfile_function_name("ci2ats_pro.c")