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
    
    
    --------------------------------------------------------------
    <?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>640</width>
    <height>300</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QPlainTextEdit" name="plainTextEdit">
    <property name="geometry">
     <rect>
      <x>140</x>
      <y>20</y>
      <width>321</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QPlainTextEdit" name="plainTextEdit_2">
    <property name="geometry">
     <rect>
      <x>140</x>
      <y>70</y>
      <width>321</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>40</x>
      <y>30</y>
      <width>71</width>
      <height>16</height>
     </rect>
    </property>
    <property name="text">
     <string>보내는사람</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_2">
    <property name="geometry">
     <rect>
      <x>40</x>
      <y>80</y>
      <width>56</width>
      <height>12</height>
     </rect>
    </property>
    <property name="text">
     <string>받는 사람</string>
    </property>
   </widget>
   <widget class="QTextEdit" name="textEdit">
    <property name="geometry">
     <rect>
      <x>140</x>
      <y>120</y>
      <width>321</width>
      <height>61</height>
     </rect>
    </property>
   </widget>
   <widget class="QLabel" name="label_3">
    <property name="geometry">
     <rect>
      <x>40</x>
      <y>140</y>
      <width>56</width>
      <height>12</height>
     </rect>
    </property>
    <property name="text">
     <string>내용</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_4">
    <property name="geometry">
     <rect>
      <x>40</x>
      <y>200</y>
      <width>56</width>
      <height>12</height>
     </rect>
    </property>
    <property name="text">
     <string>첨부파일</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton">
    <property name="geometry">
     <rect>
      <x>520</x>
      <y>120</y>
      <width>75</width>
      <height>23</height>
     </rect>
    </property>
    <property name="text">
     <string>보내기</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_5">
    <property name="geometry">
     <rect>
      <x>140</x>
      <y>202</y>
      <width>321</width>
      <height>16</height>
     </rect>
    </property>
    <property name="text">
     <string>없음</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_2">
    <property name="geometry">
     <rect>
      <x>520</x>
      <y>160</y>
      <width>75</width>
      <height>23</height>
     </rect>
    </property>
    <property name="text">
     <string>리셋</string>
    </property>
   </widget>
   <widget class="QLineEdit" name="lineEdit">
    <property name="geometry">
     <rect>
      <x>140</x>
      <y>230</y>
      <width>141</width>
      <height>21</height>
     </rect>
    </property>
   </widget>
   <widget class="QLineEdit" name="lineEdit_2">
    <property name="geometry">
     <rect>
      <x>380</x>
      <y>230</y>
      <width>141</width>
      <height>21</height>
     </rect>
    </property>
   </widget>
   <widget class="QLabel" name="label_6">
    <property name="geometry">
     <rect>
      <x>70</x>
      <y>230</y>
      <width>56</width>
      <height>12</height>
     </rect>
    </property>
    <property name="text">
     <string>ID</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_7">
    <property name="geometry">
     <rect>
      <x>320</x>
      <y>233</y>
      <width>56</width>
      <height>12</height>
     </rect>
    </property>
    <property name="text">
     <string>PW</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>640</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections>
  <connection>
   <sender>plainTextEdit</sender>
   <signal>textChanged()</signal>
   <receiver>MainWindow</receiver>
   <slot>slot_send()</slot>
   <hints>
    <hint type="sourcelabel">
     <x>452</x>
     <y>61</y>
    </hint>
    <hint type="destinationlabel">
     <x>556</x>
     <y>59</y>
    </hint>
   </hints>
  </connection>
  <connection>
   <sender>plainTextEdit_2</sender>
   <signal>textChanged()</signal>
   <receiver>MainWindow</receiver>
   <slot>slot_receive()</slot>
   <hints>
    <hint type="sourcelabel">
     <x>450</x>
     <y>106</y>
    </hint>
    <hint type="destinationlabel">
     <x>575</x>
     <y>106</y>
    </hint>
   </hints>
  </connection>
  <connection>
   <sender>textEdit</sender>
   <signal>textChanged()</signal>
   <receiver>MainWindow</receiver>
   <slot>slot_contents()</slot>
   <hints>
    <hint type="sourcelabel">
     <x>428</x>
     <y>184</y>
    </hint>
    <hint type="destinationlabel">
     <x>519</x>
     <y>249</y>
    </hint>
   </hints>
  </connection>
  <connection>
   <sender>lineEdit</sender>
   <signal>textChanged(QString)</signal>
   <receiver>MainWindow</receiver>
   <slot>slot_send()</slot>
   <hints>
    <hint type="sourcelabel">
     <x>236</x>
     <y>267</y>
    </hint>
    <hint type="destinationlabel">
     <x>307</x>
     <y>256</y>
    </hint>
   </hints>
  </connection>
  <connection>
   <sender>lineEdit_2</sender>
   <signal>textChanged(QString)</signal>
   <receiver>MainWindow</receiver>
   <slot>slot_ID()</slot>
   <hints>
    <hint type="sourcelabel">
     <x>478</x>
     <y>269</y>
    </hint>
    <hint type="destinationlabel">
     <x>584</x>
     <y>275</y>
    </hint>
   </hints>
  </connection>
 </connections>
 <slots>
  <slot>slot_send()</slot>
  <slot>slot_receive()</slot>
  <slot>slot_contents()</slot>
  <slot>slot_ID()</slot>
  <slot>slot_pw()</slot>
 </slots>
</ui>

    
