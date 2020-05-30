#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2020/3/23 9:25
# @Author  : Lancer

import os
import py_compile
import shutil
import sys

DIST = 'dist'

def pyc_uncompile():
    '''
    @brief 反编译.pyc文件为 .py文件
    '''
    for dirpath, dirnames, filenames in os.walk(DIST):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.pyc':
                pyc_file = os.path.join(dirpath, filename)
                py_file = pyc_file.strip().split('.')[0]+'.py'
                os.system("uncompyle6 %s >%s"%(pyc_file,py_file))
                print('uncompile', pyc_file, 'to', py_file)

def remove_pyc():
    for dirpath, dirnames, filenames in os.walk(DIST):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.pyc':
                src = os.path.join(dirpath, filename)
                os.remove(src)
                print('remove compile:', filename)

    pass

if __name__ == "__main__":
    pyc_uncompile()
    remove_pyc()
