#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: yang.gan  2019-8-23 23:45:27


import  os,sys,re,psutil,copy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

# 白色#FFFFFF  黑色:#000000

black ='''
    QPushButton{background-color:#363636; color:#FFFFFF; border-color:green; border-width:2px; }  
    QMainWindow{background-color:#363636; color:#FFFFFF } 
    QStackedWidget{background-color:#363636; color:#FFFFFF } 
    QLabel{background-color:#363636; color:#FFFFFF } 
    QGroupBox{background-color:#363636; color:#FFFFFF } 
    QFrame{background-color:#363636; color:#FFFFFF } 
    QListWidget{background-color:#363636; color:#FFFFFF } 
    QChartView{background-color:#363636; color:#FFFFFF;border-color:#363636; } 
    QChartView::QHeaderView{background-color:#363636; color:#FFFFFF } 
    QWidget{background-color:#363636; color:#FFFFFF } 
    QComboBox{background-color:#363636; color:#FFFFFF } 
    QLineEdit{background-color:#363636; color:#FFFFFF } 
    QListWidget::Item{padding-top:20px; padding-bottom:4px; }
    QListWidget::Item:hover{background:EEEE00; }
    QListWidget::item:selected{background:#363636; color:red; }
    QListWidget::item:selected:!active{border-width:0px; background:lightgreen;}
    QDialog{background-color:#363636; color:#FFFFFF } 
    QTableWidget{background-color:#363636; color:#FFFFFF } 
    QTableWidget::Item:hover{background:#363636; }
    QTableWidget::item:selected{background:#363636; color:#FFFFFF; }
    QTableWidget::item:selected:!active{ background:lightgreen;}
    QTableWidget::QHeaderView{background-color:#363636; color:#FFFFFF } 
    QHeaderView::section { background-color:#363636 ;color:#FFFFFF }
    QScrollBar{background-color:#363636; color:#FFFFFF;border-radius:4px; }
'''
