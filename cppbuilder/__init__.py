#!/usr/bin/env python3.7 
# -*- coding:utf-8 -*-
# Author: Lancer  2019-10-29 16:17:12


########################    Version0.0.1   自动创建CPP模块文件  #########################
#  假如模块名为: projectname  
#  目录结构:     projectname 
#                  src(该目录放源文件)
#                  Cmakelist.txt (cmake文件)
# 命令介绍:  cppbuilder init:   调用cmake工具 创建vs工程文件(工程目录下创建projects目录 生成项目文件在该目录下)
#           cppbuilder build:  编译工程
#  本工具默认刷题使用 所以不会 生成头文件(只会单独生成.cpp 含main函数)
#  加可选项:  生成标准工程  源文件头文件 分目录存储 

########################    Version0.0.2   支持增加单元测试文件  #########################