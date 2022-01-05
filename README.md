import os
import sys
import time

if sys.platform.startswith("linux"):
    sys.path.append('/opt/qcom/QUTS/Support/python')
elif sys.platform.startswith("win"):
    sys.path.append('C:\Program Files (x86)\Qualcomm\QUTS\Support\python')
elif sys.platform.startswith("darwin"):
    sys.path.append('/Applications/Qualcomm/QUTS/QUTS.app/Contents/Support/python')
    
import QutsClient
import Common.ttypes
import pickle

import DiagService.DiagService
import DiagService.constants
import DiagService.ttypes

import LogSession.LogSession
import LogSession.constants
import LogSession.ttypes

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import re
import os

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

import shutil

g_lists =[]
drop_cnt = 0

form_class = uic.loadUiType("emailtool.ui")[0]
 
class MyWindow(QMainWindow, form_class):
    def __init__(self):
        
        super().__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)
        
        self.fname = None
        self.send_name = None
        self.receive_name = None
        
        self.pushButton.clicked.connect(self.sendCommand)
        self.pushButton_2.clicked.connect(self.resetCommand)

    def dragEnterEvent(self, e):
        print("dragEnter")
        e.accept()

    def dropEvent(self, e):
        print("dropEvent")
        result = e.mimeData().text().replace("file:///", "")

        print(result)
        fname = os.path.basename(result)
        self.fname = "c:/temp/"+f"{fname}"
        if os.path.exists("c:/temp/"):
           shutil.make_archive(self.fname, "zip", result)
        else:
           os.mkdir("c:/temp")
           shutil.make_archive(self.fname, "zip", result)
           
       # os.remove(f"{fname}.zip")
  
        self.label_5.setText(f"{self.fname}.zip")                
            
    def resetCommand(self):
        os.remove(f"{self.fname}.zip")
        self.label_5.setText("없음")
        
    def sendCommand(self):
        QMessageBox.about(self, "Information", "송부완료")
        self.saveFile()
        
    def slot_send(self):
        print(self.plainTextEdit.toPlainText())
        self.send_name = self.plainTextEdit.toPlainText()    
        
        
    def slot_receive(self):
        print(self.plainTextEdit_2.toPlainText())
        self.receive_name = self.plainTextEdit.toPlainText()
        
    def slot_contents(self):
        print(self.textEdit.toPlainText())
        
    def slot_ID(self):
         print(self.lineEdit.toPlainText())
        
    def slot_pw(self):
         print(self.lineEdit_2.toPlainText())
         
    def saveFile(self):
        print("saveFile")
        user = {'name':'Andrew K. Johnson', 'score': 199, 'location':[38.189323, 127.3495672]}
        
        # save data
        with open('user.pickle','wb') as fw:
            pickle.dump(user, fw)

        # load data
        with open('user.pickle', 'rb') as fr:
            user_loaded = pickle.load(fr)

        # show data
        print(user_loaded)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
    
