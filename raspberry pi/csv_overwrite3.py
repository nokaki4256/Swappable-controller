"""
# Window key events
"""
import TkEasyGUI as eg

import pandas as pd
import glob

import time

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

def overwrite_data():
    csv_input_data = eg.popup_get_text("変更する数値を入力")
    eg.popup("変更する数値は..." + csv_input_data)
    return csv_input_data

def main_window(List, lay_sel):
    if lay_sel == 0:
        layout = [[eg.Frame("List Selsct",[[eg.Listbox(List,key="-listbox-",
                                            enable_events=True,
                                            default_value=List[0],
                                            select_mode=eg.LISTBOX_SELECT_MODE_EXTENDED)],
                                            [eg.Text("", key="-listbox-text-")],
                                            [eg.Text("", key="-text-")],],),
                    eg.Frame("操作説明画面",
                             [[eg.Text("操作説明")],
                            [eg.HSeparator()],
                            [eg.Text("Tab > リスト選択画面に移行他")],
                            [eg.Text("Return > リスト選択中ならリストを選択")],
                            [eg.Text("[ESC] ... 終了")],],),],]
    elif lay_sel == 1:
        layout = [[eg.Frame("List Selsct",[[eg.Listbox(List,key="-listbox-",
                                            enable_events=True, default_value=List[0],
                                            select_mode=eg.LISTBOX_SELECT_MODE_EXTENDED)],
                                            [eg.Text("-", key="-listtext-")],
                                            [eg.Text(key="csv")],
                                            [eg.Text("-", key="-text-")],],),
                    eg.Frame("操作説明画面",
                             [[eg.Text("操作説明")],
                            [eg.HSeparator()],
                            [eg.Text("Tab > リスト選択画面に移行他")],
                            [eg.Text("Return > リスト選択中ならリストを選択")],
                            [eg.Text("[ESC] ... 終了")],],),],]
        
    return eg.Window('Window key test', layout,enable_key_events=True)

def over_write3(dataset_csv_list):
    
    #csv_list = glob.glob("*.csv", root_dir = "dataset")
    csv_list = dataset_csv_list.copy()

    cursor_dict = {"Up":"select", "Down":"select", "Right":"select", "Left":"select"}

    layout_select = 0
    data_row = 0
    data_column = 0

    window = main_window(csv_list, layout_select)
    key_press = ""
    miss_key = ""
    # event loop
    while True:
        event, values = window.read()
        
        if values["event_type"] == "select":
            print("リストボックスの選択")
            
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
                _column, _row = key_select(key_press)
                
                key_select(key_press)
                miss_key = ""
                selected2 = miss_key
                window["-text-"].update(text=selected2)

                data_column = data_column + _column
                if data_column > len(csv_list) - 1:
                    data_column = 0
                elif data_column < 0:
                    data_column = len(csv_list) - 1
                
        #selected = " selected: " + "/".join(values["-listbox-"])
        selected = csv_list[data_column]
        window["-listbox-text-"].update(text=selected)
        
        #print(values["event_type"])closeclo
        if event == eg.WIN_CLOSED or key_press == "Escape":
            window.hide()
            return selected
        
        #データセット決定後
        if key_press == "Return":

            key_press = ""
            csv_list_name = "dataset/"+ selected
            #csv_list_name = selected
            print("ここ")
            print(csv_list_name)
            
            #CSV選択段階でdatasetのフォルダを使用してるから問題ないみたい

            #CSVファイルの呼び出し(Pandas)
            csv_data = pd.read_csv(csv_list_name)
            #ヘッダーのみを取り出すため追加で読み込み
            csv_data_header = pd.read_csv(csv_list_name, header = None).values.tolist()
            header_data = csv_data_header[0]

            print(csv_data)
            print(header_data)
            
            csv_col, csv_row = csv_data.shape
            #CSVをリストデータとして読み込み
            csv_list_data = pd.read_csv(csv_list_name).values.tolist()
            window.hide()
            #ある意味強制的にメインのウインドウ操作を止める
            layout_select = 1
            window = main_window(csv_list_data, layout_select)
            
            data_row = 0
            data_column = 0
            
            while True:
                change_data = 0.0
                event, values = window.read()

                if values["event_type"] == "select":
                    print("リストボックスの選択")
                    
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
                        _column, _row = key_select(key_press)

                        miss_key = ""
                        selected2 = miss_key
                        window["-text-"].update(text=selected2)
                        
                        #多次元配列のデータ選択用計算
                        data_row = data_row + _row
                        if data_row > csv_row - 1:
                            data_row = 0
                        elif data_row < 0:
                            data_row = csv_row - 1
                                                
                        data_column = data_column + _column
                        if data_column > csv_col - 1:
                            data_column = 0
                        elif data_column < 0:
                            data_column = csv_col - 1

                        #矢印の操作だけでヘッダーはそのままで軸を連動して変更
                        #軸が関係ないものは表示しない
                        if data_row < 6:
                            selected = header_data[data_row] + ":axis" + str(data_column)
                            window["-listtext-"].update(text=selected)
                            csv_select_data = "Select data:" + str(csv_list_data[data_column][data_row])
                            window["csv"].update(text=csv_select_data)
                        elif data_row >= 6:
                            selected = header_data[data_row]
                            window["-listtext-"].update(text=selected)
                            csv_select_data = "Select data:" + str(csv_list_data[data_column][data_row])
                            window["csv"].update(text=csv_select_data)

                            
                if key_press == "Return":
                    change_data = overwrite_data()
                    csv_data.iloc[data_column,data_row] = change_data
                    csv_data.to_csv(csv_list_name, mode = "w", index = False)
                    
                    print("CSVデータの上書き終了")
                    csv_data = pd.read_csv(csv_list_name)

                    csv_list_data = pd.read_csv(csv_list_name).values.tolist()
                    
                    window.hide()
                    window = main_window(csv_list_data, layout_select)
                        
                if event == eg.WIN_CLOSED or key_press == "Escape":
                    key_press = ""
                    event = ""
                    values = ""
                    window.hide()
                    #ある意味強制的にメインのウインドウ操作を止める
                    layout_select = 0
                    window = main_window(csv_list, layout_select)
                    break

    window.hide()
#over_write3("dataset")
