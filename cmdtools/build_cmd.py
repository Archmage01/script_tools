#!/usr/bin/env python3 
# -*- coding: gbk -*-
# Author: yang.gan  2019-3-4 08:49:53


import  sys,os,re, getopt

def  ibi_header(dump):
    os.system("smb init && smb build && smb install")

def  ib_header(dump):
    os.system("smb init && smb build ")

def  bt_header(dump):
    os.system("smb build && smb utest")

def  ixl_header(dump):
    os.system("smb init && smb xbinfo armcc  && smb lmake")