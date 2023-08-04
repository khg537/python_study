import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import re
import os

import datetime
import requests
import bs4
import pandas as pd
import threading

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QWaitCondition
from PyQt5.QtCore import QMutex
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
import pickle
from P5GLog import PLog

g_lists =[]
drop_cnt = 0

form_class = uic.loadUiType("p5g_merge.ui")[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        
        super().__init__()
        self.setupUi(self)

        self.PB_DIR.clicked.connect(self.OnDirFile)
        self.PB_FILES.clicked.connect(self.OnFiles)

        self.PB_MERGE.clicked.connect(self.MergeFile)
        self.PB_CLEAR.clicked.connect(self.ClearFile)
        
        self.file_df = None
        self.Log = PLog()
       
        
    def OnDirFile(self):
               # fname = QFileDialog.getOpenFileName(self, 'Open file', "",
        #                                 "All Files(*);; log Files(*.log)", '/home')
        
        # Directory 를 선택합니다.
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        print(folder)
        
        self.Log.add(folder, None)
        

        # C:/Users/combr/PycharmProjects/somePath/venv/Lib
        
        # File 하나를 선택합니다. Tuple 로 리턴합니다. 첫번째 path:str
        # file = QFileDialog.getOpenFileName(self.window, 'Choose File', folder, filter='')
        # print(file)
        # ('C:/Users/combr/setuptools-40.8.0-py3.7.egg', 'All Files (*)')
        
        # File 여러개를 선택합니다. Tuple로 리턴합니다.첫번째 files:list
        # files = QFileDialog.getOpenFileNames(self.window, 'Choose Files', folder, filter='*.pth')
        # print(files)
        # (['C:/Users/combr/easy-install.pth', 'C:/Users/combr/setuptools.pth'], '*.pth')

    def OnFiles(self):
        files = QFileDialog.getOpenFileNames(self, 'Choose Files',  filter='*.*')
        fnames = files[0]
        self.Log.add(None, fnames)

    def MergeFile(self):
        self.file_df = self.Log.MergeFile()
        t_time = datetime.datetime.now()
        fname = t_time.strftime("Merge_%Y_%m_%d_%H_%M_%S.log")
        self.file_df.to_csv(fname, sep='\t', index=False)

    def ClearFile(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
    
