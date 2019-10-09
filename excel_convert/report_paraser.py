#!/usr/bin/env python3.7 
# -*- coding:utf-8 -*-
# Author: Lancer  2019-09-22 11:36:46

import pdfplumber,os,sys,re


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
    print(text)
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


if __name__ == "__main__":
    pass