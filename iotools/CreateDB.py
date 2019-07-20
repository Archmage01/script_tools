#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Author: Lancer
# @File  CreateDB.py
# @Time  2019/7/22 12:09

import  os,sys,re,sqlite3

'''
提取io_table.c代码中IO位数据为io_table.db数据库文件
'''

table_pattern = re.compile(r"\{(.*)\}")  #获取{ } 中间的数据默认为io数据
name_pattern  = re.compile(r"var_item_t\w*\[")  #获取表名  字母数字下划线
del_patterm   = re.compile(r"var_item_t\w*=")  #获取表名  字母数字下划线

class  CreateDB(object):
    def __init__(self):
        self.db_table_list = []  #存储每张表表
        self.io_table_list = [ ] #存储所有表的数据
        self.read_iotable_cfile()
        for  i in range(len(self.io_table_list)):
            pass
            print(self.io_table_list[i])

        self.write_all_table()

    def  read_iotable_cfile(self):
        if True == os.path.exists('io_table.c'):
            with open('io_table.c', encoding='gbk') as f:
                lines = f.readlines()
                convert_lines = ""
                for line in lines:
                    line = re.sub(r"/\*.*\*/","",line )
                    line = re.sub(r'',"",line )
                    convert_lines = convert_lines + line
                convert_lines = convert_lines.replace('\n','').replace('\t','').replace(' ','')
                convert_lines =  re.sub(r"/\*.*\*/","",convert_lines)
                convert_lines = re.sub(r"#.*\"", "", convert_lines)
                #print(convert_lines,type(convert_lines))
                name_test = name_pattern.findall(convert_lines)
                if  name_test is not None:
                    for  i  in  range(len(name_test)):
                        name_test[i]   = re.sub("var_item_t","",name_test[i])
                        name_test[i]   =  re.sub("\[","",name_test[i])
                        #print(name_test[i],type(name_test[i]))
                        self.db_table_list.append(name_test[i])  #获得表名
                else:
                    print("匹配表名失败")

                #  获得每个表的IO数据
                all_table =  convert_lines.split(";")
                for i in  range(len(all_table)):
                    per_table  =  table_pattern.search(all_table[i])
                    if   per_table is not None:
                        per_table = per_table.group()
                        per_table  =   per_table.replace("{","").replace("}","")
                        per_table = per_table.split(",")
                        for i  in range(len(per_table)):
                            per_table[i] = per_table[i].strip()
                            #per_table[i] = per_table[i].replace("(", "#").replace(")", "")
                            #per_table[i] = per_table[i].replace("(", "#").replace(")", "").split("_")[-1]
                        per_table.pop()
                        self.io_table_list.append(per_table)
                        print(per_table)
                    else:
                        print("匹配{ }失败")


        else:
            print("io_table.c 文件不存在")

    def  write_all_table(self):
        # self.db_table_list = []  #存储每张表表
        # self.io_table_list = [ ] #存储所有表的数据
        if  len(self.db_table_list) ==  len(self.io_table_list):
            for  i  in  range(len(self.db_table_list)):
                self.write_per_table(self.db_table_list[i],self.io_table_list[i])
        else:
            print("匹配表个数和表名个数不一致 请检查文件格式 %d  %d"%( len(self.db_table_list),len(self.io_table_list)))


    #写入.db数据
    def write_per_table(self,table_name, table_data_list):
        '''
        将io_table.c文件中数据转化为db文件
        '''
        dataass = [("0","liangsss" ),("1","ssssssssssss")]
        print(dataass[0][0],dataass[0][1])
        con = sqlite3.connect("test_io.db")
        cur = con.cursor()
        try:
            cur.execute('''create table if not exists %s\
                    (inddex       char(5)       NOT NULL,\
                    io_name       char(40)      NOT NULL);'''%(table_name))
            for  i  in  range(len(table_data_list)):
                if 0 != len(table_data_list[i]):
                    cur.execute("insert into %s(inddex,io_name) values(?,?);"%(table_name), (i, table_data_list[i]))
                    con.commit()
            cur.execute("select name from sqlite_master where type='table' order by name")
            print(cur.fetchall()
)
            #cur.execute("insert into driverinfo(inddex,io_name) values(?,?);",(dataass[0][0], dataass[0][1]))
        except sqlite3.Error as e:
            print("An error occurred: %s", e.args[0])

        finally:
            cur.close()
            con.close()

if __name__ == "__main__":
    demo = CreateDB()
    pass