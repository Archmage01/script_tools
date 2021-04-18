#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @brief: 国内镜像安装python库
import getpass,os,re,sys


src_urls = [
    "https://pypi.tuna.tsinghua.edu.cn/simple", #清华
    "http://mirrors.aliyun.com/pypi/simple/"  , #阿里云
    'https://pypi.mirrors.ustc.edu.cn/simple/', #中国科技大学
    'http://pypi.hustunique.com/',              #华中理工大学
    'http://pypi.douban.com/simple/'            #豆瓣
]

if __name__ == '__main__':
    argv = sys.argv[1:len(sys.argv):]
    #print(argv)
    for url in src_urls:
        if len(argv)>=2 and argv[0] == 'install' :
            #print(argv[1])
            print("\n===== 国内镜像下载: %s "%(url))
            ret = os.system("pip install -i %s %s" % (url,argv[1]))
            if ret==0:
                break
