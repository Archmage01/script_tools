#!/usr/bin/env python3.7 
# -*- coding:utf-8 -*-
# Author: Lancer  2019-10-29 16:17:12


import  sys,os,re, getopt,logging
import  core  as  user


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["lint","version"] )
    except getopt.GetoptError as err:
        print(err) # will print something like "option -a not recognized"
        sys.exit(2)    
    #  usr interface 
    logging.basicConfig(level=logging.INFO,format="")
    # print(opts)
    # print(args)
    test = user.usr_core(args, opts )


    # if args[0]  in  cmd_dict:
    #     if  len(args[0] ) > 1 :
    #         command(cmd_dict[args[0]], args[1:] )
    #     else:
    #         command(cmd_dict[args[0]], None )
    # else:
    #     version_function()
    #     usage()


if __name__ == "__main__":
    if  len(sys.argv) >1:
        main()
    else:
        pass

