#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time :2021/3/31 22:09
#  提供画流程图的基本操作（仅仅在visio 2013上测试过）

import win32com.client
import os, sys, re
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import  ( QApplication,QWidget,QProgressBar,QLabel,QLineEdit,QPushButton,
     QGridLayout,QVBoxLayout,QHBoxLayout,QFrame,QTableWidget,QTableWidgetItem,QMessageBox,QComboBox )

FlowchartTemplateName_x="BASFLO_M.VSTX"
FlowchartStencilName_x ="BASFLO_M.VSSX"
MasterProcessName      ="Process"
MasterDecisionName     ="Decision"
MasterEndName          ="Terminator"
VS2010MasterEndName    ="Start/End" # 在visio2010中使用不同的Name，此处需要注意

# 节点的类型
NODE_P       =0 #流程
NODE_IF      =1 #判断
NODE_SEND    =2 #开始结束
NODE_NONE    =3

ELEM_TYPE=0

N=0 #北
S=1 #南
W=2 #西
E=3 #东

_node_dir_map = [   #N  S  W  E
    [3, 2, 0, 1],   #NODE_P
    [2, 3, 0, 1],   #NODE_IF
    [1, 0, 2, 3],   #NODE_END
]

# P 表示procedure
# D 表示decision
# E 表示east
# W 表示west
# N 表示north
# S 表示south
CONN_P2P = 0    #
CONN_P2D = 1    #
CONN_D2P = 2
CONN_P2E = 3
CONN_E2E = 4
CONN_E2P = 5
CONN_D2U = 6
CONN_P2N = 7
CONN_D2N = 8
CONN_W2W = 9

# 获取偏移量
OFFSET_INDEX    =0
OFFSET_COMMENT  =1
OFFSET_PROP     =2
OFFSET_X        =3
OFFSET_Y        =4
OFFSET_LINK     =5
OFFSET_LINK2    =6
OFFSET_N        =7

MAP_SHAPE=0
MAP_DATA=1


# 获取完整文件名
def get_full_name(name):
    if (len(name.split(':')) == 1):
        filename = os.path.dirname(sys.argv[0])+"\\"+name
    else:
        filename = name
    return filename

