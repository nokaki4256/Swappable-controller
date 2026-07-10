"""
### Slider Test
"""
import TkEasyGUI as eg

import pandas as pd
import glob

import smbus
bus = smbus.SMBus(1)#インスタンス定義 > i2cを使うための定型文

import time

import recieve_data_recovery
import sep_deci
import axis_calc

def send_data(select_addr, send_data):
    command = [200]
    command += send_data
    recieve_data = []

    try:
        bus.write_block_data(select_addr, 7, command)
    except OSError:
        print("通信がおかしい？")
    try:
        recieve_data = bus.read_i2c_block_data(select_addr, 0, 16)
    except OSError:
        print("通信がおかしい その2？")
    
    return recieve_data

            
def slide_wiget(number1):
    wiget = [eg.Slider(key="slide" + str(number1),
            range=[-90, 90], size=[6, 1],
            orientation="h",
            default_value=0, resolution=0.1,
            enable_events=True, disable_number_display=True),
            eg.Text("0.0", key="text"+ str(number1)),eg.Button("def"+ str(number1))]
    
    return wiget

def axis_slide_wiget():
    #デフォルトの値も引数で与える　ユニットのホームポジション時の座標値をデフォルトとする
    wiget = [eg.Slider(key="x",
            range=[-200, 300], size=[6, 1],
            orientation="h",
            default_value=0, resolution=0.1,
            enable_events=True, disable_number_display=True),
            eg.Text("0.0", key="xtext"),eg.Button("def x"),
             
            eg.Slider(key="y",
            range=[-200, 300], size=[6, 1],
            orientation="h",
            default_value=0, resolution=0.1,
            enable_events=True, disable_number_display=True),
            eg.Text("0.0", key="ytext"),eg.Button("def y"),
             
            eg.Slider(key="z",
            range=[-200, 300], size=[6, 1],
            orientation="h",
            default_value=0, resolution=0.1,
            enable_events=True, disable_number_display=True),
            eg.Text("0.0", key="ztext"),eg.Button("def z")]
    
    return wiget

def slide_window(count):
    i = 0
    
    all_wiget = []
    pass_data = []
    _wiget1 = 0
    _wiget2 = []

    wiget_part1 = []
    wiget_part2 = []
    
    axis_wiget = axis_slide_wiget()
    
    #ボタンの場合ボタンがイベントとして返す キーを設定すればキーを返す
    for i in range(count):
        _wiget1 = slide_wiget(i)
        pass_data.append(_wiget1)
    _wiget2 = pass_data.copy()
        
    for i in range(3):
        wiget_part1 += _wiget2[i]
        wiget_part2 += _wiget2[i + 3]

    layout1 = [[eg.Frame("Unit:",layout=[
                [eg.Button("unit1",key = "unit1"),
                 eg.Button("unit2",key = "unit2"),
                 eg.Button("unit3",key = "unit3"),
                 eg.Text("", key="select_unit")],
                [eg.Button("angle",key = "angle"),
                 eg.Button("axis",key = "axis"),
                 eg.Button("no_send",key = "no_send"),
                 eg.Text("", key="select_send_data")],
                 wiget_part1,wiget_part2,
                [eg.HSeparator()],
                 axis_wiget,
                [eg.Button("Exit")]
            ])]]
    return eg.Window("Test", layout1)

