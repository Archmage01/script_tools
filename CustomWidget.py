#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPoint,pyqtSignal
from PyQt5.QtGui import QFont,QMouseEvent, QEnterEvent, QPainter,QColor,QPen, QIcon
import sys,os,time

'''
自定义无边框widget:
    1 基本功能: 最大化,最小化,关闭,拖动窗口
    2 菜单栏等其他自行添加
'''

class QssLoad(object):
    def __init__(self):
        pass

    @staticmethod
    def load_style(selfstyle: str):
        with open('qss/%s'%(selfstyle), 'r', encoding='utf8') as f:
            return f.read()


class TitleBar(QWidget):
    windowMinimumed = pyqtSignal()       # 窗口最小化信号
    windowMaximumed = pyqtSignal()       # 窗口最大化信号
    windowNormaled  = pyqtSignal()       # 窗口还原信号
    windowClosed    = pyqtSignal()       # 窗口关闭信号
    windowMoved     = pyqtSignal(QPoint) # 窗口移动

    def __init__(self, *args, **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)
        # 支持qss设置背景
        #self.setAttribute(Qt.WA_StyledBackground, True)
        self.mPos = None
        self.iconSize = 20  # 图标的默认大小
        # 设置默认背景颜色,否则由于受到父窗口的影响导致透明
        # self.setAutoFillBackground(True)
        # palette = self.palette()
        # palette.setColor(palette.Window, QColor(240, 240, 240))
        # self.setPalette(palette)
        # 布局
        layout = QHBoxLayout(self, spacing=0)
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        # 窗口图标
        self.iconLabel = QLabel(self)
#         self.iconLabel.setScaledContents(True)
        layout.addWidget(self.iconLabel)
        layout.addSpacing(0)
        # 窗口标题
        self.titleLabel = QLabel(self)
        self.titleLabel.setMargin(0)
        layout.addWidget(self.titleLabel)
        layout.addSpacing(0)
        # 中间伸缩条
        layout.addSpacerItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        # 利用Webdings字体来显示图标
        font = self.font() or QFont()
        font.setFamily('Webdings')
        # 最小化按钮
        self.buttonMinimum = QPushButton(
            '0', self, clicked=self.windowMinimumed.emit, font=font, objectName='buttonMinimum')
        layout.addWidget(self.buttonMinimum)
        # 最大化/还原按钮
        self.buttonMaximum = QPushButton(
            '1', self, clicked=self.showMaximized, font=font, objectName='buttonMaximum')
        layout.addWidget(self.buttonMaximum)
        # 关闭按钮
        self.buttonClose = QPushButton(
            'r', self, clicked=self.windowClosed.emit, font=font, objectName='buttonClose')
        layout.addWidget(self.buttonClose)
        # 初始高度
        self.setHeight()

    def showMaximized(self):
        if self.buttonMaximum.text() == '1':
            # 最大化
            self.buttonMaximum.setText('2')
            self.windowMaximumed.emit()
        else:  # 还原
            self.buttonMaximum.setText('1')
            self.windowNormaled.emit()

    def setHeight(self, height=28):
        """设置标题栏高度"""
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        # 设置右边按钮的大小
        self.buttonMinimum.setMinimumSize(height, height)
        self.buttonMinimum.setMaximumSize(height, height)
        self.buttonMaximum.setMinimumSize(height, height)
        self.buttonMaximum.setMaximumSize(height, height)
        self.buttonClose.setMinimumSize(height, height)
        self.buttonClose.setMaximumSize(height, height)

    def setTitle(self, title):
        """设置标题"""
        self.titleLabel.setText(title)

    def setIcon(self, icon):
        """设置图标"""
        self.iconLabel.setPixmap(icon.pixmap(self.iconSize, self.iconSize))

    def setIconSize(self, size):
        """设置图标大小"""
        self.iconSize = size

    def enterEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        super(TitleBar, self).enterEvent(event)

    def mouseDoubleClickEvent(self, event):
        super(TitleBar, self).mouseDoubleClickEvent(event)
        self.showMaximized()

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()
        event.accept()

    def mouseReleaseEvent(self, event):
        '''鼠标弹起事件'''
        self.mPos = None
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mPos:
            self.windowMoved.emit(self.mapToGlobal(event.pos() - self.mPos))
        event.accept()

# 枚举左上右下以及四个定点
Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(8)

