#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os,re,shutil 

def  packtools():
    rootpath = os.getcwd()
    if True == os.path.exists("src"):
        os.chdir("src")
        if True == os.path.exists("cppbuilder.py"):
            os.system("pyinstaller -F cppbuilder.py")
            try:
                shutil.copy("dist/cppbuilder.exe", rootpath)
            except IOError as e:
                print("Unable to copy file. %s" % e)
            except:
                print("Unexpected error:", sys.exc_info())
    #clean  temp build file
    print(os.getcwd())
    if  True ==   os.path.exists("cppbuilder.spec"):
        os.remove("cppbuilder.spec")  
    if  True ==   os.path.exists("dist"):
        shutil.rmtree("dist")
    if  True ==   os.path.exists("build"):
        shutil.rmtree("build")

packtools()

