#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @brief: util package

import getpass,os,re,psutil
import shutil
from   typing import List

def joindir(*args):
    '''
    拼接目录
    :param args: 目录及其子项
    :return: 拼接后目录
    '''
    args = list(args)
    for i in range(len(args)):
        args[i] = args[i].replace('\\', '/')
    return '/'.join(args)

def isdir_exists(dirpath,makeflag=None):
    '''
    判断目录是否存在
    :param dirpath:  路径
    :param makeflag: 默认不创建
    :return: 目录存在:True 不存在:False
    '''
    dirpath = dirpath.replace('\\','/')
    if os.access(dirpath, os.F_OK):
        return True #目录存在
    else:
        if makeflag:
            os.makedirs(dirpath)
            #print("mkdir success: %s "%(dirpath))
            return True
    return False


def getdirs(dirpath,isdir=True)->List[str]:
    '''
    获得目录下所有文件/目录(当层目录不递归)
    :param dirpath: 路径
    :param isdir:   目录:True 文件:False
    :return: 目录或者文件列表
    '''
    dirpath = dirpath.replace('\\', '/')
    for root, dirs, files in os.walk(dirpath):
        if root == dirpath:
            if True == isdir:
                return  dirs
            else:
                #return  [file for file in files if file.endswith('txt')]
                return files
    return []

'''
def walkFile(file):
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            print(os.path.join(root, f))
        # 遍历所有的文件夹
        for d in dirs:
            print(os.path.join(root, d))
'''




if __name__ == '__main__':
    print(os.getcwd())
    srcdir = joindir(r'D:\code\yanggan\dirtest')
    #print(isdir_exists(srcdir,makeflag=True))
    #s01 = "{0} {1} {0} ".format("hello","world")
    #print(s01)
    temp = '教程是:%(name)s, 价格是:%(price)010.2f, 出版社是:%(publish)s'
    book = {'name': 'Python基础教程', 'price': 99, 'publish': 'C语言中文网'}
    print(temp % book)
    import platform
    print(platform.system(), getpass.getuser())
