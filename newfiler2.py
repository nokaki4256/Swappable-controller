"""
# Window key events
"""
import TkEasyGUI as eg

import pandas as pd
import glob

import shutil

import csv

import time

def key_select(press):

    column = 0
    row = 0
        
    if press == "Up":
        column = column + 1
    elif press == "Down":
        column = column - 1
    elif press == "Right":
        row = row + 1
    elif press == "Left":
        row = row - 1
    else:
        pass
    
    return column, row

def make_csv(file_list, header, default):

    flag = 0
    boolian = False
    i = 0
    
    #新規ファイルの作成
    while boolian == False:
    
        csv_name = eg.popup_get_text("新規CSVファイルの名称")
        unit_name = csv_name
        default[0][8] = unit_name
        print(default)
            
        try:
            csv_name = csv_name + ".csv"
            
            for i in range(len(file_list)):
                if csv_name == file_list[i]:
                    flag = 0
                    break
                elif csv_name != file_list[i]:
                    flag = 1
            if flag == 1:
                eg.popup("作成可能しますた:" + csv_name)
                boolian = True
                
            elif flag == 0:
                eg.popup("上書きはお控えください") 
                boolian = False

        except TypeError:
            break
        
        try:
            #CSVファイルの新規作成
            #asの後ろのfileは名称自由かも
            with open(csv_name, "w", newline = "") as file:
                writer = csv.writer(file)
                
                #ヘッダーの書き込み　１行目１、２列目
                writer.writerow(header)
                
                #データ書き込み
                writer.writerows(default)

            print("作成されたファイル確認")
            read_data = csv_name
            #CSVデータの読み出し
            with open(read_data) as file:
                print(file.read())
                
            shutil.move(read_data,"dataset")
        
        except TypeError:
            break

def new_dataset():
    filepath = "/home/cells/control"
    csv_list = glob.glob("*.csv",root_dir = "dataset")

    cursor_dict = {"Up":"select", "Down":"select", "Right":"select", "Left":"select"}

    #aはalpha bはbeta
    header = ["P","I","D","a","b","motor_limit","Pulse_width","Home_Position","ユニット名","リンクの長さ"]
    default = [[0.0,0.0,0.0,0.0,0.0,0.0,    0,  0.0,"new",0.0],
               [0.0,0.0,0.0,0.0,0.0,0.0,"Non",  0.0,"Non",0.0],
               [0.0,0.0,0.0,0.0,0.0,0.0,"Non",  0.0,"Non",0.0],
               [0.0,0.0,0.0,0.0,0.0,0.0,"Non","Non","Non",0.0],
               [0.0,0.0,0.0,0.0,0.0,0.0,"Non","Non","Non",0.0],
               [0.0,0.0,0.0,0.0,0.0,0.0,"Non","Non","Non",0.0]
               ]

    make_csv(csv_list,header,default)

#new_dataset()