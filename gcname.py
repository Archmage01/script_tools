#!/usr/bin/env python3 
# -*- coding:gbk -*-
# Author: yang.gan  2019-2-18 12:13:15

import  sys,os,re
import  templatestr 


count_fcase_pattern =  re.compile(r"测试案例编号")



def  get_dir_filename(loacal_dir):
    for root, dirs, files in os.walk( loacal_dir):
        #print(root) #当前目录路径 
        #print(dirs) #当前路径下所有子目录 
        print(files) #当前路径下所有非目录子文件 
    return (files)

#解析每个行
def  line_parser(line ):
    #line = line.strip().strip('\n')
    ret = 0 
    find = re.findall(r"测试案例编号",line)
    if len(find) > 0 :
        ret = ret + len(find)
    return ret




#解析每个.c文件
def  per_file_parser(code):
    ret = 0 
    for  line in code:
        t_count = line_parser(line)
        ret = ret + t_count
    return ret

cpppattern  = re.compile(r'.\.cpp') 

#get  .c  function  name
def  extract_cfile(argv):
    loacal_dir = os.getcwd()
    case_num = 0 
    t_ret = 0 
    filelist = get_dir_filename(loacal_dir)
    if(len(filelist)>0):
        for i in  filelist:
            cpptype = cpppattern.search(i)
            if  cpptype is not None:
                with open(i,encoding='gbk') as f:
                    lines = f.readlines()
                    t_ret = per_file_parser(lines)
                    #print(i + "  num:%d"%t_ret)
                    case_num = case_num + t_ret
            else:
                print("%s is not  .cpp"%i)
        print("extract ==> count case_num: %d"%case_num)
    else:
        print("extract: ==>> loacal dir not exist  .c  file")


func_def_pattern  = re.compile(r'^(\w+\s+)+(\w+)\s*\(\s*(.+)\s*(\)?|(\)\{)?)')
param_dec_pattern = re.compile(r'\(\s*((?:void)|[^!=<>]+\s*)(\)?|(\)\{)?|,?)$')

cfunc_pattern01  = re.compile(r'^(\w+\s+)+\w+\(.+\)')
cfunc_pattern02  = re.compile(r'^(\w+\s+)+\*+\w+\(.+\)')
cfunc_pattern03  = re.compile(r'^(\w+\s+)+\*+\s+\w+\(.+\)')
cdec_pattern   = re.compile(r'\w')

#get  .c  function  definition
def  getcfunction_header(filename):
    cdef = []
    if  len(filename) > 0:
        for i in  range(len(filename)):
            if True == os.path.exists(filename[i]):
                with open(filename[i],encoding='gbk') as f:
                    lines = f.readlines()
                    for  line  in  lines:
                        ff01  = cfunc_pattern01.search(line)
                        ff02  = cfunc_pattern02.search(line)
                        ff03  = cfunc_pattern03.search(line)
                        if ff01 is not None or ff02 is not None or ff03 is not None :
                            if  ff01 is not None:
                                cdef.append(ff01.group())
                            if  ff02 is not None:
                                cdef.append(ff02.group())
                            if  ff03 is not None:
                                cdef.append(ff03.group())
                        pass  
            else:
                print("extract ==> file:%s  not exist  "%filename)
        for i in range(len(cdef)):
            print(cdef[i])