class CustomWidget(QWidget):
    # 四周边距
    Margins = 2
    def __init__(self):
        super().__init__()
        self.resize(400, 300)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框
        # 鼠标跟踪
        self.setMouseTracking(True)
        self.show()
        #设置透明度
        self.setWindowOpacity(1)
        # layout 
        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.titleBar  =  TitleBar()
        self.mainlayout.addWidget(self.titleBar)
        self.mainlayout.setSpacing(0)
        self.mainlayout.setContentsMargins(0,0,0,0)
        #菜单栏
        self.menubar = QMenuBar(self)
        #slot
        self.titleBar.windowMinimumed.connect(self.showMinimized)
        self.titleBar.windowMaximumed.connect(self.showMaximized)
        self.titleBar.windowNormaled.connect(self.showNormal)
        self.titleBar.windowClosed.connect(self.close)
        self.titleBar.windowMoved.connect(self.move)
        #########################
        self._pressed  = False
        self.Direction = None
        self.installEventFilter(self)

    def addMenu(self, menubar):
        self.mainlayout.insertWidget(1, menubar)
        self.mainlayout.setSpacing(0)

    #设置标题栏stylesheet
    def settitleBarstylesheet(self,style):
        self.titleBar.setStyleSheet(style)

    def showNormal(self):
        """还原,要保留上下左右边界,否则没有边框无法调整"""
        super(CustomWidget, self).showNormal()
        self.layout().setContentsMargins(
            self.Margins, self.Margins, self.Margins, self.Margins)
    
    #重写设置窗口标题
    def setWindowTitle(self, title: str): 
        self.titleBar.setTitle(title)

    #子控件widget
    def setCenterWidget(self, wedget, stretch=0 ):
        self.mainlayout.addWidget(wedget,stretch)
        self.mainlayout.addStretch()

    #子控件layout
    def setCenterLayout(self, layout, stretch=10 ):
        self.mainlayout.addLayout(layout,stretch )
        self.mainlayout.addStretch()


    def mouseMoveEvent(self, event: QMouseEvent):
        """重写鼠标移动事件"""
        super(CustomWidget, self).mouseMoveEvent(event)
        pos = event.pos()              #返回相对于控件的当前鼠标位置的QPoint对象;
        xPos, yPos = pos.x(), pos.y()
        #################
        wm, hm = self.width() - self.Margins, self.height() - self.Margins
        if self.isMaximized() or self.isFullScreen():
            self.Direction = None
            self.setCursor(Qt.ArrowCursor)
            return
        if event.buttons() == Qt.LeftButton and self._pressed:
            self._resizeWidget(pos)
            return
        if xPos <= self.Margins and yPos <= self.Margins:
            # 左上角
            self.Direction = LeftTop
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm <= xPos <= self.width() and hm <= yPos <= self.height():
            # 右下角
            self.Direction = RightBottom
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm <= xPos and yPos <= self.Margins:
            # 右上角
            self.Direction = RightTop
            self.setCursor(Qt.SizeBDiagCursor)
        elif xPos <= self.Margins and hm <= yPos:
            # 左下角
            self.Direction = LeftBottom
            self.setCursor(Qt.SizeBDiagCursor)
        elif 0 <= xPos <= self.Margins and self.Margins <= yPos <= hm:
            # 左边
            self.Direction = Left
            self.setCursor(Qt.SizeHorCursor)
        elif wm <= xPos <= self.width() and self.Margins <= yPos <= hm:
            # 右边
            self.Direction = Right
            self.setCursor(Qt.SizeHorCursor)
        elif self.Margins <= xPos <= wm and 0 <= yPos <= self.Margins:
            # 上面
            self.Direction = Top
            self.setCursor(Qt.SizeVerCursor)
        elif self.Margins <= xPos <= wm and hm <= yPos <= self.height():
            # 下面
            self.Direction = Bottom
            self.setCursor(Qt.SizeVerCursor)

    def _resizeWidget(self, pos):
        """调整窗口大小"""
        if self.Direction == None:
            return
        mpos = pos - self._mpos
        xPos, yPos = mpos.x(), mpos.y()
        geometry = self.geometry()
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()
        if self.Direction == LeftTop:  # 左上角
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
        elif self.Direction == RightBottom:  # 右下角
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos = pos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos = pos
        elif self.Direction == RightTop:  # 右上角
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos.setX(pos.x())
        elif self.Direction == LeftBottom:  # 左下角
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos.setY(pos.y())
        elif self.Direction == Left:  # 左边
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            else:
                return
        elif self.Direction == Right:  # 右边
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos = pos
            else:
                return
        elif self.Direction == Top:  # 上面
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            else:
                return
        elif self.Direction == Bottom:  # 下面
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos = pos
            else:
                return
        self.setGeometry(x, y, w, h)

    def mousePressEvent(self, event: QMouseEvent): 
        """重写鼠标点击事件"""
        super(CustomWidget, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._mpos = event.pos()
            self._pressed = True

    def mouseReleaseEvent(self, event: QMouseEvent):
        '''鼠标弹起事件''' 
        super(CustomWidget, self).mouseReleaseEvent(event)
        self._pressed = False
        self.Direction = None

    def move(self, pos):
        if self.windowState() == Qt.WindowMaximized or self.windowState() == Qt.WindowFullScreen:
            # 最大化或者全屏则不允许移动
            return
        super(CustomWidget, self).move(pos)

    def eventFilter(self, obj, event):
        """事件过滤器,用于解决鼠标进入其它控件后还原为标准鼠标样式"""
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
        return super(CustomWidget, self).eventFilter(obj, event)

    def paintEvent(self, event):
        """由于是全透明背景窗口,重绘事件中绘制透明度为1的难以发现的边框,用于调整窗口大小"""
        super(CustomWidget, self).paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255, 1), 2 * self.Margins))
        painter.drawRect(self.rect())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = CustomWidget()
    test.setWindowTitle("自定义窗口")
    
    #菜单
    menubar = QMenuBar()
    ttt = menubar.addMenu("文件")
    sel = menubar.addMenu("选择")
    ttt.addAction("新建")
    sel.addAction("全选")
    
    frame = QFrame()
    frame.setFixedHeight(200)
    frame.setStyleSheet("background-color:#3c3c3c")
    test.mainlayout.addWidget(frame)
    test.addMenu(menubar)
    test.mainlayout.addStretch()

    sys.exit(app.exec_())   