class VisioDraw(object):
    def __init__(self, filename, autoquit=0):
        self.filename=filename
        self.autoquit=autoquit
        self.pgcount = 0
        self.ver = 0
        self.elem_map = {}

    def open(self, name=''):
        if (name!=''):
            self.filename = get_full_name(name)
        print('Drawing vsdx:', self.filename)
        self.visio = win32com.client.Dispatch("Visio.Application")
        #self.Visio = win32com.client.Dispatch("Visio.InvisibleApp")
        self.visio.Visible = 1

        self.ver = int(float(self.visio.Version))
        #print("visio version : ", self.ver )
        # ver 11: visio 2003
        # ver 12: visio 2007
        # ver 15: visio 2013
        FlowchartTemplateName = FlowchartTemplateName_x
        FlowchartStencilName = FlowchartStencilName_x

        self.objtable = {}
        # add a new file using visio template name
        self.docFlowTemplate = self.visio.Documents.Add(FlowchartTemplateName)

        # Search open documents for our flowchart stencil:
        for doc in self.visio.Documents :
            #print doc.Name, FlowchartStencilName, doc.Name == FlowchartStencilName
            if (doc.Name == FlowchartStencilName):
                docFlowStencil = doc
                break

        # Step 2: get the masters and connect.
        # ------------------------------------------------
        # Get masters for Process and Decision:
        mstProcess = docFlowStencil.Masters.ItemU(MasterProcessName)
        mstDecision = docFlowStencil.Masters.ItemU(MasterDecisionName)
        try:
            mstEnd = docFlowStencil.Masters.ItemU(MasterEndName)
        except:
            mstEnd = docFlowStencil.Masters.ItemU(VS2010MasterEndName)
        # 标准物体
        self.stdobj = [mstProcess, mstDecision, mstEnd, mstDecision, mstDecision]

        # Get the built-in connector object. Note, it's
        # not typed as a master!
        self.conn = self.visio.Application.ConnectorToolDataObject
        self.dx = 1.5
        self.dy = 0.8
        self.pgcount = 1

    # 保存文件
    def save(self, autoquit=True):
        print('saving visio %s'%self.filename)
        self.visio.ActiveDocument.SaveAs(self.filename)
        self.visio.ActiveDocument.Close()
        if autoquit:
            self.visio.Quit()
    # 关闭文件
    def close(self):
        # Deselect all shapes, so it looks better:
        self.visio.ActiveWindow.DeselectAll
        # Tile the windows so the user doesn't freak out!
        self.visio.ActiveDocument.SaveAs(self.filename)
        # 判断自动关闭
        if (self.autoquit == 1):
            self.visio.ActiveDocument.Close()
            self.visio.Quit()

    def new_page(self, name):
        if (self.pgcount == 0):
            self.open()
        # We'll draw on the first page of the document,
        # which is probably the only page in the document!
        if (self.pgcount == 1):
            self.pg = self.docFlowTemplate.Pages.Item(self.pgcount)
            # 针对visio2013，设置非填充主题
            if self.ver >=14:
                #self.pg.SetThemeVariant(1, 1)  # 红色判断框主题
                #self.pg.SetThemeVariant(0, 0)
                self.pg.SetTheme(0, 0, 0, 0, 0)
        else:
            # 如果是第二次，则需要增加页
            self.pg = self.docFlowTemplate.Pages.Add()

        self.pgcount += 1
        self.pg.Name = name
        self.pgwidth = self.pg.PageSheet.CellsU("PageWidth").ResultIU
        self.pgheight = self.pg.PageSheet.CellsU("PageHeight").ResultIU
        # Get the center, top of the page:
        self.orix = self.pgwidth / 6
        self.oriy = self.pgheight - 1
        self.elem_map.clear()
        return self.pg

    def copyvisiodraw(self):
        # 全选页内的所有元素
        self.visio.ActiveWindow.SelectAll()
        # 复制
        self.visio.ActiveWindow.Selection.Copy()

    def push_elem(self, id, type, x=0, y=0):
        self.elem_map[id] = [type, x, y]

    def get_cellsrc(self, node, direction):
        try:
            type = self.elem_map[node.ID][ELEM_TYPE]
            # 获取相关的接口
            return node.CellsSRC(7, _node_dir_map[type][direction], 0)
        except:
            return node.CellsU('PinX')

    # 绘制元素
    def draw_node(self, type, x:int, y:int, text:str, line=0):
        """
        @brief 绘制节点
        @type 节点类型
        @x  x轴偏移量
        @y  y轴偏移量
        @text 文字
        @line 线条宽度
        """
        shape = self.pg.Drop(self.stdobj[type], self.orix + self.dx*x, self.oriy - self.dy*y)
        shape.Text = text
        shape.Cells("Prop.Cost").ResultIU = line

        shape.Cells('Height').ResultIU = self.dy*5/8
        print("shape.ID:", shape.ID)

        self.push_elem(shape.ID, type, x, y)
        return shape

    # 连接接点
    #           2                    1
    #     0  Rect | D  1     2  Ellipse  3
    #           3                    0
    #     默认 CellsU("PinX")
    def conn_node(self, node1, node2, type=CONN_P2P, text='', width=0):
        print('conn', node1, node2)
        if (isinstance(node1, int)
                or isinstance(node2, int) ):
            # 在RETURN等封闭性的节点上，采用-1用于标记node2
            return
        if (node1 is None
                or node2 is None):
            # 在RETURN等封闭性的节点上，采用-1用于标记node2
            return

        con = self.pg.Drop(self.conn, 0, 0)
        # VisSectionIndices visSectionObject=1
        # VisRowIndices VisRowIndices=2
        # VisCellIndices visLineEndArrow=6
        con.CellsSRC(1, 2, 6).FormulaU = "1"

        self.push_elem(con.ID, type, node1.ID, node2.ID)

        #con = self.pg.Drop(self.conn, self.pgwidth, self.pgheight*0.75)
        if (text != ''):
            con.Text = text
        if (type == CONN_P2P):
            # 将起点连接到当前节点
            con.CellsU("BeginX").GlueTo(node1.CellsU("PinX"))
            # 将终点连接到当前节点
            con.CellsU("EndX").GlueTo(node2.CellsU("PinX"))
        elif (type == CONN_D2P):
            # 将起点连接到当前节点
            con.CellsU("BeginX").GlueTo(node1.CellsU("Connections.X2"))
            # 将终点连接到当前节点
            con.CellsU("EndX").GlueTo(node2.CellsU("PinX"))
        elif (type == CONN_D2U):
            # 将起点连接到当前节点
            con.CellsU("BeginX").GlueTo(node1.CellsU("Connections.X2"))
            # 将终点连接到当前节点
            con.CellsU("EndX").GlueTo(node2.CellsSRC(7, N, 0))
        elif (type == CONN_P2D):
            # 将起点连接到当前节点
            con.CellsU("BeginX").GlueTo(node1.CellsU("PinY"))
            # 将终点连接到当前节点
            con.CellsU("EndX").GlueTo(node2.CellsU("Connections.X1"))
        elif (type == CONN_P2E):
            # 将起点连接到当前节点
            con.CellsU("BeginX").GlueTo(node1.CellsU("PinX"))
            # 将终点连接到当前节点
            con.CellsU("EndX").GlueTo(node2.CellsU("PinY2"))
        elif (type == CONN_E2E):
            # 将起点连接到当前节点
            con.CellsU("BeginX").GlueTo(node1.CellsU("PinY"))
            con.CellsU("EndX").GlueTo(node2.CellsU("PinY"))
        elif (type == CONN_E2P):
            con.CellsU("BeginX").GlueTo(node1.CellsSRC(7, 1, 0))
            con.CellsU("EndX").GlueTo(node2.CellsU("PinX"))
            #con.CellsU("EndX").GlueTo(node2.CellsSRC(7, 0, 0))
        elif (type == CONN_P2N):
            con.CellsU("BeginX").GlueTo(node1.CellsU("PinX"))
            con.CellsU("EndX").GlueTo(self.get_cellsrc(node2, N))
        elif (type == CONN_D2N):
            con.CellsU("BeginX").GlueTo(node1.CellsU("Connections.X2"))
            con.CellsU("EndX").GlueTo(self.get_cellsrc(node2, N))
        elif (type == CONN_W2W):
            con.CellsU("BeginX").GlueTo(self.get_cellsrc(node1, W))
            con.CellsU("EndX").GlueTo(self.get_cellsrc(node2, W))
        else:
            return

        # 更新线段的width
        pass

    #
    def draw_table(self, table):
        try:
            # 遍历表中的元素
            for elem in table:
                # 放置图形 流程图基本元素
                if (elem[OFFSET_PROP] == NODE_NONE):
                    continue
                shape = self.draw_node(elem[OFFSET_PROP], elem[OFFSET_X], elem[OFFSET_Y], elem[OFFSET_COMMENT], elem[OFFSET_INDEX])
                self.objtable[elem[OFFSET_INDEX]] = [shape, elem]
            print("draw table")
            print(self.objtable)
            for elem in self.objtable.values():
                #print( elem)    # 打印所有的连接
                if (elem[MAP_DATA][OFFSET_LINK] != -1):
                    node=self.objtable[elem[MAP_DATA][OFFSET_LINK]]
                    text = ''
                    if (elem[MAP_DATA][OFFSET_PROP] == NODE_IF):
                        text = 'YES'
                    self.conn_node(elem[MAP_SHAPE], node[MAP_SHAPE], CONN_P2P, text)

                if (len(elem[MAP_DATA]) > OFFSET_LINK2
                        and elem[MAP_DATA][OFFSET_LINK2] != -1
                        ):
                    node=self.objtable[elem[MAP_DATA][OFFSET_LINK2]]
                    self.conn_node(elem[MAP_SHAPE], node[MAP_SHAPE], CONN_D2P, 'NO')
        except:
            return

