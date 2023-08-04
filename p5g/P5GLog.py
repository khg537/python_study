import os
import sys
import pandas as pd
import datetime
import time

class PLog:
    def __init__(self, dir_path=None, file_list = None):
        self.df = None
        self.dir = None
        self.file_list = None

    def validate_date(self, date_text):
        try:
            datetime.datetime.strptime(date_text,'%H:%M:%S.%f')
            return True
        except ValueError:
            print("Incorrect data format({0}), should be YYYY-MM-DD".format(date_text))
            return False

    def change_df(self, file_path):
        out_lists = []
        with open(file_path) as rfile:
            try:
                lines = rfile.readlines()
                for line in lines:
                    line_split = line.split(' ',1)
                    # print(line_split)
                    if self.validate_date(line_split[0]):
                            out_lists.append(line_split)
            except:
              print("reade error")

        self.df = pd.DataFrame(out_lists)

    def add(self, dir_path, file_list = None):
        if dir_path != None:   self.dir = dir_path
        if file_list != None:  self.file_list = file_list


    def MergeFile(self):
        dflists = []
        for (root, directories, files) in os.walk(self.dir):
            for file in files:
                file_path = os.path.join(root, file)
                print(file_path)
                if os.path.getsize(file_path) > 0:
                    #  print(file_path)
                     df = self.MakeDF(file_path)
                     print(df.size)
                     if df.size >0:
                         dflists.append(df)
        print(dflists)

        dflists = pd.concat(dflists)

        dflists=dflists.apply(lambda x:x.str.strip(), axis=1)

        dflists.columns = ['time', 'value']
        print(dflists.head())
        dflists['time'] = pd.to_datetime(dflists['time'])
        dflists = dflists.sort_values(by='time')
        dflists['time'] = dflists['time'].dt.time

        return dflists

    def MakeDF(self, file_path):
        out_lists = []
        print("makedef", file_path)
        with open(file_path) as rfile:
            try:
                lines = rfile.readlines()
                # print(lines.size)
                for line in lines:
                    # print(line)
                    line_split = line.split(' ',1)
                    # print(line_split[0])
                    if self.validate_date(line_split[0]):
                    #    print(line_split[0])
                       out_lists.append(line_split)
            except:
               print("reade error")    

        # for out_list in out_lists:
        #     print(out_list)

        df = pd.DataFrame(out_lists)
        return df


    def validate_date(self, date_text):
        try:
            datetime.datetime.strptime(date_text,'%H:%M:%S.%f')
            return True
        except ValueError:
            # print("Incorrect data format({0}), should be YYYY-MM-DD".format(date_text))
            return False


    # list_df = pd.concat(list_df)

    # list_df=list_df.apply(lambda x:x.str.strip(), axis=1)

    # list_df.columns = ['time', 'value']
    # print(list_df.head())
    # list_df['time'] = pd.to_datetime(list_df['time'])
    # list_df = list_df.sort_values(by='time')
    # list_df['time'] = list_df['time'].dt.time

    # list_df.info()
    # list_df.to_csv('out.txt', sep='\t', index=False) 

    def print_path(self):
        print("dir", self.dir)
        print("file_path", self.file_list)


