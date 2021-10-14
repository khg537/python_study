import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import re

form_class = uic.loadUiType("eng_dict.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        
        super().__init__()
        self.setupUi(self)
    
    def slot_text(self, my_str):
        print(my_str)
        
    def slot_find():
        run_dict()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()