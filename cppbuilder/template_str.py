#!/usr/bin/env python3.7 
# -*- coding:utf-8 -*-
# Author: Lancer  2019-10-29 17:07:00

import  sys,os,re 

sig_cmake = \
"""
cmake_minimum_required(VERSION 2.8)

SET(mname projectname)

# defining common source variables
AUX_SOURCE_DIRECTORY(src  SRC )

if(SRC)
    ADD_EXECUTABLE( ${mname}  ${SRC} )
endif(SRC)
"""

cppfile_template = \
"""
#include <stdio.h>
#include<stdlib.h>
#include <iostream>


void  main()
{

    printf("hello   world\\n");
	system("pause");
}
"""