class NodeWidget(QWidget):
    def __init__(self,ID=0 ):
        super(NodeWidget, self).__init__()
        laytout = QHBoxLayout()
        self.input_id = QLineEdit(str(ID))
        self.input_id.setFixedWidth(30)
        self.input_text = QLineEdit("")
        self.input_text.setFixedHeight(20)
        self.input_text.setFixedWidth(400)
        self.input_type = QComboBox()
        self.input_type.addItem('开始/结束')
        self.input_type.addItem('流程')
        self.input_type.addItem('判定')
        self.input_type.addItem('None')
        self.input_type.setFixedWidth(80)
        self.input_x = QLineEdit("0")
        self.input_x.setFixedWidth(30)
        self.input_y = QLineEdit("0")
        self.input_y.setFixedWidth(30)
        self.input_link1 = QLineEdit("")
        self.input_link1.setFixedWidth(30)
        self.input_link2 = QLineEdit("")
        self.input_link2.setFixedWidth(30)

        laytout.addWidget(self.input_id)
        laytout.addWidget(self.input_text)
        laytout.addWidget(self.input_type)
        laytout.addWidget(self.input_x)
        laytout.addWidget(self.input_y)
        laytout.addWidget(self.input_link1)
        laytout.addWidget(self.input_link2)
        laytout.addStretch()
        laytout.setContentsMargins(0,0,0,0)
        self.setLayout(laytout)
        self.data = [ ]

    def  get_node_info(self):
        print("读取数据")
        self.data.append(int(self.input_id.text()))
        self.data.append( self.input_text.text() )
        if '开始/结束' == self.input_type.currentText():
            self.data.append(2)
            print("开始/结束")
        elif '流程' == self.input_type.currentText():
            self.data.append(0)
            print("流程")
        elif '判定' == self.input_type.currentText():
            self.data.append(1)
            print("判定")
        else:
            print("None")
            self.data.append(3)
        print("===1===")
        self.data.append(int(self.input_x.text()))
        self.data.append(int(self.input_y.text()))
        if self.input_link1.text():
            self.data.append(int(self.input_link1.text()))
        if self.input_link2.text():
            self.data.append(int(self.input_link2.text()))

        print(self.data )
        return self.data

