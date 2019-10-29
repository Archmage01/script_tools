#!/usr/bin/env python3.7 
# -*- coding:utf-8 -*-
# Author: Lancer  2019-10-29 17:07:00

import  sys,os,re
import  template_str


def  create_project(projectname):
    if not os.listdir(os.getcwd()):
        if 0 == len(projectname):
            print("cmd err: [ create projectname ]")
            return 
        # os.mkdir("%s"%projectname[0])
        # os.chdir("%s"%projectname[0])
        with  open('CMakeLists.txt',mode="w",encoding='utf-8') as file:
            file.write(template_str.sig_cmake) #创建CMakeList.txt
            file.close()
        os.mkdir("src")
        os.chdir("src")
        with  open('%s.cpp'%projectname[0],mode="w",encoding='utf-8') as file:
            file.write(template_str.cppfile_template) #projectname.cpp
            file.close()
    else:
        print("目录非空 请在空目录下执行创建工程命令")



def  init_project( op=None ):
    if True == os.path.exists("projects"):
        pass
    else:
        os.mkdir("projects")
    os.chdir("projects")
    os.system("cmake .. && cd ..")

def  build_project(op=None):
        os.system("cmake --build projects")