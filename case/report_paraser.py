#!/usr/bin/env python3.7 
# -*- coding:utf-8 -*-
# Author: Lancer  2019-09-22 11:36:46

import pdfplumber,os,sys,re


linepattern  = re.compile(r'LC+.+\(')
cfilepattern = re.compile(r'\w+.\.c')
functionpattern = re.compile(r'\w+.\s')
notDumppattern  = re.compile(r'\w+.\S')
excel_data = []


def  paraser_report_pdf( path ):
    with pdfplumber.open(path) as pdf:
        pdf_page_num =  len(pdf.pages)
        print("报告页数: %d"%pdf_page_num )
        text = ""
        for i in  range(pdf_page_num):
            text_temp = pdf.pages[i].extract_text()
            text = text +  text_temp 
    return text 

def  get_rate_percent(text):
    text = text.replace(r"C++test 报告.*Page"," ")   #换页多余信息删除掉
    rate_pattern_01 =  re.compile(r'覆盖率概要')
    rate_pattern_02 =  re.compile(r'LC - 行覆盖率')
    rate_str_start = rate_pattern_01.search(text)
    rate_str_end = rate_pattern_02.search(text)
    start = rate_str_start.span()[1]
    end =  rate_str_end.span()[0]
    text = text[start:end]
    #step 2 
    rate_pattern_01 =  re.compile(r'\w+.\.c')
    rate_str_start = rate_pattern_01.search(text)
    start = rate_str_start.span()[1]
    text = rate_str_start.group() + text[start:]
    rate_pattern_02 =  re.compile(r'图例:')
    rate_str_end = rate_pattern_02.search(text)
    end =  rate_str_end.span()[0]
    text= text[:end].strip()
    #print(text)
    text =  remove_page_numbers(text)
    return text

#删除多页时多余页脚 奇数页偶数页格式不一样-.-
def  remove_page_numbers(text):
    text = text.replace("\xa0"," ")
    ret_pattern =  re.compile('C\+\+test+.+Page+\s+\d+\s')  
    page_str = ret_pattern.search(text)
    while  page_str is not None:
        start =  page_str.span()[0]
        end =   page_str.span()[1]
        text = text[0:start] + text[end:]
        page_str = ret_pattern.search(text)
    end_pattern =  re.compile('Page+\s+\d+\s+C\+\+test+\s+报告+\s+\[.*\]')
    page_str = end_pattern.search(text)
    while  page_str is not None:
        start =  page_str.span()[0]
        end =   page_str.span()[1]
        text = text[0:start] + text[end:]
        page_str = end_pattern.search(text)
    return  text

def  paraser_and_fill_dt(lines ):
    """将PDF数据(列表)提取填充为excel所需格式 """
    tfilename = ""
    excel_data.clear()
    for i  in range(len(lines)):
        per_line = []
        cfile_name = cfilepattern.search(lines[i])
        if cfile_name is not None:
            tfilename = cfile_name.group()
        else:
            per_line.append(tfilename)  #.c名
            functionname =  functionpattern.search(lines[i]) 
            per_line.append(functionname.group().strip()) #函数名
            #  LC SC  BC FC PC DC  SCC MCDC
            line =  lines[i].split("[")[-1]
            line = line.split("(%")[0].strip()
            line = line.split(" ")
            per_line.append(line[0].split("=")[-1])  #LC
            per_line.append(line[1].split("=")[-1])  #SC
            per_line.append(line[2].split("=")[-1])  #BC
            per_line.append(line[3].split("=")[-1])  #FC
            per_line.append(line[4].split("=")[-1])  #PC
            per_line.append(line[5].split("=")[-1])  #DC
            per_line.append(line[6].split("=")[-1])  #SCC
            per_line.append(line[7].split("=")[-1])  #MCDC
            per_line.append(get_test_case_num(per_line[1] )) #测试案例个数
        if 0 != len(per_line):
            excel_data.append(per_line)

    # for i  in range(len(excel_data)):
    #     print(excel_data[i])


def  count_test_case_num( cppfilename):
    case_num = 0 
    with open(cppfilename,encoding='gbk') as f:
        lines = f.readlines()
        for  line in lines:
            find = re.findall(r"测试案例编号",line)
            if len(find) > 0 :
                case_num = case_num + len(find)
    return  (case_num)

def  is_file_in_dir(function_name, dir , rootdir ):
    """判断文件是否存在 存在计算其测试案例个数"""
    if (os.getcwd() != dir):
        os.chdir(dir)
    else:
        pass
    cppfilename = "test_"+function_name+".cpp"
    case_num = 0 
    if True == os.path.exists(cppfilename):
        case_num = count_test_case_num(cppfilename)
    else:
        cppfilename = function_name+".cpp"
        if True == os.path.exists(cppfilename):
            case_num = count_test_case_num(cppfilename)
        else:
            cppfilename = function_name+"_test"+".cpp"
            if True == os.path.exists(cppfilename):
                case_num = count_test_case_num(cppfilename)
            else:
                case_num = -1 
    os.chdir(rootdir)
    return case_num
    


def  get_test_case_num( function_name ):
    """通过函数名获得测试案例个数
        支持格式 1: test_function_name.cpp 2: function_name.cpp 3: function_name_test.cpp 
        目录只支持查找本层目录及其下一层目录
    """
    #获得目录及文件
    rootdirs = []
    rootfiles = []
    case_num = 0 
    rootdir  = os.getcwd()
    mixfile =  os.listdir(os.getcwd())
    for i in  range(len(mixfile)):
        if os.path.isdir(os.getcwd()+"\\"+mixfile[i]):
            rootdirs.append(mixfile[i])
        elif os.path.isfile(os.getcwd()+"\\"+mixfile[i]):
            rootfiles.append(mixfile[i])
        else:
            pass
            print( os.getcwd() + "\\"+ mixfile[i])

    # 判断测试文件是否在根目录下
    case_num =  is_file_in_dir(function_name, os.getcwd(), rootdir )
    if (-1 != case_num) :
        return case_num
    else:
        for i in  range(len(rootdirs)):
            case_num =  is_file_in_dir(function_name, rootdir+"\\"+rootdirs[i], rootdir )
            if (-1 != case_num) :
                return  case_num
    if (-1 == case_num):
        print("%s 未找到测试文件"%function_name)
        return  -1

if __name__ == "__main__":
    lines = paraser_report_pdf("report.pdf")  
    lines = get_rate_percent(lines)
    #print(lines)
    lines = lines.split("\n")
    #print(lines)
    paraser_and_fill_dt(lines )