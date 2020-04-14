#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2020/4/14 11:24
# @Author  : Lancer

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *


style_format_01 = '''

QPushButton{
    background-color:lightgray;
}
QPushButton:hover{
    border: 2px solid red;
}
QPushButton:pressed{
    border: 2px solid green;
    background-color:red;
}


.QFrame{
    background-color:lightgray;   
    border: 2px solid green;
}

.QWidget{
    background-color:lightgray;   
}

.QTextEdit{
    background-color:lightgray;   
}

'''
