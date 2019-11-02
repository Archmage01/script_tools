#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os,re,shutil 

def  packtools():
    rootpath = os.getcwd()
    if True == os.path.exists("src"):
        os.chdir("src")
        if True == os.path.exists("cppts.py"):
            os.system("pyinstaller -F cppts.py")
            try:
                shutil.copy("dist/cppts.exe", rootpath)
            except IOError as e:
                print("Unable to copy file. %s" % e)
            except:
                print("Unexpected error:", sys.exc_info())
    #clean  temp build file
    print(os.getcwd())
    if  True ==   os.path.exists("cppts.spec"):
        os.remove("cppts.spec")  
    if  True ==   os.path.exists("dist"):
        shutil.rmtree("dist")
    if  True ==   os.path.exists("build"):
        shutil.rmtree("build")
    os.chdir(rootpath)
    python_script_path = sys.executable
    python_script_path = python_script_path.split("\\")
    python_script_path.pop()
    python_script_path = "\\".join(python_script_path)
    python_script_path = python_script_path + "\\Scripts"
    try:
        shutil.copy("cppts.exe", python_script_path)
    except IOError as e:
        print("Unable to copy file. %s" % e)
    except:
        print("Unexpected error:", sys.exc_info())
    #copy  exe  to  python/script  C:\python\python.exe



if __name__ =="__main__":
    packtools()
    # python_script_path = sys.executable
    # python_script_path = python_script_path.split("\\")
    # python_script_path.pop()
    # python_script_path = "\\".join(python_script_path)
    # python_script_path = python_script_path + "\\Scripts"
    # print(python_script_path)
    #print(ss)
    pass

