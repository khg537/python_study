import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import re

import requests
import bs4

def crawling(code_in):
    my_header = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    }

    r = requests.get(
        "https://finance.naver.com/item/main.nhn?code={}".format(code_in), headers=my_header
        )
  
    bs= bs4.BeautifulSoup(r.text, "lxml")
    tr_elements= bs.select("dl.blind")
    disp_str = ""
    for tr_element in tr_elements:
        print(tr_element)
        disp_str += tr_element.text
    
    return disp_str

def name2code(name_in):
    name2in_table = {
        'sk케미칼' : '285130',
        '메지온': '140410'
    }
    
    return name2in_table[name_in]


form_class = uic.loadUiType("stock.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        
        super().__init__()
        self.setupUi(self)
    
    def slot_text(self, my_str):
        print(my_str)
        
    def slot_get(self):
        in_val = name2code( self.code_in)
        print(in_val)
        str = crawling(in_val )
        print(str)
        regx = re.compile(r'현재가 [0-9]+[,][0-9]+')
        current_value  =regx.search(str).group()
        regx = re.compile('[0-9]+,[0-9]+')
        m = regx.search(current_value).group()
        self.textBrowser.setText(m)
        
        regx= re.compile('[0-9]+년 [0-9]+월 [0-9]+일 [0-9]+시 [0-9]+분')
        m = regx.search(str).group()
        self.label_time.setText(m)
        
    def slot_name(self):
        self.code_in = self.plainTextEdit.toPlainText()
        
        
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()