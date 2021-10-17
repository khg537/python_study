import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import re
from googletrans import Translator
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import re

import requests
import bs4

form_class = uic.loadUiType("trans.ui")[0]

def GetText(word_in):
 
    my_header = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    }

    r = requests.get(
        "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={}".format(word_in), headers=my_header
        )
  
    bs= bs4.BeautifulSoup(r.text, "lxml")
    return bs

def GetText_Ko(word_in):
    my_header = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
        }

    r = requests.get(
        "https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&sq=&o=&q={}".format(word_in), headers=my_header
        )
  
    bs= bs4.BeautifulSoup(r.text, "lxml")

    dic_elements = bs.find_all("dl",{"class":"dl_comm clear"})

    rslt_list = []
    for i in dic_elements:
        r = i.find_all("span")
        for i in r:
            print(i.text)
            rslt_list.append(i.text.strip())
            
    return rslt_list

def GetMeaning(bs):
    name_list = bs.find_all("p", {"class":"mean api_txt_lines"})
    rslt_list =[]
    for name in name_list:
        print(name.text)
        rslt_list.append(name.text)
        
    return rslt_list
        
def GetExample(bs):
    all = bs.select("div.example")
    exam = re.compile(r'data-tts-text="(.+\.)\"')
    rslt_list = []
    for a in all:    
        r = exam.search(str(a))   
        if r!=None:
            print(r.group(1))
            rslt_list.append(r.group(1))
        
        p= a.select("p.text_mean")       
        print(p[0].text)
        rslt_list.append(p[0].text)
    return rslt_list
    

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        
        super().__init__()
        self.setupUi(self)
        self.textEdit_ko.setText("")
        self.textEdit_en.setText("")
        self.en = None
        self.ko = None
        self.lang = None
        self.word = False
        self.radioButton_2.setChecked(False)
        self.radioButton.setChecked(True)
        
    def slot_toEn(self):
        print(self.ko)
        if self.word == False:
            self.translator2en()
            self.textEdit_en.setText(self.lang)
        else:
            print(self.ko)
            rslt = GetText_Ko(self.ko)
            print(rslt)
            
            self.textEdit_en.clear()
 
            for e in rslt:
                self.textEdit_en.append(e)
    
    def slot_toKo(self):
        if self.word == False:
            self.translator2ko()
            self.textEdit_ko.setText(self.lang)
        else:
            print(self.en)
            bs = GetText(self.en)
            mean_list = GetMeaning(bs)
            exam_list = GetExample(bs)
            self.textEdit_ko.clear()
            
            self.textEdit_ko.append("<< 뜻 >>")
            i = 0
            for e in mean_list:
                i += 1
                self.textEdit_ko.append("{} ".format(i) + e)
            self.textEdit_ko.append('\n') 
            self.textEdit_ko.append("<< 예문 >>")
          
            for e in exam_list:  
                self.textEdit_ko.append(e)
                
            
    
    def slot_getEn(self):
        self.en = self.textEdit_en.toPlainText()
    
    def slot_getKo(self):
        self.ko = self.textEdit_ko.toPlainText()    
        
    def slot_word(self, is_word):
        print(is_word)
        self.word = is_word
        
    def slot_statement(self, is_statement):
        print(is_statement)
        
    def slot_clear(self):
        self.textEdit_ko.clear()
        self.textEdit_en.clear()
        
        
    def translator2ko(self):
        translator = Translator(service_urls=['translate.googleapis.com'])
        self.lang = translator.translate(self.en, dest='ko').text
        
    def translator2en(self):
        translator = Translator(service_urls=['translate.googleapis.com'])
        self.lang = translator.translate( self.ko, dest='en').text
        
    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()