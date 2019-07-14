#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Author: Lancer
# @File  qt_matplotlib.py
# @Time  2019/7/14 12:33

# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import  *
from  matplotlib  import  pyplot  as  plt
from  mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import numpy as np
import   sys,re,os


class  MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        # 获取显示器分辨率大小
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        self.resize(self.width/2,self.height/2)
        self.setWindowTitle("Matplotlib学习")
        #QTabWidget
        self.mainwidget =  QTabWidget(self)
        self.main_layout = QVBoxLayout()
        self.widget_01 = QWidget()
        self.widget_02 = QWidget()
        self.widget_03 = QWidget()
        self.widget_04 = QWidget()
        self.widget_05 = QWidget()
        self.widget_06 = QWidget()
        self.widget_07 = QWidget()
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
        self.paint_widget_01()
        self.paint_widget_02()
        self.paint_widget_04()
        self.paint_widget_05()
        self.paint_widget_06()
        self.paint_widget_07()

    #Scatter散点图
    def paint_widget_01(self):
        figure = plt.figure()
        canvas = FigureCanvas(figure)
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        self.widget_01.setLayout(layout)
        #绘图
        x_values = [1, 2, 3, 4, 5]
        y_values = [1, 4, 9, 16, 25]
        plt.scatter(x_values, y_values, s=100)  # 指定线条宽度

        # 设置图表标题， 并给坐标轴加上标签
        plt.title("Square Numbers", fontsize=24)
        plt.xlabel("Value", fontsize=14)
        plt.ylabel("Square of Value", fontsize=14)

        # 设置刻度标记的大小
        plt.tick_params(axis='both', which='major', labelsize=14)



    #Bar柱状图
    def paint_widget_02(self):
        figure = plt.figure()
        canvas = FigureCanvas(figure)
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        self.widget_02.setLayout(layout)
        #绘图
        N = 5
        menMeans = (20, 35, 30, 35, 27)
        womenMeans = (25, 32, 34, 20, 25)
        menStd = (2, 3, 4, 1, 2)
        womenStd = (3, 5, 2, 3, 3)
        ind = np.arange(N)  # the x locations for the groups
        width = 0.5  # the width of the bars: can also be len(x) sequence

        p1 = plt.bar(ind, menMeans, width, yerr=menStd)
        p2 = plt.bar(ind, womenMeans, width,
                     bottom=menMeans, yerr=womenStd)
        plt.ylabel('Scores')
        plt.title('Scores by group and gender')
        plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
        plt.yticks(np.arange(0, 81, 10))
        plt.legend((p1[0], p2[0]), ('Men', 'Women')) # 添加图例


    def paint_widget_04(self):
        figure = plt.figure(figsize=(8, 3))
        canvas = FigureCanvas(figure)
        ax1 = figure.add_subplot(121, projection='3d')
        ax2 = figure.add_subplot(122, projection='3d')
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        self.widget_04.setLayout(layout)
        # fake data
        _x = np.arange(4)
        _y = np.arange(5)
        _xx, _yy = np.meshgrid(_x, _y)
        x, y = _xx.ravel(), _yy.ravel()
        top = x + y
        bottom = np.zeros_like(top)
        width = depth = 1

        ax1.bar3d(x, y, bottom, width, depth, top, shade=True)
        ax1.set_title('Shaded')
        ax2.bar3d(x, y, bottom, width, depth, top, shade=False)
        ax2.set_title('Not Shaded')
        canvas.draw()
        self.mainwidget.setCurrentIndex(3)

    def  paint_widget_05(self):
        figure = plt.figure(facecolor='#FAFAD2') #可选参数,facecolor为背景颜色
        canvas = FigureCanvas(figure)  #创建的Figure本身是一个部件，它也是PyQt中的Widget  这是连接pyqt5与matplot
        #figure02 = plt.figure(facecolor='#FAFAD2')  # 可选参数,facecolor为背景颜色
        #canvas02 = FigureCanvas(figure02)
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        #layout.addWidget(canvas02)
        self.widget_05.setLayout(layout)
        #绘图
        x = np.arange(0, 2 * np.pi, 0.02)
        y = np.sin(x)
        y1 = np.sin(2 * x)
        y2 = np.sin(3 * x)
        ym1 = np.ma.masked_where(y1 > 0.5, y1)
        ym2 = np.ma.masked_where(y2 < -0.5, y2)
        lines = plt.plot(x, y, x, ym1, x, ym2, 'o')
        # 设置线的属性
        plt.setp(lines[0], linewidth=1)
        plt.setp(lines[1], linewidth=2)
        plt.setp(lines[2], linestyle='-', marker='^', markersize=4)
        # 线的标签
        plt.legend(('No mask', 'Masked if > 0.5', 'Masked if < -0.5'), loc='upper right')
        plt.title('Masked line demo')
        plt.xlabel("time")
        plt.ylabel("value")
        canvas.draw()

    def paint_widget_06(self):
        figure, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
        canvas = FigureCanvas(figure)  #创建的Figure本身是一个部件，它也是PyQt中的Widget  这是连接pyqt5与matplot
        layout = QHBoxLayout()
        layout.addWidget(canvas)
        self.widget_06.setLayout(layout)
        #饼状图
        recipe = ["375 g flour",
                  "75 g sugar",
                  "250 g butter",
                  "300 g berries"]

        data = [float(x.split()[0]) for x in recipe]
        ingredients = [x.split()[-1] for x in recipe]

        def func(pct, allvals):
            absolute = int(pct / 100. * np.sum(allvals))
            return "{:.1f}%\n({:d} g)".format(pct, absolute)

        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                          textprops=dict(color="w"))

        ax.legend(wedges, ingredients,
                  title="Ingredients",
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")

        ax.set_title("Matplotlib bakery: A pie")

    def paint_widget_07(self):
        figure, (vax, hax) = plt.subplots(1, 2, figsize=(12, 6))
        canvas = FigureCanvas(figure)  #创建的Figure本身是一个部件，它也是PyQt中的Widget  这是连接pyqt5与matplot
        layout = QHBoxLayout()
        layout.addWidget(canvas)
        self.widget_07.setLayout(layout)
        #饼状图
        t = np.arange(0.0, 5.0, 0.1)
        s = np.exp(-t) + np.sin(2 * np.pi * t) + 1
        nse = np.random.normal(0.0, 0.3, t.shape) * s
        vax.plot(t, s + nse, '^')
        vax.vlines(t, [0], s)
        # By using ``transform=vax.get_xaxis_transform()`` the y coordinates are scaled
        # such that 0 maps to the bottom of the axes and 1 to the top.
        vax.vlines([1, 2], 0, 1, transform=vax.get_xaxis_transform(), colors='r')
        vax.set_xlabel('time (s)')
        vax.set_title('Vertical lines demo')

        hax.plot(s + nse, t, '^')
        hax.hlines(t, [0], s, lw=2)
        hax.set_xlabel('time (s)')
        hax.set_title('Horizontal lines demo')


if __name__  == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mywidget = MyWidget()
    mywidget.show()
    app.exec()
