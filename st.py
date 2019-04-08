#!/usr/bin/env python3 
# -*- coding:gbk -*-
# Author: yang.gan  2019-2-16 23:37:58

import  sys,os,re, getopt
import  templatestr, gcname, countTestcase
import  build_cmd

''' 

''' 

__Author__  = "yang.gan"
__Version__ = "version: 0.0.4 "


def version_function():
    print("author:%s  version:%s"%(__Author__, __Version__))


cmd_dict = {
    "extract":gcname.extract_cfile,    #
    "count":countTestcase.countTestcasenum,
    "create":  templatestr.create_test_file,
    "ibi": build_cmd.ibi_header, 
    "ib":  build_cmd.ib_header, 
    "bt":  build_cmd.bt_header, 
    "ixl": build_cmd.ixl_header, 
    "getcfunction":gcname.getcfunction_header,
}



def command(function_header,str):
    function_header(str)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ha", ["help", "output="] )
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        sys.exit(2)
    #print(opts)
    #print(args)
    if args[0]  in  cmd_dict:
        command(cmd_dict[args[0]], args[1:] )
    else:
        version_function()
        usage()


def usage():   
    usagestr = "\
    \n[ st  create cppname     ]   create  cpptest  file\
    \n[ st  -h   --help        ]   print   script   helpdata\
    \n[ st  extract            ]   get test case num in locoal dir\
    \n[ st  count              ]   get test case num  and  create  excel table  \
    \n[ st  getcfunction       ]   get .c  function  def   \
    "
    print(usagestr)

if __name__ == "__main__":
    if  len(sys.argv) >1:
        main()
    else:
        usage()

