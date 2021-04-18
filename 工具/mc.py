#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @brief: 自用命令行工具

import getpass,os,re,sys

cmd =  [
    #自定义命令替换模板
['pip','install','-i https://pypi.tuna.tsinghua.edu.cn/simple' ],
['pip','install','-i http://mirrors.aliyun.com/pypi/simple/' ],
['pip','install','-i https://pypi.mirrors.ustc.edu.cn/simple/' ],
]



class CmdFormat(object):
    def __init__(self,cmdlists=None):
        self.cmdinfo ={}
        if cmdlists:
            for cmdlist in cmdlists:
                cmd,param,exstr = cmdlist[0], cmdlist[1],cmdlist[2]
                self.add_cmd_info(cmd,param,exstr)
        self.get_cmd_info()

    def get_cmd_info(self):
        return self.cmdinfo

    def add_cmd_info(self,cmd,  param=None, *exstr):
        if cmd in self.cmdinfo.keys():
            #非空
            if param:
                if param in  self.cmdinfo[cmd].keys():
                    self.cmdinfo[cmd][param].append(' '.join(exstr))
                else:
                    self.cmdinfo[cmd][param] = [' '.join(exstr)]
        else:
            #添加
            self.cmdinfo[cmd] = {}
            if  param:
                if param in self.cmdinfo[cmd].keys():
                    self.cmdinfo[cmd][param].append(' '.join(exstr))
                else:
                    self.cmdinfo[cmd][param] = [' '.join(exstr)]


    def execute_cmd(self, cmd,  param, *exstr):
        if cmd in self.cmdinfo.keys() and param in self.cmdinfo[cmd].keys():
            try:
                tail = ' '.join(exstr)
                # 遍历并列命令
                for ext in self.cmdinfo[cmd][param]:
                    wholecmd = cmd+' '+ param+' ' +  ext + ' '+tail
                    print("===== execute cmd =====: ", wholecmd)
                    ret = os.system(wholecmd)
                    print(" ")
                    if 0 == ret:
                        break
            except Exception as e:
                print(e)
        else:
            print("%s %s not add in tools cmd format"%(cmd,param))

    def print_cmdinfo(self):
        print("")
        for key,dvalues in self.cmdinfo.items():
            print(key," : ")
            for childkey in dvalues.keys():
                print("  ",childkey," : ")
                for v in dvalues[childkey]:
                    print("      ",v)
        print("\nSupport format cmdinfo")


if __name__ == '__main__':
    test = CmdFormat(cmd)
    argv = sys.argv[1::]
    if argv[0] in test.cmdinfo.keys():
        #添加额外操作
        if len(argv)>2:
            test.execute_cmd(argv[0],argv[1],' '.join(argv[2::]))
    else: #保持原状
        cmd = ' '.join(argv)
        if argv[0] in ('-h','--help'):
            test.print_cmdinfo()
        else:
            try:
                print("=========== " + cmd + "  ===========")
                os.system(cmd)
            except Exception as e:
                pass
