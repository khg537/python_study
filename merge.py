import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import re
import os

import requests
import bs4


form_class = uic.loadUiType("merge.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.OnOpenDocument)
        self.pushButton_2.clicked.connect(self.filelists)
        
        self.merge_list =[]
            
    def OnOpenDocument(self):
        print("select button")
        fname = QFileDialog.getOpenFileName(self, 'Open file', "",
                                        "All Files(*);; Python Files(*.py)", '/home')
        # if fname[0]:
        #     f = open(fname[0], 'r', encoding = "utf-8")
        #     flines = f.readlines()

        #     for line in flines:
        #         print(line)
        # else:
        #     QMessageBox.about(self, "Warning", "파일을 선택하지 않았습니다.")
        print(fname)
        self.merge_list.append(fname[0])
        self.textBrowser.append(os.path.basename(fname[0]))
            
    def filelists(self):
        for e in self.merge_list:
            print(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()