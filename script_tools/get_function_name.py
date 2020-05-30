#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: Lancer  2020-05-27 14:44:41



import os,re,sys

finction_pattern    = re.compile("\S+\s+\S+\(.*\)")

hash = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_*(), " 


class  FunctionNameGet(object):
    def  __init__(self):
        self.function_list = {}
        self.function_num = 0
        os.chdir("src\\main")
        #print(os.getcwd())
        for root,dirs,files in os.walk(os.getcwd()):
            pass
        print(files)
        for file in  files:
            self.get_function_name(file)
        
        #print(self.function_list )

        for key in self.function_list.keys():
            print("\n文件名:", key)
            for  name in self.function_list[key]:
                print(name)
        print("函数个数: ", self.function_num )

    def  get_function_name(self,file_name):
        self.function_list[file_name] = []
        try:
            file = open(file_name,encoding='gbk')
            lines = file.read()
            file.close()
            function_list = []
            match_obj = finction_pattern.findall(lines)
            sp_list = [""]
            if match_obj:
                for c in match_obj:
                    if c.strip()[0].isalpha() and c.strip().endswith(')') :
                        child_cout = 0
                        for child_c in c:
                            if child_c in hash:
                                child_cout += 1
                        if child_cout == len(c):
                            #print(c)
                            self.function_list[file_name].append(c)
        

        except Exception as e:
            print("open file fail: ", e)
        self.function_num += len(self.function_list[file_name])


if __name__ == "__main__":
    test = FunctionNameGet()
    