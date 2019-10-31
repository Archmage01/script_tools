#!/usr/bin/env python3.7 
# -*- coding:utf-8 -*-
# Author: Lancer  2019-10-29 17:07:00

import  sys,os,re,shutil
import  template_str

def  create_project(projectname):
    rootpath = os.getcwd()
    if not os.listdir(os.getcwd()):
        if 0 == len(projectname):
            print("cmd err: [ create projectname ]")
            return 
        # os.mkdir("%s"%projectname[0])
        # os.chdir("%s"%projectname[0])
        os.mkdir("lib")
        str_template_cmake = {"prjname":projectname[0] }
        with  open('CMakeLists.txt',mode="w",encoding='utf-8') as file:
            file.write(template_str.sig_cmake%(str_template_cmake)) #创建CMakeList.txt
            file.close()
        os.mkdir("src")
        os.chdir("src")
        with  open('%s.cpp'%projectname[0],mode="w",encoding='utf-8') as file:
            file.write(template_str.cppfile_template) #projectname.cpp
            file.close()
        os.chdir(rootpath)
        os.mkdir("test")
        os.chdir("test")
        str_template_ntest = {"prjname":projectname[0] }
        with  open('%s_test.cpp'%projectname[0],mode="w",encoding='utf-8') as file:
            file.write(template_str.cppunit_testfile%(str_template_ntest) ) #projectname.cpp
            file.close()
    else:
        print("目录非空 请在空目录下执行创建工程命令")



def  init_project( op=None ):
    if True == os.path.exists("projects"):
        pass
    else:
        os.mkdir("projects")
    os.chdir("projects")
    os.system("cmake  .. && cd ..")

def  build_project(op=None):
        os.system("cmake --build projects    ")

def  cppunit_test(op=None):
    rootpath =  os.getcwd()
    os.chdir("projects/Debug")
    print("chdir>> ",os.getcwd() )
    names = os.listdir(os.getcwd())  
    for name in names:
        if name.endswith('.exe') and  name.startswith("cppunit_"): 
            os.system(name)
            break 

def  clean_project(op=None):
    if True == os.path.exists("projects"):
        shutil.rmtree("projects")
    else:
        print("no dir projects already clean  cmakefile")
    pass

if __name__ == "__main__":
    pass
    # str_template = {"projectname":"hello world"}
    # print(template_str.sig_cmake%(str_template))
