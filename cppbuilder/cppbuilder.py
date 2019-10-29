#!/usr/bin/env python3.7 
# -*- coding:utf-8 -*-
# Author: Lancer  2019-10-29 16:17:12


import  sys,os,re, getopt
import  core  as  user

__author__  = "yang.gan"
__version__ = "version: 0.0.1"


def version_function():
    print("    author:%s  version:%s"%(__author__, __version__))


cmd_dict = {
    "create" : user.create_project,   #创建工程 固定目录结构  cmake  源文件(.cpp)
    "init"   : user.init_project ,    #初始化工程 
    "build"  : user.build_project,    #
}



def command(function_header,str):
    function_header(str)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ha", ["help", "output="] )
    except getopt.GetoptError as err:
        print(err) # will print something like "option -a not recognized"
        sys.exit(2)    
    if args[0]  in  cmd_dict:
        if  len(args[0] ) > 1 :
            command(cmd_dict[args[0]], args[1:] )
        else:
            command(cmd_dict[args[0]], None )
    else:
        version_function()
        usage()


def usage():   
    usagestr = \
    """    --------------------------------  工具命令介绍  --------------------------------
    [cppbuilder create  projectname ] : 创建工程 固定目录结构  cmake  
    [cppbuilder init                ] : 初始化项目 拉取vs项目文件 
    [cppbuilder build               ] : 编译项目
    --------------------------------------------------------------------------------
    """   
    print(usagestr)

if __name__ == "__main__":
    if  len(sys.argv) >1:
        main()
    else:
        usage()

