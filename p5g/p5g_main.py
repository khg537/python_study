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

import subprocess
import pickle
from P5GLog import PLog

from os import path

g_lists = []
drop_cnt = 0

form_class = uic.loadUiType("p5g_merge.ui")[0]

class Thread1(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.file_df = None
    
    def run(self):
       self.file_df = self.parent.Log.MergeFile()

       t_time = datetime.datetime.now()
       fname = t_time.strftime("Merge_%Y_%m_%d_%H_%M_%S.log")
       self.file_df.to_csv(fname, sep='\t', index=False)
       # print(self.file_df)
       self.parent.label_select.setText(f"{fname} 생성")       
       
    def get_file_df(self):
        return self.file_df


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        
        super().__init__()
        self.setupUi(self)

        self.PB_DIR.clicked.connect(self.OnDirFile)
        self.PB_FILES.clicked.connect(self.OnFiles)

        self.PB_MERGE.clicked.connect(self.MergeFile)
        self.PB_CLEAR.clicked.connect(self.ClearFile)
        
        self.PB_MSG.clicked.connect(self.MsgFile)
        self.PB_EXPLORER.clicked.connect(self.FileExplorer)
        self.PB_NOTEPAD.clicked.connect(self.RunNotepad)
        self.PB_QDIR.clicked.connect(self.RunQdir)
        
        self.file_df = 123
        self.message_df = None
        
        self.cur_dir = self.ReadFileDir()
        
        self.textBrowser.setPlainText("")
        self.label_select.setText("0 개 선택")
        self.Log = PLog()
       
        self.child_thread = Thread1(self)
      
    def OnDirFile(self):
               # fname = QFileDialog.getOpenFileName(self, 'Open file', "",
        #                                 "All Files(*);; log Files(*.log)", '/home')
        
        # Directory 를 선택합니다.
        folder = QFileDialog.getExistingDirectory(self, "Select Directory", self.cur_dir)
   
        
        self.Log.add(folder, None)
        
        self.PrintFiles()
        self.cur_dir = os.getcwd()
        self.WriteFileDir()

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
        files = QFileDialog.getOpenFileNames(self, 'Choose Files', self.cur_dir,  filter='*.*')
        fnames = files[0]
        # print(files)
        print(os.getcwd())
        self.Log.add(None, fnames)
        self.PrintFiles()
        self.cur_dir = os.getcwd()
        self.WriteFileDir()

    def MergeFile(self):
        # self.file_df = self.Log.MergeFile()
        
        self.child_thread.start()
        self.label_select.setText(f"Merge File 생성 중......")
        
        # t_time = datetime.datetime.now()
        # fname = t_time.strftime("Merge_%Y_%m_%d_%H_%M_%S.log")
        # self.file_df.to_csv(fname, sep='\t', index=False)
        # # print(self.file_df)
        # self.label_select.setText(f"{fname} 생성")
   
    def ClearFile(self):
        self.Log.clear_file()
        self.textBrowser.setPlainText("")
        self.label_select.setText("0 개 선택")

    def PrintFiles(self):
        i = 0
        files = self.Log.get_files()
        for i, file in enumerate(files):
            self.textBrowser.append(file)
            
        self.label_select.setText(f"{i+1}개 선택")
        
    def MsgFile(self):
        self.message_df = self.Log.MakeMessage()
        self.message_df.columns = ['time', 'value']

        self.message_df['time'] = pd.to_datetime(self.message_df['time'])
        self.message_df = self.message_df.sort_values(by='time')  
       
        cont_series = self.message_df.iloc[:,1]
        for i, cont in cont_series.items():
            self.print_list_prettier(cont)
        
    def print_list_prettier(self, prt_list):
        t_time = datetime.datetime.now()
        fname = t_time.strftime("Message_%Y_%m_%d_%H_%M_%S.log")
        
        for i in prt_list:
            with open(fname, "a") as f:
                f.write(i + "\n")
              
        self.label_select.setText(f"\n{fname} 생성")
        
    def FileExplorer(self):
        self.cur_dir = self.ReadFileDir()
        print("222",self.cur_dir)
        os.startfile(self.cur_dir)
        
    def ReadFileDir(self):
        if path.exists('Filedir.cfg'):
           with open("Filedir.cfg") as f:
                return(f.readline().strip())
        else:
            self.cur_dir = "c:\\"
            self.WriteFileDir()
        
        if self.cur_dir == None:
            self.cur_dir = "c:\\"
    
    def WriteFileDir(self):
        with open("Filedir.cfg", "w") as f:
            f.write(self.cur_dir)
            
    def RunNotepad(self):
        subprocess.call(["C:\\Program Files\\Notepad++\\notepad++.exe"])
        
    def RunQdir(self):
        subprocess.call(["C:\\Program Files (x86)\\Q-Dir\\Q-Dir.exe"])
     
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
    
