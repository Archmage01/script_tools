#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup

setup( 
    name        = 'CustomUi',  #pip或者easy_install安装时使用的名称
    author      = "Zero",
    version     = '1.0.1',
    description = "A python lib for user to create ui simple",
    py_modules  = ['CustomWidget',"CustomRulesLayout"], #需要打包的python文件列表
    #packages=['RedisRun'], # 需要打包的目录列表

    # 需要安装的依赖
    # install_requires=[
    #     'PyQt5>=5.0.0',
    #     'setuptools>=16.0',
    # ],

    # 添加这个选项，在windows下Python目录的scripts下生成exe文件
    #注意：模块与函数之间是冒号:
    #entry_points={'console_scripts': [
    #'redis_run = RedisRun.redis_run:main',
    #]},

    # 此项需要，否则卸载时报windows error
    zip_safe=False
)