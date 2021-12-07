import sys
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QWidget
from PyQt5 import uic
import pandas._libs.tslibs.base

import func
import openpyxl, os, sys, shutil
import openpyxl
import time
from PyQt5.QtCore import QObject
import threading

from datetime import datetime
import re, glob

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

import pandas as pd
from difflib import context_diff

g_feature_sheet = None
g_ref_folder = None
g_target_folder = None

g_progressBar = None
g_feature_name = None
g_feature_name_list = []

g_no = 0

ref_folder = './result/ref_folder'
target_folder = './result/target_folder'


def AutoFitColumnSize(worksheet, columns=None, margin=2):
    for i, column_cells in enumerate(worksheet.columns):
        is_ok = False
        if columns == None:
            is_ok = True
        elif isinstance(columns, list) and i in columns:
            is_ok = True
            
        if is_ok:
            length = max(len(str(cell.value)) for cell in column_cells)
            worksheet.column_dimensions[column_cells[0].column_letter].width = length + margin

    return worksheet


def MakeResultsFile():

    ref_file_lists = os.listdir(ref_folder)
    tar_file_lists = os.listdir(target_folder)

    file_lists = {'ref':ref_file_lists, 'target': tar_file_lists}

    df = pd.DataFrame(file_lists, columns = ['ref', 'target'])

    df['results']= 'NOK'
    df.loc[df['ref'] == df['target'], 'results'] = 'OK'

    no = 0
    nok_no = 0
    os.makedirs('./Result/', exist_ok= True)
    os.makedirs('./Result/NOK/REF/', exist_ok= True)
    os.makedirs('./Result/NOK/TARGET/', exist_ok= True)

    for x in df['results']:
        if x == 'NOK':
            file_r = df.iloc[no]['ref']
            file_t = df.iloc[no]['target']
            nok_no += 1

            shutil.copy('./Result/ref_folder/'+file_r, './Result/NOK/REF/'+file_r)
            shutil.copy('./Result/target_folder/'+file_t, './Result/NOK/TARGET/'+file_t)

        no+=1


    df.to_excel('results.xlsx', sheet_name='result')
    wb = openpyxl.load_workbook('results.xlsx')
    ws = wb.active
# ws.column_dimensions['B','C'].width = 70

    AutoFitColumnSize(ws)

    ws.auto_filter.ref = "A:D"
    wb.save('results.xlsx')

    shutil.move('results.xlsx', './Result/results.xlsx')



class Thread1(QThread): 
    threadEvent = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__()
        self.main = parent

    def is_allow_search(self, search_dir):
        if len(search_dir) >=4 and search_dir[1] == 'core' and search_dir[2] == 'mproc' and search_dir[3] == 'qmi':
            return True
        elif len(search_dir) >=3 and search_dir[1] == 'lge_product':
            return True
        elif search_dir[1] == 'geran' or search_dir[1] == 'wcdma':
            return True
        elif search_dir[1] == 'mmcp' or search_dir[1] == 'uim':
            return True
        elif search_dir[1] == 'datamodem':
            return True
        else:
            return False


    def find_feature(self, local_path,f1, feature):
        line_num = 0
        p = re.compile(feature)
        #1 - search
        for i in glob.glob(local_path, recursive=True):
            mylist = i.split('\\')
            # print(mylist)

            if self.is_allow_search(mylist) == False:    continue

            with open(i, 'r', encoding='UTF8', errors='ignore') as f:

                for x, y in enumerate(f.readlines(),1):
                    m = p.findall(y)
                    if m:
                #      print('File %s [ %d ] Line Searching : %s' %(i,x,m))
                        #print('File %s [ %d ] ' %(i,x))
                        # print(i)
                        # print('==>  %s' %y)
                        line_num += 1
                        # f1.write('File %s [ %d ] Line Searching : %s' %(i,x,m))
                        # f1.write('Full Line Text : %s' %y)
                        f1.write('File %s [ %d ] ' %(i,x))
                        f1.write('==> %s' %y)


        return line_num        

    def thread_search1(self, sheet1, folder, target_dir):
       # print(sheet1)

        global g_no
        
        feature_no = 0
        
        for x in range(2, sheet1.max_row):
            f1 = f'B{x}'
            f2 = f'C{x}'
            
            sheet1[f1].value= sheet1[f1].value
           
            print(sheet1[f1].value, sheet1[f2].value, feature_no)

            sheet1[f1].value = sheet1[f1].value.strip()
    
            if sheet1[f1].value == 'Modem' or sheet1[f1].value == 'Modme' or sheet1[f1].value == 'modem' or sheet1[f1].value == 'Data':
                feature_no += 1
                if sheet1[f2].value == None:
                    break
      #  print('feature no:', feature_no, )
        
        for x in range(2, sheet1.max_row):
            f1 = f'B{x}'
            f2 = f'C{x}'
         #   print(sheet1[f1].value)
            line_cnt = 0
          #  print("count : {}".format(x))

            sheet1[f1].value = sheet1[f1].value.strip()
            if sheet1[f1].value == 'Modem' or sheet1[f1].value == 'Modme' or sheet1[f1].value == 'modem' or sheet1[f1].value == 'Data' :
                f3 = sheet1[f2].value
                print(f3)

                with open(f3, 'w') as f1:
                    
                    # print("folder {} f1 {} f3 {}".format(folder, f1, f3))
                    line_cnt = self.find_feature(folder,f1, f3)
            
                
                t_dir = target_dir + f3 + '_'+str(line_cnt)
                # print(target_dir)
                if os.path.exists(t_dir) == False:
                    shutil.move(f3,t_dir)
                    
                
            #    print('g_target_folder:' , g_target_folder)
            #    print('g_ref_folder:', g_ref_folder)

                if g_ref_folder != None and g_target_folder != None:
                    mul = 2
                elif g_ref_folder != None or g_target_folder != None:
                    mul = 1
                
                g_no += 1
                # g_progressBar.setValue(no/max_val*100)
                self.threadEvent.emit(str(int(g_no/(mul*feature_no)*100)))
                
             #   print('1 send : ', str(int(g_no/(mul*feature_no)*100)))
            else:
             #   print('error', sheet1[f1].value)
             pass


    def thread_search2(self, feature_name_lists, folder, target_dir):
       # print(sheet1)
        global g_no
        if feature_name_lists == None:
            return

        for f3 in feature_name_lists:
            line_cnt = 0
            print(f3)

            with open(f3, 'w') as f1:
                line_cnt = self.find_feature(folder,f1, f3)
            
                
            t_dir = target_dir + f3 + '_'+str(line_cnt)
            # print(target_dir)
            if os.path.exists(t_dir) == False:
                shutil.move(f3,t_dir)

            if g_ref_folder != None and g_target_folder != None:
                mul = 2
            elif g_ref_folder != None or g_target_folder != None:
                mul = 1
                
            g_no += 1
            self.threadEvent.emit(str(int(g_no/(mul*len(feature_name_lists))*100)))

    def do_worker(self):

        if g_ref_folder != None:
            cwd = os.getcwd()
            os.makedirs(cwd+'\\Result\\ref_folder\\', exist_ok = True) 
            dir = cwd +'\\Result\\ref_folder\\'
            if g_feature_name != True :
                self.thread_search1(g_feature_sheet, g_ref_folder, dir)     
            else:
                self.thread_search2(g_feature_name_list, g_ref_folder, dir) 
        
        #print("ref ended !!!")
        # self.threadEvent.emit("ref end")
        
        if g_target_folder != None:
            cwd = os.getcwd()
            os.makedirs(cwd+'\\Result\\target_folder\\', exist_ok = True)            
            dir = cwd +'\\Result\\target_folder\\'
            if g_feature_name != True :
                self.thread_search1(g_feature_sheet, g_target_folder, dir)     
            else:
                self.thread_search2(g_feature_name_list, g_target_folder, dir)         
        #print("target ended !!!")
        # self.threadEvent.emit("target end")
        #self.threadEvent.emit(str(5/200*100))    
    def run(self): 
        #print("threading start")
        self.do_worker()

