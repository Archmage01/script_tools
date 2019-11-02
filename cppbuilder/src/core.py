#!/usr/bin/env python3.7 
# -*- coding:utf-8 -*-
# Author: Lancer  2019-10-29 17:07:00

import  sys,os,re,shutil
import  templatefile.cmakefile as cmake
import  templatefile.cppandcfile as cppformat 

def  create_project(projectname):
    rootpath = os.getcwd()
    if not os.listdir(os.getcwd()):
        if 0 == len(projectname):
            print("cmd err: [ create projectname ]")
            return 
        str_template_cmake = {"prjname":projectname[0] }
        with  open('CMakeLists.txt',mode="w",encoding='utf-8') as file:
            file.write(cmake.topcmake%(str_template_cmake)) #创建CMakeList.txt
            file.close()
        os.makedirs('src/main')
        os.makedirs('src/include')
        os.makedirs('src/test_cppunit')
        os.chdir("src")
        with  open('CMakeLists.txt',mode="w",encoding='utf-8') as file:
            file.write(cmake.src_leve_cmake%(str_template_cmake)) #创建CMakeList.txt
            file.close()
        os.chdir(rootpath)
        os.chdir("src/main")
        with  open('%s.cpp'%projectname[0],mode="w",encoding='utf-8') as file:
            file.write(cppformat.cppfile_template) #projectname.cpp
            file.close()
            os.chdir(rootpath)
        os.chdir("src/test_cppunit")
        str_template_ntest = {"prjname":projectname[0] }
        with  open('%s_test.cpp'%projectname[0],mode="w",encoding='utf-8') as file:
            file.write(cppformat.cppunit_testfile%(str_template_ntest) ) #projectname.cpp
            file.close()
        with  open('main_cppunit.cpp',mode="w",encoding='utf-8') as file:
            file.write(cppformat.cppunit_testmain ) #projectname.cpp
            file.close()
        os.chdir(rootpath)
    else:
        print("dir not  empty  please  create in empty dir")



def  init_project( op=None ):
    if False == os.path.exists("lib"):
        os.mkdir("lib")
    if True == os.path.exists("projects"):
        pass
    else:
        os.mkdir("projects")
    os.chdir("projects")
    os.system("cmake  .. && cd ..")

def  build_project(op=None):
    if  False == os.path.exists("target"):
        os.mkdir("target")
    os.system("cmake --build projects    ")

def  cppunit_test(op=None):
    rootpath =  os.getcwd()
    if True == os.path.exists("target"):
        os.chdir("projects/src/Debug")
        print("chdir>> ",os.getcwd() )
        names = os.listdir(os.getcwd())  
        for name in names:
            if name.endswith('.exe') and  name.startswith("cppunit_"): 
                shutil.copy(name, rootpath+"\\target")
                os.chdir(rootpath+"\\target")
                os.system(name)
                break 
    else:
        print("cppunit target not find ")
        return 0 



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
