#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Author: Lancer
# @File  pyqtchart.py
# @Time  2019/7/14 20:46

import   sys,re,os
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore  import *
from PyQt5.QtWidgets import  *
from PyQt5.QtChart import *


class  MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        # 获取显示器分辨率大小
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        self.resize(self.width/2,self.height/2)
        self.setWindowTitle("PyQtChart学习")
        #QTabWidget
        self.mainwidget =  QTabWidget(self)
        self.main_layout = QVBoxLayout()
        self.widget_01 = QChartView()
        self.widget_02 = QChartView()
        self.widget_03 = QChartView()
        self.widget_04 = QChartView()
        self.widget_05 = QChartView()
        self.widget_06 = QChartView()
        self.widget_07 = QChartView()
        self.mainwidget.addTab(self.widget_01, "Scatter散点图")
        self.mainwidget.addTab(self.widget_02, "Bar柱状图")
        self.mainwidget.addTab(self.widget_03, "Contours等高线图")
        self.mainwidget.addTab(self.widget_04, "3D 数据")
        self.mainwidget.addTab(self.widget_05, "折线图")
        self.mainwidget.addTab(self.widget_06, "饼状图")
        self.mainwidget.addTab(self.widget_07, "hlines和vlines图例")
        self.main_layout.addWidget(self.mainwidget)
        self.setLayout(self.main_layout)
        #绘图
        self.widget_01_ui()
        self.widget_02_ui()
        self.widget_05_ui()
        self.widget_06_ui()
    #Bar柱状图
    def widget_02_ui(self):
        series = QBarSeries()
        set0 = QBarSet("Jane")
        set1 = QBarSet("John")
        set2 = QBarSet("Axel")
        set3 = QBarSet("Mary")
        set4 = QBarSet("Samantha")
        set0.append([1,2 ,3 ,4 ,5 ,6])
        set1.append([5, 0, 0, 4, 0, 7])
        set2.append([3, 5, 8, 12, 8, 5])
        set3.append([5, 6, 7, 3, 4, 5])
        set4.append([9, 7, 5, 3, 1, 2])
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
        series.append(set4)
        chart = QChart()
        chart.createDefaultAxes()
        chart.addSeries(series)
        chart.setTitle("Simple barchart example")
        x_list = [ "Jan","Feb","Mar","Apr","May","Jun" ]
        axis = QBarCategoryAxis()
        axis.append(x_list)
        y_Aix = QValueAxis()  # 定义y轴
        y_Aix.setRange(0.00, 15.00)
        chart.setAxisY(y_Aix)
        chart.setAxisX(axis, series)
        chart.legend().setVisible(True)
        self.widget_02.setChart(chart)

    def  widget_05_ui(self):
        series = QLineSeries()  # 定义LineSerise，将类QLineSeries实例化
        series_01 = QLineSeries()  # 创建曲线

        point_0 = QPointF(0.00, 0.00)  # 定义折线坐标点
        point_1 = QPointF(0.80, 6.00)
        point_2 = QPointF(2.00, 2.00)
        point_3 = QPointF(4.00, 3.00)
        point_4 = QPointF(1.00, 3.00)
        point_5 = QPointF(5.00, 3.00)

        s_point_0 = QPointF(0.00, 1.00)  # 定义折线坐标点
        s_point_1 = QPointF(0.80, 5.00)
        s_point_2 = QPointF(2.00, 3.00)
        s_point_3 = QPointF(4.00, 6.00)
        s_point_4 = QPointF(1.00, 2.00)
        s_point_5 = QPointF(5.00, 4.00)

        point_list = [point_0, point_1, point_4, point_2, point_3, point_5]  # 定义折线点清单
        point_list_01 = [s_point_0, s_point_1, s_point_4, s_point_2, s_point_3, s_point_5]  # 定义折线点清单

        series.append(point_list)  # 折线添加坐标点
        series.setName("折线一")  # 折线命名

        series_01.append(point_list_01)  # 折线添加坐标点
        series_01.setName("折线二")  # 折线命名

        x_Aix = QValueAxis()  # 定义x轴，实例化
        x_Aix.setRange(0.00, 8.00)  # 设置量程
        x_Aix.setLabelFormat("%0.2f")  # 设置坐标轴坐标显示方式，精确到小数点后两位
        x_Aix.setTickCount(8)  # 设置x轴有几个量程
        x_Aix.setMinorTickCount(0)  # 设置每个单元格有几个小的分级

        y_Aix = QValueAxis()  # 定义y轴
        y_Aix.setRange(0.00, 9.00)
        y_Aix.setLabelFormat("%0.2f")
        y_Aix.setTickCount(9)
        y_Aix.setMinorTickCount(0)
        self.widget_05.chart().addSeries(series)  # 添加折线
        self.widget_05.chart().addSeries(series_01)  # 添加折线
        self.widget_05.chart().setAxisX(x_Aix)  # 设置x轴属性
        self.widget_05.chart().setAxisY(y_Aix)  # 设置y轴属性
        self.widget_05.chart().createDefaultAxes()  # 使用默认坐标系
        # charView.chart().setTitleBrush(QBrush(Qt.cyan))  # 设置标题笔刷
        self.widget_05.chart().setTitle("折线图标题")  # 设置标题
        #self.widget_05.show()  # 显示charView
        """
        1.QChartView : 是一个可以显示图表（chart）的独立部件。
        2.QChart : 用于创建图表。
        3.series : 被词典翻译为 串联;级数;系列，连续; 这里我理解为存储的一系列坐标；
        4.QValueAxis : 继承自QAbstractAxis,用于对坐标轴进行操作。
        流程: 坐标附加到series然后使用addSeries方法把series载入ChartView。
        """

    def widget_06_ui(self):
        series = QPieSeries()
        series.append("python",3)
        series.append("C++",3)
        series.append("C",1)
        series.append("java",1)
        series.append("javascript",2)
        slice =  QPieSlice()
        slice = series.slices()[0]  # 得到饼图的某一个元素切片，在这取得为第一个
        slice.setExploded()  # 设置为exploded
        slice.setLabelVisible()  # 设置Lable
        slice.setPen(QtGui.QPen(Qt.darkGreen, 1))  # 设置画笔类型
        slice.setBrush(Qt.green)  # 设置笔刷
        slice.setLabelVisible(True)
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Simple piechart example")
        self.widget_06.setChart(chart)

    def widget_01_ui(self):
        series0 = QScatterSeries()
        series0.append(1, 2)
        series0.append(2, 4)
        series0.append(3, 8)
        series0.append(7, 4)
        series0.append(10, 5)
        series0.setName("散点图")
        chart = QChart()
        chart.addSeries(series0)
        chart.setTitle("Simple scatterchart example")
        chart.createDefaultAxes()
        y_Aix = QValueAxis()  # 定义y轴
        y_Aix.setRange(0.00, 15.00)
        chart.setAxisY(y_Aix)
        x_Aix = QValueAxis()  # 定义y轴
        x_Aix.setRange(0.00, 10.00)
        chart.setAxisX(x_Aix)
        #chart.setAxisX(axis, series)
        self.widget_01.setChart(chart)
        pass



if __name__  == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mywidget = MyWidget()
    mywidget.show()
    app.exec()