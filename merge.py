import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import re
import os

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

g_lists =[]
drop_cnt = 0

form_class = uic.loadUiType("merge.ui")[0]

def log_to_df(in_name):
        global drop_cnt
        rd_list =[]
        check=0
        with open(in_name,"r", encoding='UTF8', errors='ignore') as fp1:
            while(True):
                rd = fp1.readline()
                rd=rd.strip()
                print(rd)
                rd_columns = rd.split(" ",2)
                if not rd:
                    break
                    
                rd_list.append(rd_columns)
                
        df =pd.DataFrame(rd_list)
        # df = df.applymap(lambda x: ILLEGAL_CHARACTERS_RE.sub(r'', x) if isinstance(x, str) else x)
        df.columns = ['날짜', '시간', '내용']
        df["날짜_전처리"] = "2021-"+df["날짜"]+" "+df["시간"]
        df["날짜_전처리"] = pd.to_datetime(df["날짜_전처리"], errors = 'coerce')
        return df
        
def thread_filelists(file_list):
    print("thread start")
    index = 0
    for e in file_list:
        print(e)
        if index == 0:
            df = log_to_df(e)
        else:
            t_df = log_to_df(e)
            df = pd.concat([df, t_df], axis = 0)
        index +=1
        
    
    df = df.sort_values(by=['날짜_전처리'])
    df =  df.drop(['날짜_전처리'], axis =1)  

    df.to_csv("./merge.log", index = False, header = None, sep="\t")
    
class Thread1(QThread): 
    threadEvent = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__()
        self.main = parent

 
    def run(self): 
        print("threading start")
        self.do_worker(g_lists)
        
    def do_worker(self, lists):
        print(lists)
        thread_filelists(lists)
        self.threadEvent.emit("end")
       

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.OnOpenDocument)
        self.pushButton_2.clicked.connect(self.filelists)
        self.pushButton_3.clicked.connect(self.clear_lists)
        
        self.merge_list =[]
        self.th = Thread1(self)
        self.th.threadEvent.connect(self.threadEventHandler)  # custom signal from worker thread to main thread
        
        
    def OnOpenDocument(self):
        print("select button")
        fname = QFileDialog.getOpenFileName(self, 'Open file', "",
                                        "All Files(*);; log Files(*.log)", '/home')
        # if fname[0]:
        #     f = open(fname[0], 'r', encoding = "utf-8")
        #     flines = f.readlines()

        #     for line in flines:
        #         print(line)
        # else:
        #     QMessageBox.about(self, "Warning", "파일을 선택하지 않았습니다.")
        print(fname)
        
        for e in self.merge_list:
            print(e, fname[0])
            if fname[0] == e:
                QMessageBox.about(self, "Warning", "이미 추가되어있습니다.")
                return
        self.merge_list.append(fname[0])    
        self.textBrowser.append(os.path.basename(fname[0]))
            
    def filelists(self):
        global g_lists
        print("start")
        g_lists = self.merge_list
        self.th.start()
        
    def clear_lists(self):
        self.merge_list = 0
        self.textBrowser.clear()
    
    def threadEventHandler(self, mystr):
        print("1 Recevied Thread: ", mystr)
        if mystr == "end":
            QMessageBox.about(self, "Information", "머지 완료")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
    