class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.setFixedSize(620,600)
        self.setWindowTitle("自动画流程图工具 version:1.0.0 ")
        self.laytout = QVBoxLayout(self)
        headwidget = QWidget(self)
        headlayout = QHBoxLayout()
        label01 = QLabel(" ID ")
        label02 = QLabel("流程图内容")
        label03 = QLabel("节点类型")
        label04 = QLabel("X坐标")
        label05 = QLabel("Y坐标")
        label06 = QLabel("link1")
        label07 = QLabel('link2')
        headlayout.addWidget(label01,3)
        headlayout.addWidget(label02,40)
        headlayout.addWidget(label03,8)
        headlayout.addWidget(label04,3)
        headlayout.addWidget(label05,3)
        headlayout.addWidget(label06,3)
        headlayout.addWidget(label07,3)
        headlayout.addStretch()
        headlayout.setContentsMargins(0,0,0,0)
        headwidget.setLayout(headlayout)
        btnwidget = QWidget()
        btnlayout = QHBoxLayout()
        self.add_btn = QPushButton("添加节点")
        self.start_btn = QPushButton("开始画图")
        btnlayout.addWidget(self.add_btn)
        btnlayout.addWidget(self.start_btn)
        btnwidget.setLayout(btnlayout)
        btnlayout.setContentsMargins(0,0,0,0)

        self.laytout.addStretch()
        self.laytout.addWidget(btnwidget)
        self.laytout.addWidget(headwidget)
        #self.laytout.addStretch()

        self.add_btn.clicked.connect(self.add_node)
        self.start_btn.clicked.connect(self.start_draw_visiflow)

        self.nodes = [ ]
        self.id = 0

    def add_node(self):
        node = NodeWidget(self.id)
        self.laytout.addWidget(node)
        self.nodes.append(node)
        #self.laytout.addStretch()
        self.id += 1

        #print("添加节点")

    def start_draw_visiflow(self):
        data = []
        for node in self.nodes:
            data.append(node.get_node_info())
        print(data)
        obj = VisioDraw(os.getcwd() + '\\2.vsdx', autoquit=False)
        obj.open()
        obj.new_page('第一页')
        obj.draw_table(data)
        obj.save()
        #


if __name__ == '__main__':
    # OFFSET_INDEX=0 OFFSET_COMMENT=1 OFFSET_PROP=2 OFFSET_X=3 OFFSET_Y=4 OFFSET_LINK=5 OFFSET_LINK2=6
    app = QApplication(sys.argv)
    mainwindows = MyWidget()
    mainwindows.show()
    sys.exit(app.exec())