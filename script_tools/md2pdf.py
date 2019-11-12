#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: yang.gan  2019-10-12 19:38:27


import os,re,sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

from win32com.client import gencache
from win32com.client import constants, gencache
 
def createPdf(wordPath, pdfPath):
    """
    word转pdf
    :param wordPath: word文件路径
    :param pdfPath:  生成pdf文件路径
    """
    word = gencache.EnsureDispatch('Word.Application')
    doc = word.Documents.Open(wordPath, ReadOnly=1)
    doc.ExportAsFixedFormat(pdfPath,
                            constants.wdExportFormatPDF,
                            Item=constants.wdExportDocumentWithMarkup,
                            CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
    word.Quit(constants.wdDoNotSaveChanges)

inpp = os.getcwd() + "\\1.docx"
outpp = os.getcwd() + "\\1.pdf"

#createPdf(inpp, outpp)

css = """
    QPushButton{  color:red; border-color:green; border-width:1px; }  
    QPushButton:hover{background-color:#1E1E1E; color:red;  border: 1px solid #008B00;  }  
    QPushButton:pressed{background-color:red; color:white;  }  
"""


class  ToolsUi(QWidget):
        def  __init__(self, parent=None):
            super(ToolsUi,self).__init__(parent)
            self.desktop = QApplication.desktop()
            self.screenRect = self.desktop.screenGeometry()
            self.height = self.screenRect.height()
            self.width = self.screenRect.width()
            self.resize(400, 80 ) #w h
            self.setWindowTitle(" 自用格式转化工具 markdown-> pdf   markdown-> docx ")

            self.rootpath = os.getcwd() 
            self.mdname = ""

            #
            self.markdown_chose = QPushButton(" markdown转PDF ",self)
            self.markdown_chose.setFixedSize(200,80)
            self.markdowntoword = QPushButton(" markdown转word ",self)
            self.markdowntoword.setFixedSize(200,80)
            self.markdowntoword.move(200,0)

            #slot
            self.markdown_chose.clicked.connect(self.md_chose_slot)

            self.setStyleSheet(css)

        def md_chose_slot(self):
            self.markdown = ""
            Widget = QWidget()
            self.markdown, filetype = QFileDialog.getOpenFileName(Widget,
                                                                      "选取文件",
                                                                      os.getcwd(),
                                                                      "Text Files (*.md)")
            if self.markdown == "":
                print("错误:请未选择.md 文件")
                return
            # print(self.markdown)
            self.mdname = self.markdown.split("/")[-1].split(".")[0]
            cmd_str =  "pandoc \"%s.md\" -o %s.docx"%(self.mdname,self.mdname)
            print(cmd_str)
            os.system( cmd_str )
            wordPath = self.rootpath + "\\" + self.mdname + ".md"
            pdfPath  = self.rootpath + "\\" + self.mdname + ".pdf"
            self.createPdf(wordPath, pdfPath )


        def createPdf(self, wordPath, pdfPath):
            """
            word转pdf
            :param wordPath: word文件路径
            :param pdfPath:  生成pdf文件路径
            """
            word = gencache.EnsureDispatch('Word.Application')
            doc = word.Documents.Open(wordPath, ReadOnly=1)
            doc.ExportAsFixedFormat(pdfPath,
                                    constants.wdExportFormatPDF,
                                    Item=constants.wdExportDocumentWithMarkup,
                                    CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
            word.Quit(constants.wdDoNotSaveChanges)

        def md2pdf(self):
            pass



if __name__ == "__main__":
    app  = QApplication(sys.argv)
    demo = ToolsUi()
    demo.show()
    sys.exit(app.exec_())