class MyForm(QWidget):

    def __init__(self, parent = None):
        global g_progressBar
       # QWidget.__init__(self)
        super().__init__(parent)
       # Ui_MainWindow, QtBaseClass = uic.loadUiType(BASE_DIR + r'\feature_check_v2.ui')
        self.ui = uic.loadUi('feature_check_v2.ui', self)
        #self.ui = uic.loadUi("feature_check_v2.ui", self)
        self.ref_selected = None
        self.target_selected = None
        self.ui.progressBar.setValue(0)
        g_progressBar = self.progressBar
        self.ui.show()

        self.th = Thread1(self)
        self.th.threadEvent.connect(self.threadEventHandler)  # custom signal from worker thread to main thread
        
               
    def slot_selectRefFolder(self):
        global g_ref_folder

        #print('slot_ref_folder()')
        self.ref_folder = QFileDialog.getExistingDirectory()+'/**/*.c'
        self.textBrowser.setPlainText(self.ref_folder)
        
        g_ref_folder = self.ref_folder
    
    def slot_selectTargetFolder(self):
        global g_target_folder

        #print('slot_target_folder()')
        self.target_folder = QFileDialog.getExistingDirectory()+'/**/*.c'
        self.textBrowser_2.setPlainText(self.target_folder)
       
        g_target_folder = self.target_folder

    def slot_exit(self):
      #  print('slot_exit()')
        sys.exit()
    
    def slot_start(self):
    #    print('slot_exit()')
        global g_feature_name
        global g_feature_name_list
        global g_no
        
        cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        mystr2 = self.textEdit.toPlainText()
        mystr2 = re.split(r'\s|\n', mystr2)
        mylist = pd.unique(mystr2).tolist()
        mylist = [ x for x in mylist if not x=='']
        g_feature_name_list = mylist.copy()

        if len(g_feature_name_list) > 0:
            g_feature_name = True

        g_no = 0
        
        print(mystr2, type(mylist),mylist, sep='\n')
        self.label_7.setText(cur_time)

        self.th.start()

    def slot_featureFile(self):
        global g_feature_sheet
        global g_feature_no

        file_name =  QFileDialog.getOpenFileName(self, 'Open file', './')
      #  print('slot_featureFile()', file_name , sep=' ')

        if re.search(r'xlsx', file_name[0]) == None:
            return 0
        self.textBrowser_3.setPlainText(file_name[0])
        wb = openpyxl.load_workbook(file_name[0]) 

        g_feature_sheet = wb.active 

    def slot_changed(self):
        print('slot_changed()')
        g_feature_name = True

        mystr2 = self.textEdit.toPlainText()
        mystr2 = re.split(r'\s|\n', mystr2)
        mylist = pd.unique(mystr2).tolist()
        mylist = [ x for x in mylist if not x=='']
        
        self.label_9.setText('Feature - {}'.format(len(mylist)))

    def slot_makeResult(self):
        MakeResultsFile()
    

    def threadEventHandler(self, mystr):
      #  print("1 Recevied Thread: ", mystr)
        ptg = int(mystr)
        self.progressBar.setValue(ptg)
   #     print("2 Recevied Thread", ptg)
        cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.label_8.setText(cur_time)

    
app = QApplication(sys.argv)
w = MyForm()
w.show()
sys.exit(app.exec())
