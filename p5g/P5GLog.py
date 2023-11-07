import os
import sys
import pandas as pd
import datetime
import time

import re

class PLog:
    def __init__(self, dir_path=None, file_list = None):
        self.df = None
        self.dir = None
        self.file_list = None
        self.Msg_list = []

    def validate_date(self, date_text):
        try:
            datetime.datetime.strptime(date_text,'%H:%M:%S.%f')
            return True
        except ValueError:
            # print("Incorrect data format({0}), should be YYYY-MM-DD".format(date_text))
            return False
        
    def separate_data(self, line_data):
        pattern1 = r'\d{2}:\d{2}:\d{2}.\d{6}' 

        # Use re.search to find the first match in the input string

        try:
                # Use re.search to find the first match in the input string
                match = re.search(pattern1, line_data)

                return match.group(0), line_data
        except:
                return None, None
        
    def extract_date(self, text):
        #pattern = r'\[(\d{4}-\d{2}-\d{2}/\d{2}:\d{2}:\d{2}.\d{3})\]'
        pattern = r'\d{4}-\d{2}-\d{2}/(\d{2}:\d{2}:\d{2}.\d{3})' 

        # Use re.search to find the first match in the input string
        match = re.search(pattern, text)

        # Check if a match was found
        if match:
            timestamp = match.group(1)
            print("Extracted timestamp:", timestamp)
        else:
            print("No timestamp found in the input string.")
        
        return timestamp   
        

    # def change_df(self, file_path):
    #     out_lists = []
    #     with open(file_path) as rfile:
    #         try:
    #             lines = rfile.readlines()
    #             for line in lines:
    #                 line_split = line.split(' ',1)
    #                 # print(line_split)
    #                 temp_date = self.extract_date(line_split[0])
    #                 if self.validate_date(temp_date):
    #                         out_lists.append(line_split)
    #         except:
    #           print("reade error")

    #     self.df = pd.DataFrame(out_lists)

    def add(self, dir_path, file_list = None):
        if dir_path != None:   self.dir = dir_path
        if file_list != None:  self.file_list = file_list


    def MergeFile(self):
        dflists = []
        
        if self.dir != None: 
            for (root, directories, files) in os.walk(self.dir):

                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.getsize(file_path) > 0:
                        df = self.MakeDF(file_path)
                        print(df)
                        if df.size >0:
                            dflists.append(df)
        
        if self.file_list != None:               
            for file_path in self.file_list:
                df = self.MakeDF(file_path)
                print(df)
                if df.size >0:
                     dflists.append(df)
                
        if self.file_list == None and self.dir == None: return  pd.DataFrame()

        if len(dflists) > 0: dflists = pd.concat(dflists)

        # dflists=dflists.apply(lambda x:x.str.strip(), axis=1)

        dflists.columns = ['time', 'value']
        dflists['time'] = pd.to_datetime(dflists['time'], format='%H:%M:%S.%f').dt.time
     
        dflists = dflists.sort_values(by='time')

        # dflists['time'] = dflists['time'].dt.time

        dflists['value'] = dflists['value'].apply(lambda x : "\n".join([x for x in x]))
     
        return dflists

    def MakeDF(self, file_path):
        out_lists = []
        cont_list = []
        ongoing = False
        
    #    check_message = False
        with open(file_path) as rfile:
            try:
                lines = rfile.readlines()

                i = 0
                for line in lines:
                    i +=1
                    line = line.rstrip()
                    # print(i, line, sep=" ")
                    if ongoing == True and not line:
                        ongoing = False
                        
                        out_lists.append([time_p, cont_list])
                        # print(out_lists)
                        cont_list = []

                    if not line:
                        # print("blank")
                        continue       
                   
                    time_part,  content_part = self.separate_data(line)
                    
                    if ongoing == False and not time_part:
                        continue
                   
                    if ongoing != False:
                        cont_list.append( line)
                    else:
                    
                        if self.CheckMessage(line):
                            ongoing = True
                            time_p =  time_part
                            cont_list.append(content_part)
                        else:
                            time_p =  time_part
                            cont_list.append( content_part)
                            out_lists.append([time_p, cont_list])                        
                            cont_list = []


            except:
                print("reader error")    

        # for out_list in out_lists:
        # print(out_lists[15228])

        df = pd.DataFrame(out_lists)
        return df


    # list_df = pd.concat(list_df)

    # list_df=list_df.apply(lambda x:x.str.strip(), axis=1)

    # list_df.columns = ['time', 'value']
    # print(list_df.head())
    # list_df['time'] = pd.to_datetime(list_df['time'])
    # list_df = list_df.sort_values(by='time')
    # list_df['time'] = list_df['time'].dt.time

    # list_df.info()
    # list_df.to_csv('out.txt', sep='\t', index=False) 
    
    def CheckMessage(self, line):
        messages = [ 'asn1PrtToStr_']

        for message in messages:
            if message in line:
                return True
                break
                
        else: return False

    def print_path(self):
        print("dir", self.dir)
        print("file_path", self.file_list)
        
    def clear_file(self):
        self.df = None
        self.dir = None
        self.file_list = None
        
    def get_files(self):
        filelist = []
        if self.dir != None: 
            for (root, directories, files) in os.walk(self.dir):

                for file in files:
                    file_path = os.path.join(root, file)
                    print(file_path)
                    filelist.append(file_path)
        
        if self.file_list != None:               
            for file_path in self.file_list:
                filelist.append(file_path)
                
        
        return filelist 

    def MakeMessage(self):
        time_list =[]
        
        if self.dir != None: 
            for (root, directories, files) in os.walk(self.dir):

                for file in files:
                    file_path = os.path.join(root, file)
                    print(file_path)
                    if os.path.getsize(file_path) > 0:
                        #  print(file_path)
                        self.MakeMsgList(file_path)

        
        if self.file_list != None:               
            for file_path in self.file_list:
                self.MakeMsgList(file_path)

        len_glist = len(self.Msg_list)
        for i in range(len_glist):
            for j in range(len(self.Msg_list[i])):
            # print(glist[i][j])
                if j == 0:
                    time_split = self.Msg_list[i][j].split(' ',1)
                    time_list.append(time_split[0])        

        df = pd.DataFrame(zip(time_list, self.Msg_list))
         
        return df
  
    def MakeMsgList(self, file_path):
        result=[]
        ongoing = False
        print(file_path)
        with open(file_path) as rfile:
            try:
                lines = rfile.readlines()
                # print(lines)
                for line in lines:
                    line = line.rstrip('\n')
                    # print(line)                    
                    if ongoing == True:
                        if not line:
                            ongoing = False
                            self.Msg_list.append(result)
                            result = []
                            continue

                        result.append(line)

       
                    if self.CheckMessage(line):
                        print("checkmessage")
                        result.append(line)
                        ongoing = True

            except:
                pass        
        
     
