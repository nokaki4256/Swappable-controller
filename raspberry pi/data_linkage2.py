"""
# Window key events
"""
import TkEasyGUI as eg

import pandas as pd
import glob

import csv

import time

import newfiler2

def key_select(press):

    column = 0
    row = 0
        
    if press == "Up":
        column = column - 1
    elif press == "Down":
        column = column + 1
    elif press == "Right":
        row = row + 1
    elif press == "Left":
        row = row - 1
    else:
        pass
    
    return column, row

def main_window(List):
    
    #ボタンの場合ボタンがイベントとして返す キーを設定すればキーを返す
    layout = [[eg.Frame("List Selsct",[[eg.Listbox(List,key="-listbox-",size =(100,5),
                                        enable_events=True, default_value=List[0],
                                        select_mode=eg.LISTBOX_SELECT_MODE_EXTENDED)],
                                        [eg.Text("-", key="-listtext-")],
                                        [eg.Text(key="csv")],
                                        [eg.Text("-", key="-text-")],],),
                eg.Frame("操作説明画面",
                         [[eg.Text("操作説明")],
                        [eg.HSeparator()],
                        [eg.Text("矢印で選択")],
                        [eg.Text("エンターで選択")],
                        [eg.Text("[ESC]:終了")],],),],]
        
    return eg.Window('Window key test', layout,enable_key_events=True,enable_events=True)


def sub_window(List):
    layout = [[eg.Frame("List Selsct",[[eg.Listbox(List,key="-listbox-",
                                            enable_events=True, default_value=List[0],
                                            select_mode=eg.LISTBOX_SELECT_MODE_EXTENDED)],
                                            [eg.Text("-", key="-listtext-")],
                                            [eg.Text(key="csv")],
                                            [eg.Text("-", key="-text-")],],),
                    eg.Frame("操作説明画面",
                         [[eg.Text("操作説明")],
                        [eg.HSeparator()],
                        [eg.Text("矢印で選択")],
                        [eg.Text("エンターで選択")],
                        [eg.Text("[ESC]:終了")],],),],]
    
    return eg.Window('Window key test', layout,enable_key_events=True,enable_events=True)

def change_dataset():
    dataset_list = glob.glob("*.csv",root_dir = "dataset")
    
    cursor_dict = {"Up":"select", "Down":"select", "Right":"select", "Left":"select"}

    window = sub_window(dataset_list)
    
    key_press = ""
    miss_key = ""
    data_column = 0
    # event loop

    while True:
        event, values = window.read()

        if event == eg.WIN_CLOSED or key_press == "Escape":
            break

        if values["event_type"] == "select":
            print("紐付けデータの選択")
            
        elif values["event_type"] == "key":
            print(values["key"])
            key_press = values["key"]
            
            try:
                print(cursor_dict[key_press])
            except KeyError:
                miss_key = "矢印以外"
                selected2 = miss_key
                window["-text-"].update(text=selected2)
            else:
                #矢印入力
                #データの選択はデータセットの選択だけに変更
                _column, _row = key_select(key_press)

                miss_key = ""
                selected2 = miss_key
                window["-text-"].update(text=selected2)

                                        
                data_column = data_column + _column
                if data_column > len(dataset_list) - 1:
                    data_column = 0
                elif data_column < 0:
                    data_column = len(dataset_list) - 1

                selected = dataset_list[data_column]
                window["-listtext-"].update(text=selected)
                dataset_select_data = "Select dataset:" + str(dataset_list[data_column])
                window["csv"].update(text=dataset_select_data)
                print(str(dataset_list[data_column]))
                
        if event == eg.WIN_CLOSED or key_press == "Escape":
            key_press = ""
            event = ""
            window.hide()
                
            window = main_window(csv_list_data)
            break
        
        if key_press == "Return":
            
            window.hide()
            return str(dataset_list[data_column])

def linkage2():
    
    cursor_dict = {"Up":"select", "Down":"select", "Right":"select", "Left":"select"}

    
    linkage_csv = "tester_linkage.csv"
    csv_data = pd.read_csv("tester_linkage.csv")
    
    csv_col, csv_row = csv_data.shape
    #CSVをリストデータとして読み込み
    csv_list_data = pd.read_csv(linkage_csv).values.tolist()
    
    #CSV内の１６進は取り込んでも変換されないっぽい
    if csv_list_data[0][1] == "0x30":
        print(0x30)
    if csv_list_data[2][1] == "0x31":
        print(0x31)
    if csv_list_data[1][1] == "0x32":
        print(0x32)
    window = main_window(csv_list_data)
    
    data_row = 2
    data_column = 0
    
    key_press = ""
    miss_key = ""
    # event loop

    while True:
        event, values = window.read()

        if event == eg.WIN_CLOSED or key_press == "Escape":
            break

        if values["event_type"] == "select":
            print("紐付けデータの選択")
            
        elif values["event_type"] == "key":
            print(values["key"])
            key_press = values["key"]
            
            try:
                print(cursor_dict[key_press])
            except KeyError:
                miss_key = "矢印以外"
                selected2 = miss_key
                window["-text-"].update(text=selected2)
            else:
                #矢印入力
                #データの選択はデータセットの選択だけいに変更
                _column, _row = key_select(key_press)

                miss_key = ""
                selected2 = miss_key
                window["-text-"].update(text=selected2)
                                        
                data_column = data_column + _column
                if data_column > csv_col - 1:
                    data_column = 0
                elif data_column < 0:
                    data_column = csv_col - 1

                selected = csv_list_data[data_column][0]
                window["-listtext-"].update(text=selected)
                csv_select_data = "Select dataset:" + str(csv_list_data[data_column][data_row])
                window["csv"].update(text=csv_select_data)
                
        if event == eg.WIN_CLOSED or key_press == "Escape":
            key_press = ""
            event = ""
            window.hide()
                
            window = main_window(csv_list_data)
            break
        
        if key_press == "Return":

            key_press = ""
                
            window.hide()
            
            change_data = change_dataset()
            
            csv_data.iloc[data_column,data_row] = change_data
            csv_data.to_csv(linkage_csv, mode = "w", index = False)
            
            print("紐付けデータの変更完了")
            csv_data = pd.read_csv(linkage_csv)

            csv_list_data = pd.read_csv(linkage_csv).values.tolist()
            
            window.hide()
            
            window = main_window(csv_list_data)

    window.hide()

#linkage2()