def slide(linkage_data_set):
    #1:ユニットナンバー,2:ユニット名,3:アドレス,4:PID CSV,5:Home CSV,6:Motor Limit CSV
    
    key_press = ""
    miss_key = ""
    cursor_dict = {"Up":"select", "Down":"select", "Right":"select", "Left":"select"}
    
    i = 0

    base_count = 6
    change_flag = 0
    default_flag = 0
    angle_send_flag = 0
    axis_send_flag = 0
    
    slide_data1 = [0.0,0.0,0.0,0.0,0.0,0.0]
    slide_data2 = [0.0,0.0,0.0,0.0,0.0,0.0]
    slide_data3 = [0.0,0.0,0.0,0.0,0.0,0.0]
    
    slide_x = [0.0,0.0,0.0]
    slide_y = [0.0,0.0,0.0]
    slide_z = [0.0,0.0,0.0]
    
    old_axis1 = 0.0
    old_axis2 = 0.0
    
    def_axis_x = 0
    def_axis_y = 0
    def_axis_z = 0
    
    def_axis_x, def_axis_y = axis_calc.parallel_link_kine(100, 100, 105, 90, 0)
    
    #unit1
    slide_x[0] = def_axis_x
    slide_y[0] = def_axis_y
    
    # create a window
    window = slide_window(base_count)

    _address = []
    _send = []
    _rev = []
    
    _send_axis = []
    
    while True:
        event, values = window.read()
        
        try:
            if values["event_type"] == "key":
                print(values["key"])
                key_press = values["key"]
                try:
                    print(cursor_dict[key_press])
                except KeyError:
                    miss_key = "矢印以外"
                    selected2 = miss_key
                else:
                    #矢印入力
                    key_select(key_press)
                    miss_key = ""
                    selected2 = miss_key
        except KeyError:
            pass
        
        if event in ["Exit", eg.WIN_CLOSED] or key_press == "Escape":
            break
        
        for i in range(base_count):
            if event == "slide" + str(i):
                v = values["slide" + str(i)]
                window["text" + str(i)].update(str(v))
            if event == "def" + str(i):
                window["slide" + str(i)].update(value=0)
                window["text" + str(i)].update("0.0")
             
        if event == "x":
            v2 = values["x"]
            window["xtext"].update(str(v2))
        if event == "def x":
            window["x"].update(value=0)
            window["xtext"].update("0.0")
            
        if event == "y":
            v2 = values["y"]
            window["ytext"].update(str(v2))
        if event == "def y":
            window["y"].update(value=0)
            window["ytext"].update("0.0")
            
        if event == "z":
            v2 = values["z"]
            window["ztext"].update(str(v2))
        if event == "def z":
            window["z"].update(value=0)
            window["ztext"].update("0.0")
            
        if event == "angle":
            window["select_send_data"].update(text="角度データ送信中")
            angle_send_flag = 1
            axis_send_flag = 0
        elif event == "axis":
            window["select_send_data"].update(text="座標データ送信中")
            angle_send_flag = 0
            axis_send_flag = 1
        elif event == "no_send":
            window["select_send_data"].update(text="")
            angle_send_flag = 0
            axis_send_flag = 0
       
        #ユニット選択時センサーの値を読み込んでスライドに反映？
            
        if event == "unit1":
            change_flag = 1
            default_flag = 1
            
        elif event == "unit2":
            change_flag = 2
            default_flag = 1
            
        elif event == "unit3":
            change_flag = 3
            default_flag = 1
            
        else:
            pass
                        
        if change_flag == 1:
            window["select_unit"].update(text="ユニット1選択中")
            
            if event == "def x":
                window["x"].update(value = def_axis_x)
                window["xtext"].update(str(def_axis_x))

            if event == "def y":
                window["y"].update(value = def_axis_y)
                window["ytext"].update(str(def_axis_y))

            if event == "def z":
                window["z"].update(value = def_axis_z)
                window["ztext"].update(str(def_axis_z))

            if default_flag == 1:
                
                for i in range(base_count):
                    value = slide_data1[i]
                    window["slide" + str(i)].update(value)
                    window["text" + str(i)].update(value)

                value = slide_x[0]
                window["x"].update(value)
                window["xtext"].update(value)
                value = slide_y[0]
                window["y"].update(value)
                window["ytext"].update(value)
                value = slide_z[0]
                window["z"].update(value)
                window["ztext"].update(value)
                
                default_flag = 0
                
            slide_x[0] = values["x"]
            slide_y[0] = values["y"]
            slide_z[0] = values["z"]
            
            #座標の範囲と座標が0の場合どうするか >　ホームポジションの状態を送信　またデータのセットを行う
            if slide_x[0] != 0 and slide_y[0] != 0:
                axis1, axis2 = axis_calc.parallel_link_inv_kine(100, 100, 105, slide_x[0], slide_y[0])
                
                if axis1 == 65535 and axis2 == 65535:
                    axis1 = old_axis1
                    axis2 = old_axis2
                elif axis1 != 65535 and axis2 != 65535:
                    old_axis1 = axis1
                    old_axis2 = axis2
                    
                sign, num1, num2 = sep_deci.separate_decimal(axis1)
                _send_axis.append(sign)
                _send_axis.append(num1)
                _send_axis.append(num2)
                sign, num1, num2 = sep_deci.separate_decimal(axis2)
                _send_axis.append(sign)
                _send_axis.append(num1)
                _send_axis.append(num2)
            
            #送信データに変換
            for i in range(base_count):
                if event == "slide" + str(i):
                    slide_data1[i] = values["slide" + str(i)]
                sign, num1, num2 = sep_deci.separate_decimal(slide_data1[i])
                _send.append(sign)
                _send.append(num1)
                _send.append(num2)
            _rev = send_data(int(linkage_data_set[0][2], 0), _send)
            #print(_send)
            #print(_send_axis)
            
            if angle_send_flag == 1:
                _rev = send_data(int(linkage_data_set[0][2], 0), _send)
                
            elif axis_send_flag == 1:
                _rev = send_data(int(linkage_data_set[0][2], 0), _send_axis)
                
            _send_axis = []
            _send =[]
            _rev = []

        elif change_flag == 2:
            window["select_unit"].update(text="ユニット2選択中")
            
            if event == "def x":
                window["x"].update(value = def_axis_x)
                window["xtext"].update(str(def_axis_x))

            if event == "def y":
                window["y"].update(value = def_axis_y)
                window["ytext"].update(str(def_axis_y))

            if event == "def z":
                window["z"].update(value = def_axis_z)
                window["ztext"].update(str(def_axis_z))

            if default_flag == 1:
                
                for i in range(base_count):
                    value = slide_data1[i]
                    window["slide" + str(i)].update(value)
                    window["text" + str(i)].update(value)

                value = slide_x[1]
                window["x"].update(value)
                window["xtext"].update(value)
                value = slide_y[1]
                window["y"].update(value)
                window["ytext"].update(value)
                value = slide_z[1]
                window["z"].update(value)
                window["ztext"].update(value)
                
                default_flag = 0
                
            slide_x[1] = values["x"]
            slide_y[1] = values["y"]
            slide_z[1] = values["z"]
            
            #座標の範囲と座標が0の場合どうするか >　ホームポジションの状態を送信　またデータのセットを行う
            if slide_x[1] != 0 and slide_y[1] != 0:
                axis1, axis2 = axis_calc.parallel_link_inv_kine(100, 100, 105, slide_x[0], slide_y[0])
                
                if axis1 == 65535 and axis2 == 65535:
                    axis1 = old_axis1
                    axis2 = old_axis2
                elif axis1 != 65535 and axis2 != 65535:
                    old_axis1 = axis1
                    old_axis2 = axis2
                    
                sign, num1, num2 = sep_deci.separate_decimal(axis1)
                _send_axis.append(sign)
                _send_axis.append(num1)
                _send_axis.append(num2)
                sign, num1, num2 = sep_deci.separate_decimal(axis2)
                _send_axis.append(sign)
                _send_axis.append(num1)
                _send_axis.append(num2)
            
            print(_send_axis)
            _send_axis = []
            
            #送信データに変換
            for i in range(base_count):
                if event == "slide" + str(i):
                    slide_data1[i] = values["slide" + str(i)]
                sign, num1, num2 = sep_deci.separate_decimal(slide_data1[i])
                _send.append(sign)
                _send.append(num1)
                _send.append(num2)
            _rev = send_data(int(linkage_data_set[0][2], 0), _send)
            #print(_rev)
            _send =[]
            _rev = []
            
        elif change_flag == 3:
            window["select_unit"].update(text="ユニット3選択中")
            
            if default_flag == 1:
                for i in range(base_count):
                    value = slide_data3[i]
                    window["slide" + str(i)].update(value)
                    window["text" + str(i)].update(value)
                default_flag = 0
                
                value = slide_x[2]
                window["x"].update(value)
                window["xtext"].update(value)
                value = slide_y[2]
                window["y"].update(value)
                window["ytext"].update(value)
                value = slide_z[2]
                window["z"].update(value)
                window["ztext"].update(value)
                
            slide_x[2] = values["x"]
            slide_y[2] = values["y"]
            slide_z[2] = values["z"]
            
            for i in range(base_count):
                if event == "slide" + str(i):
                    slide_data3[i] = values["slide" + str(i)]
    
    window.hide()
