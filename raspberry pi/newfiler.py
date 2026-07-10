"""
# Window key events
"""
import TkEasyGUI as eg

import pandas as pd
import glob

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
        
        except TypeError:
            break

def main_window():

    #ボタンの場合ボタンがイベントとして返す キーを設定すればキーを返す
    layout = [[eg.Frame("Main Selsct",[[eg.Button("PIDのテンプレート",key = "PID")],
                                       [eg.Button("パルス幅のテンプレート",key = "Pulse")],
                                       [eg.Button("ホームポジションのテンプレート",key = "Home")],
                                       [eg.Button("モータ出力リミットのテンプレート",key = "limit")],],),
                eg.Frame("操作説明画面",
                         [[eg.Text("操作説明")],
                        [eg.HSeparator()],
                        [eg.Text("Tab:選択画面のボタンを選択")],
                        [eg.Text("Return:選択したボタンの内容を選択")],
                        [eg.Text("[ESC]:終了")],],),],]
        
    return eg.Window('Window key test', layout,enable_key_events=True)


def newfile():
    filepath = "/home/cells/control"
    csv_list = glob.glob("*.csv")

    cursor_dict = {"Up":"select", "Down":"select", "Right":"select", "Left":"select"}

    #aはalpha bはbeta
    PID_header = ["P","I","D","a","b"]
    PID_default = [[0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0]]
    
    Pulse_width_header = ["Pulse_width"]
    Pulse_width_default = [0]

    Home_header = ["Home_Position"]
    Home_default = [[0.0],[0.0],[0.0],[0.0],[0.0],[0.0]]
    
    limit_header = ["motor_limit"]
    limit_default = [[0.0],[0.0],[0.0],[0.0],[0.0],[0.0]]
    
    window = main_window()
    key_press = ""
    miss_key = ""
    # event loop
    while True:
        event, values = window.read()

        #print(event)
        #print(values)
        if values["event_type"] == "key":
            print(values["key"])
            key_press = values["key"]
            
            try:
                print(cursor_dict[key_press])
            except KeyError:
                miss_key = "矢印以外"
                selected2 = miss_key
                #window["-text-"].update(text=selected2)
            else:
                #矢印入力
                key_select(key_press)
                miss_key = ""
                selected2 = miss_key
                #window["-text-"].update(text=selected2)
                
        if event == "PID":
            print("PIDのテンプレート")
            make_csv(csv_list,PID_header,PID_default)
        elif event == "Pulse":
            eg.popup("未実装,パルス幅はCSVで管理していません") 
        #    print("パルス幅のテンプレート")
        #    make_csv(csv_list,Pulse_width_header,Pulse_width_default)
        elif event == "Home":
            print("ホームポジションのテンプレート")
            make_csv(csv_list,Home_header,Home_default)
        elif event == "limit":
            print("モータ出力リミットのテンプレート")
            make_csv(csv_list,limit_header,limit_default)
        
        #print(values["event_type"])
        if event == eg.WIN_CLOSED or key_press == "Escape":
            break

    window.hide()
