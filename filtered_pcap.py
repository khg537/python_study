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
from scapy.all import *
import time
import datetime
from PyQt5.QtCore import QDateTime
import shutil

form_class = uic.loadUiType("filtered_pcap.ui")[0]   

class time_struct():
    tm_year=0.0
    tm_mon=0.0
    tm_mday=0.0
    tm_hour=0.0
    tm_min=0.0
    tm_sec=0.0
    def toString(self):
        return str(self.tm_year) +"-" + str(self.tm_mon) +"-" + str(self.tm_mday) +"_" + str(self.tm_hour) +":" + str(self.tm_min) +":" + str(self.tm_sec)
    def toSimpleString(self):
        return str(self.tm_mday) +"-" + str(self.tm_hour) +"-" + str(self.tm_min) +"-" + str(self.tm_sec)
    
class MyWindow(QMainWindow, form_class):
    def __init__(self):
        
        super().__init__()
        self.setupUi(self)
        self.threadclass = ThreadClass() 
        self.fname = None
        
        self.s_tm = None
        self.e_tm = None
        
        self.s_tm2 = None
        self.e_tm2 = None
        self.dict_var4 = dict()
        self.dict_var6 = dict()
        
        self.pushButton.clicked.connect(self.slot_file_sel)
        self.btn_save.clicked.connect(self.slot_save)
        self.btn_load.clicked.connect(self.slot_load)
        
    def slot_file_sel(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', "",
                                        "All Files(*);; log Files(*.log)", '/home')
        print(file_name[0])
        self.label_file_name.setText(file_name[0])       
        self.fname =file_name[0]
        self.orig_file_load()
        
    def orig_file_load(self):
        self.pkts = rdpcap(self.fname) 
        self.pkt_len = len(self.pkts )

        s_tm1 = time.localtime(float(self.pkts [0].time))
        e_tm1 = time.localtime(float(self.pkts [self.pkt_len-1].time))
        
        self.s_tm = s_tm1
        self.e_tm = e_tm1
        
        # 현재 파일에서 읽은 값
        self.dTimeEdit_From.setDateTime(QDateTime(s_tm1.tm_year, s_tm1.tm_mon, s_tm1.tm_mday, s_tm1.tm_hour, s_tm1.tm_min, s_tm1.tm_sec))
        self.dTimeEdit_To.setDateTime(QDateTime(e_tm1.tm_year, e_tm1.tm_mon, e_tm1.tm_mday, e_tm1.tm_hour, e_tm1.tm_min, e_tm1.tm_sec))
        
        # self.display_analyze()   
    def slot_save(self):
        self.s_tm2, self.e_tm2 = self.convert_time(self.dTimeEdit_From.dateTime(),self.dTimeEdit_To.dateTime() )
        i = 0
        lname = self.s_tm2.toSimpleString() + "_" +self.e_tm2.toSimpleString()
        for pkt in self.pkts:
            tmp_tm = time.localtime(float(pkt.time))
            if self.time_filter_pkt(tmp_tm, self.s_tm2, self.e_tm2) == True:
                i +=1
                wrpcap('./filtered.pcap', pkt, append=True) 
                
        self.pkt_len = i
        shutil.move("./filtered.pcap", lname+".pcap")
    def slot_load(self):
        # self.s_tm2 = self.dTimeEdit_From.dateTime()
        # self.e_tm2 = self.dTimeEdit_To.dateTime()
        self.textBrowser.clear()
        self.dict_var4.clear()
        self.dict_var6.clear()       
        
        self.s_tm2, self.e_tm2 = self.convert_time(self.dTimeEdit_From.dateTime(),self.dTimeEdit_To.dateTime() )

   #     print(self.s_tm2.toString("yyyy-MM-dd hh:mm:ss"))
        i =0
        for pkt in self.pkts:
            tmp_tm = time.localtime(float(pkt.time))
            if self.time_filter_pkt(tmp_tm, self.s_tm2, self.e_tm2) == True:
                   
                if self.cb_dns_q4.isChecked() == True and self.cb_dns_q6.isChecked() == False:
                    if pkt.getlayer('DNS'): self.dns_analyzer(pkt, 1)
                    
                if self.cb_dns_q4.isChecked() == False and self.cb_dns_q6.isChecked() == True:
                    if pkt.getlayer('DNS'): self.dns_analyzer(pkt, 2)
                    
                if self.cb_dns_q4.isChecked() == True and self.cb_dns_q6.isChecked() == True:
                    if pkt.getlayer('DNS'): self.dns_analyzer(pkt, 3)
                    
                i+=1
   
        self.s_tm, self.e_tm = self.s_tm2, self.e_tm2
        self.pkt_len = i
              

        self.display_analyze()
  
    def dns_analyzer(self, pkt, flag):
           
        if pkt.getlayer('DNS') and pkt.getlayer('DNS').opcode == 0 and  pkt.getlayer('DNS').qr==0 :
            if pkt.getlayer('DNS').qd.qtype == 1:
                query = pkt['DNS'].qd.qname
                dns_name = query.decode('utf-8').rstrip('.')
                print(dns_name)
                if not dns_name in self.dict_var4:
                    self.dict_var4[dns_name] = 1
                else:
                    self.dict_var4[dns_name] += 1
            elif pkt.getlayer('DNS').qd.qtype == 28:
                query = pkt['DNS'].qd.qname
                dns_name = query.decode('utf-8').rstrip('.')
                print(dns_name)
                if not dns_name in self.dict_var6:
                    self.dict_var6[dns_name] = 1
                else:
                    self.dict_var6[dns_name] += 1
                
               
    def display_analyze(self):
        self.textBrowser.clear()
        self.textBrowser.setText("Packet Count :" + str(self.pkt_len))

        self.textBrowser.append(f"\nFrom :  {self.s_tm.tm_year}-{self.s_tm.tm_mon}-{self.s_tm.tm_mday} {self.s_tm.tm_hour}:{self.s_tm.tm_min}:{ self.s_tm.tm_sec}")
        self.textBrowser.append(f"To     :  {self.e_tm.tm_year}-{self.e_tm.tm_mon}-{self.e_tm.tm_mday} {self.e_tm.tm_hour}:{self.e_tm.tm_min}:{ self.e_tm.tm_sec}")      
        
        if self.cb_dns_q4.isChecked() == True and self.cb_dns_q6.isChecked() == False:
            self.textBrowser.append("\n<< The Result of IPV4 DNS QUERY >> \n")
            for m in self.dict_var4.items():
                disp_str = m[0] +str("  ") + str(m[1])
                self.textBrowser.append(disp_str)
        elif self.cb_dns_q4.isChecked() == False and self.cb_dns_q6.isChecked() == True:
            self.textBrowser.append("\n<< The Result of IPV6 DNS QUERY >> \n")
            for m in self.dict_var6.items():
                disp_str = m[0] +str("  ") + str(m[1])
                self.textBrowser.append(disp_str)
        elif self.cb_dns_q4.isChecked() == True and self.cb_dns_q6.isChecked() == True:
            self.textBrowser.append("\n<< The Result of IPV4 DNS QUERY >> \n")
            for m in self.dict_var4.items():
                disp_str = m[0] +str("  ") + str(m[1])
                self.textBrowser.append(disp_str)
            
            self.textBrowser.append("\n<< The Result of IPV6 DNS QUERY >> \n")
            for m in self.dict_var6.items():
                disp_str = m[0] +str("  ") + str(m[1])
                self.textBrowser.append(disp_str)
        
    def time_filter_pkt(self, in_time, s_time, e_time):
        
        if in_time.tm_year > e_time.tm_year or in_time.tm_mon > e_time.tm_mon:
            return False
        
        if in_time.tm_year < s_time.tm_year or in_time.tm_mon < s_time.tm_mon:
            return False
        
        full_in_time = in_time.tm_sec + in_time.tm_min*60 +in_time.tm_hour*60*60 + in_time.tm_mday*60*60*24
        full_s_time = s_time.tm_sec + s_time.tm_min*60 +s_time.tm_hour*60*60 + s_time.tm_mday*60*60*24
        full_e_time = e_time.tm_sec + e_time.tm_min*60 +e_time.tm_hour*60*60 + e_time.tm_mday*60*60*24

        if full_in_time >= full_s_time and full_in_time <= full_e_time:
            return True
        
    def convert_time(self, s_time, e_time):
        tmp1_format = time_struct()
        tmp2_format = time_struct()
        
        tmp = s_time.toString("yyyy-MM-dd hh:mm:ss")
        tmp_date, tmp_time = tmp.split(" ")
        
        tm_year, tm_mon, tm_mday = tmp_date.split("-")
        tm_hour, tm_min, tm_sec = tmp_time.split(":")
        
        tmp1_format.tm_year = int(tm_year)
        tmp1_format.tm_mon = int(tm_mon)
        tmp1_format.tm_mday = int(tm_mday)
        
        tmp1_format.tm_hour = int(tm_hour)
        tmp1_format.tm_min = int(tm_min)
        tmp1_format.tm_sec = int(tm_sec)
        
        tmp = e_time.toString("yyyy-MM-dd hh:mm:ss")
        tmp_date, tmp_time = tmp.split(" ")
        
        tm_year, tm_mon, tm_mday = tmp_date.split("-")
        tm_hour, tm_min, tm_sec = tmp_time.split(":")
        
        tmp2_format.tm_year = int(tm_year)
        tmp2_format.tm_mon = int(tm_mon)
        tmp2_format.tm_mday = int(tm_mday)
        
        tmp2_format.tm_hour = int(tm_hour)
        tmp2_format.tm_min = int(tm_min)
        tmp2_format.tm_sec = int(tm_sec)
        
        return tmp1_format, tmp2_format
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
