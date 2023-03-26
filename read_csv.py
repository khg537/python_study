#!/bin/python3
import os
import pandas as pd

folder_path = "/home/k8s/work/Altran_src/20221020/5G_IPR/gNB_SW/gNB_O1_hdl/csv"
file_paths = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path)]

# 파일 이름과 경로 출력
df = pd.DataFrame()

for file_path in file_paths:
    new_df = pd.read_csv(file_path)
    df = df.append(new_df, ignore_index = True)

print(df.head())
