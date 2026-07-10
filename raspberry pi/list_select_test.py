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

def main_window(List, lay_sel):
    if lay_sel == 0:
        layout = [[eg.Frame("List Selsct",[[eg.Listbox(List,key="-listbox-",
                                            enable_events=True, default_value=List[0],
                                            select_mode=eg.LISTBOX_SELECT_MODE_EXTENDED)],
                                            [eg.Text("-", key="-listbox-text-")],
                                            [eg.HSeparator()],
                                            [eg.Text("-", key="-text-")],],),
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
                                            [eg.HSeparator()],
                                            [eg.Text("-", key="-text-")],],),
                    eg.Frame("操作説明画面",
                             [[eg.Text("操作説明")],
                            [eg.HSeparator()],
                            [eg.Text("Tab > リスト選択画面に移行他")],
                            [eg.Text("Return > リスト選択中ならリストを選択")],
                            [eg.Text("[ESC] ... 終了")],],),],]
        
    return eg.Window('Window key test', layout,enable_key_events=True)



filepath = "/home/cells/control"
csv_list = glob.glob("*.csv")

test_list = ["list1", "list2", "list3", "list4"]
cursor_dict = {"Up":"select", "Down":"select", "Right":"select", "Left":"select"}

layout_select = 0

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
            key_select(key_press)
            miss_key = ""
            selected2 = miss_key
            window["-text-"].update(text=selected2)
            
    selected = " selected: " + "/".join(values["-listbox-"])
    window["-listbox-text-"].update(text=selected)
    
    #print(values["event_type"])
    if event == eg.WIN_CLOSED or key_press == "Escape":
        break
    
    if key_press == "Return":

        key_press = ""
        #windowから辞書形式のフォルダ内CSVファイルをテキストデータとして取り出す
        csv_list_name = "".join(values["-listbox-"])
        #CSVファイルの呼び出し(Pandas)
        csv_data = pd.read_csv(csv_list_name)
        
        print(csv_data)
        csv_col, csv_row = csv_data.shape
        #CSVをリストデータとして読み込み
        csv_list_data = pd.read_csv(csv_list_name).values.tolist()
        
        window.close()
        #ある意味強制的にメインのウインドウ操作を止める
        layout_select = 1
        window = main_window(csv_list_data, layout_select)
        
        data_row = 0
        data_column = 0
        
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
                        
                    if data_row == 0:
                        #windowでの表示
                        selected = "P, axis:" + str(data_column)
                        window["-listtext-"].update(text=selected)
                        csv_select_data = "Select data:" + str(csv_list_data[data_column][data_row])
                        window["csv"].update(text=csv_select_data)
                        
                    elif data_row == 1:
                        #windowでの表示
                        selected = "I, axis:" + str(data_column)
                        window["-listtext-"].update(text=selected)
                        csv_select_data = "Select data:" + str(csv_list_data[data_column][data_row])
                        window["csv"].update(text=csv_select_data)
                        
                    elif data_row == 2:
                        #windowでの表示
                        selected = "D, axis:" + str(data_column)
                        window["-listtext-"].update(text=selected)
                        csv_select_data = "Select data:" + str(csv_list_data[data_column][data_row])
                        window["csv"].update(text=csv_select_data)
                        
                    elif data_row == 3:
                        #windowでの表示
                        selected = "alpha, axis:" + str(data_column)
                        window["-listtext-"].update(text=selected)
                        csv_select_data = "Select data:" + str(csv_list_data[data_column][data_row])
                        window["csv"].update(text=csv_select_data)
                        
                    elif data_row == 4:
                        #windowでの表示
                        selected = "beta, axis:" + str(data_column)
                        window["-listtext-"].update(text=selected)
                        csv_select_data = "Select data:" + str(csv_list_data[data_column][data_row])
                        window["csv"].update(text=csv_select_data)
                    
            if event == eg.WIN_CLOSED or key_press == "Escape":
                key_press = ""
                window.close()
                #ある意味強制的にメインのウインドウ操作を止める
                layout_select = 0
                window = main_window(csv_list, layout_select)
                break
            
    # TkEasyGUI key events --> enable_key_events=True
    #if event == eg.WINDOW_KEY_EVENT:
    #    key = values["key"]
    #    if key == "Escape":
    #        break
window.close()
