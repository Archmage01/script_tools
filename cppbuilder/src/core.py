#!/usr/bin/env python3.7 
# -*- coding:utf-8 -*-
# Author: Lancer  2019-10-29 17:07:00

import  sys,os,re,shutil,logging
import  templatefile.cmakefile as cmake
import  templatefile.cppandcfile as cppformat 


__author__  = "Lancer"
__version__ = " 0.0.1"
__modifytime__ = "2019-10-31"

class usr_core(object):
    def __init__(self, args_list, opts ):
        self.root_path = os.getcwd() 
        self.project_name = ""
        # cmd and header imap 
        self.cmd_dict = {  
            "init"   : self.init_project ,    
            "build"  : self.build_project,    
            "utest"  : self.cppunit_test,    
            "clean"  : self.clean_project, 
        }
        self.args_paraser(args_list, opts)

    def  write_file(self,  file_path, template_str):
        """
        create new  file
        """
        filename = ""
        create_path = ""
        file_path = file_path.split("\\")
        if 1 == len(file_path):
            filename = file_path[0]
        else:
            filename = file_path[-1]
            file_path.pop()
            create_path = "\\".join(file_path)
            if  False ==   os.path.exists(create_path):
                os.makedirs(create_path) 
            os.chdir(create_path)
        with  open(filename,mode="w",encoding='utf-8') as file:
            file.write(template_str) 
            file.close()
            os.chdir(self.root_path)
    
    def  args_paraser(self,args_list, opts):
        if 0 == len(args_list):
            logging.info("cmd err please  input extern cmd data")
        elif 1 == len(args_list):
            if args_list[0]  in self.cmd_dict:
                self.cmd_dict[args_list[0]]()
            pass
        elif  2 == len(args_list):
            if  "create" == args_list[0]:
                self.project_name = args_list[1]
                self.create_project()



    ################################## usr tools public API  #########################################
    def  create_project(self):
        if not os.listdir(os.getcwd()):  
            if 0 == len(self.project_name):
                logging.info("cmd err: no  project name: create projectname")
                return 
            #write CMakeList.txt file
            projectname = {"prjname": self.project_name }
            self.write_file(r"CMakeLists.txt",  cmake.topcmake%(projectname) ) 
            self.write_file(r"src\CMakeLists.txt",  cmake.src_leve_cmake%(projectname) ) 
            #write  cppunit  test file 
            self.write_file(r"src\test_cppunit\%s_test.cpp"%(self.project_name)  ,(cppformat.cppunit_testfile%(projectname)) ) 
            self.write_file(r"src\test_cppunit\main_cppunit.cpp",  cppformat.cppunit_testmain ) 
            #write  cpp/h  src file 
            self.write_file( r"src\main\%s.cpp"%self.project_name,cppformat.cppfile_template ) 
            self.write_file( r"src\include\%s.h"%self.project_name," ") 
        else:
            logging.error("dir not  empty  please  create in empty dir")

    def  init_project(self):
        if False == os.path.exists("lib"):
            os.mkdir("lib")
        if True == os.path.exists("projects"):
            pass
        else:
            os.mkdir("projects")
        os.chdir("projects")
        os.system("cmake  .. && cd ..")

    def  build_project(self):
        if  False == os.path.exists("target"):
            os.mkdir("target")
        else:
            os.chdir("target")
            ls = os.listdir(os.getcwd())
            for i in ls:
                c_path = os.path.join(os.getcwd(), i)
                if os.path.isdir(c_path):
                    pass
                else:
                    os.remove(c_path)
        os.chdir(self.root_path)
        os.system("cmake --build projects    ")
        if True == os.path.exists("target"):
            os.chdir("projects/src/Debug/")
            print("chdir>> ",os.getcwd() )
            names = os.listdir(os.getcwd())  
            for name in names:
               if name.endswith('.lib') or  name.endswith('.exe') or name.endswith('.a'):
                   shutil.copy(name, self.root_path+"\\target")
            
    def  cppunit_test(self):
        if True == os.path.exists("target"):
            os.chdir("projects/src/Debug")
            print("chdir>> ",os.getcwd() )
            names = os.listdir(os.getcwd())  
            for name in names:
               if name.endswith('.exe') and  name.startswith("cppunit_"): 
                   shutil.copy(name, self.root_path+"\\target")
                   os.chdir(self.root_path +"\\target")
                   os.system(name)
                   break 
        else:
            logging.info("cppunit target not find ")
            return 0 



    def  clean_project(self):
        if True == os.path.exists("projects"):
            shutil.rmtree("projects")
        else:
            logging.info("no dir projects already clean  cmakefile")
        pass

if __name__ == "__main__":
    pass
