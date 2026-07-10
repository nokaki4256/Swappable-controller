"""
# Window key events
"""
import TkEasyGUI as eg

import sys
import pandas as pd
import glob

import time

import smbus
bus = smbus.SMBus(1)#インスタンス定義 > i2cを使うための定型文

import i2caddress_check
import axis_calc

old_Lc = 0.0
old_arm_LR = 0.0
old_arm_Length = 0.0
old_arm_UD = 0.0

#ワイヤーコントローラから上下左右とワイヤーの長さ
#身長とユニットを伸ばした最大の長さを入力
def wire_calc(wire_LR, wire_UD, wire_Length, body_length, unit_home_length):
    
    arm_home_length = 0.325 * body_length
    k = unit_home_length / arm_home_length #人間の腕とアームの比率を計算
    
    wire_Length = abs(wire_Length - 921)
    #wire_UD = wire_UD + 90
    
    #ワイヤー側の座標計算
    wire_x = wire_Length * axis_calc.sin(wire_UD) *  axis_calc.cos(wire_LR)
    wire_y = wire_Length * axis_calc.sin(wire_UD) *  axis_calc.sin(wire_LR)
    wire_z = wire_Length * axis_calc.cos(wire_UD)
    
    wire_x = round(wire_x,2)
    wire_y = round(wire_y,2)
    wire_z = round(wire_z,2)
    
    Lc = 0.0
    
    if wire_UD == 90:
        Lc = old_Lc
    elif wire_UD != 90:
        if axis_calc.tan(wire_UD) != 0:
            #Lc = wire_y / axis_calc.tan(wire_LR)
            Lc = wire_y / axis_calc.tan(wire_UD)
        elif axis_calc.tan(wire_UD) == 0:
            Lc = old_Lc
        
    La = arm_home_length - Lc
    
    arm_y = wire_y
    
    arm_LR = 0.0
    
    if axis_calc.atan(arm_y / La) == 90:
        arm_LR = old_arm_LR
    elif axis_calc.atan(arm_y / La) != 90:
        arm_LR = axis_calc.atan((arm_y * axis_calc.tan(wire_LR)) / La)
    
    arm_Length = 0.0
    if axis_calc.cos(arm_LR) == 0:
        arm_Length = old_arm_Length
    elif axis_calc.cos(arm_LR) != 0:
        arm_Length = La / axis_calc.cos(arm_LR)
        
    #sub_calc1 = wire_Length * axis_calc.sin(wire_LR)
    #sub_calc2 = arm_Length * axis_calc.sin(arm_LR)
    sub_calc1 = round(wire_Length * axis_calc.tan(wire_UD),2)
    sub_calc2 = round(La,2)
        
    arm_UD = 0.0
    #if sub_calc2 == 0:
    if sub_calc1/sub_calc2 == 90:
        arm_UD = old_arm_UD
    #elif sub_calc2 != 0:
    elif sub_calc1/sub_calc2 != 90:
        #arm_UD = axis_calc.sin(wire_UD)*axis_calc.asin((sub_calc1/sub_calc2) * axis_calc.sin(arm_UD))
        arm_UD = axis_calc.atan(sub_calc1/sub_calc2)
    
    unit_UD = 0.0
    unit_LR = 0.0
    
    unit_UD = round(arm_UD,2)
    unit_LR = round(arm_LR,2)
    unit_Length = round(k * arm_Length,2)
    
    print("ユニットの左右角度:",unit_LR)
    print("ユニットの上下角度:",unit_UD)
    print("wire_y:",wire_y)
    print("La:",La)
    print("ユニットの長さ:",unit_Length)
    
    old_Lc = Lc
    old_arm_Length = arm_Length
    old_arm_LR = arm_LR
    old_arm_UD = arm_UD
    
    
    return 0
    #return unit_LR, unit_LR, unit_Length

def trace(frame, event, arg):
    print("--")
    print(f"file = {frame.f_code.co_filename}, func = {frame.f_code.co_name}, lineno = {frame.f_lineno}")
    print(f"event = {event}")
    print(f"arg = {arg}")
    
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
#[eg.Button("移行",key = "control_mode"),
    #ボタンの場合ボタンがイベントとして返す キーを設定すればキーを返す
    layout = [[eg.Button("コンフィグ",key = "config"),
               eg.Button("Exit")],
              [eg.Frame("左コントローラ",
                         [[eg.Text("AD1:"),eg.Text("", key = "AD1")],
                          [eg.Text("AD2:"),eg.Text("", key = "AD2")],
                          [eg.Text("AD3:"),eg.Text("", key = "AD3")],
                          [eg.Text("AD4:"),eg.Text("", key = "AD4")],
                          [eg.HSeparator()],
                          [eg.Text("axis1:")],
                          [eg.Text("axis2:")],
                          [eg.Text("axis3:")],
                          ],
                         ),
                eg.Frame("センターコントローラ",
                         [[eg.Text("axis1:")],
                          [eg.Text("axis2:")],
                          [eg.Text("axis3:")],
                          ],
                         ),
               eg.Frame("右コントローラ",
                         [[eg.Text("AD1:")],
                          [eg.Text("AD2:")],
                          [eg.Text("AD3:")],
                          [eg.Text("AD4:")],
                          [eg.HSeparator()],
                          [eg.Text("axis1:")],
                          [eg.Text("axis2:")],
                          [eg.Text("axis3:")],
                          ],
                         ),
               ],
              ]

        
    return eg.Window('センサー接続の確認', layout,enable_key_events=True,enable_events=True)

def check():
    slave_address = i2caddress_check.add_check()
    print("address:",slave_address[1])
    
    #確認するデータはアドレスを直接指定orユニット指定
    #取得したアドレスがどのユニットに対応するかを調べる
    
    filepath = "/home/cells/control"
    csv_list = glob.glob("*.csv")

    test_list = ["list1", "list2", "list3", "list4"]
    cursor_dict = {"Up":"select", "Down":"select", "Right":"select", "Left":"select"}

    layout_select = 0

    window = main_window(csv_list, layout_select)
    key_press = ""
    miss_key = ""

    check_count = 0
    old_length = 0.0

    # event loop
    while True:
        
        event, values = window.read(timeout=300,timeout_key='timeout')

        #print(event)
        #print(values)
        try:
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
        except KeyError:
            pass
        if event in "timeout":
            send_data = [50]
            command = [180]
            command += send_data
            recieve_data = []

            try:
                bus.write_block_data(slave_address[1], 7, command)
            except OSError:
                print("通信がおかしい？")
            try:
                recieve_data = bus.read_i2c_block_data(slave_address[1], 0, 21)
                AD_rev = []
                
                i = 0
                                
                for i in range(5):
                    if recieve_data[3 * i + 1] == 255:
                        _AD_rev = recieve_data[3 * i + 2] + 0.01 * recieve_data[3 * i + 3]
                        if _AD_rev > 255 or _AD_rev < -255:
                            _AD_rev = 0
                    elif recieve_data[3 * i + 1] == 250:
                        _AD_rev = (-1.0) * (recieve_data[3 * i + 2] + 0.01 * recieve_data[3 * i + 3])
                    AD_rev.append(_AD_rev)
                print(AD_rev)

            except OSError:
                print("通信がおかしい その2？")
            except IndexError:
                print("インデックスエラー")
            except UnboundLocalError:
                print("とりあえず無視")
                
            window["AD1"].update(AD_rev[0])
            window["AD2"].update(AD_rev[1])
            window["AD3"].update(AD_rev[2])
            window["AD4"].update(AD_rev[3])
            
        if event == "control_mode":
            print(" ")
        #sys.settrace(trace)
        #print(values["event_type"])
        if event in ["Exit", eg.WIN_CLOSED] or key_press == "Escape":
            break
        #old_length = Length

    window.hide()

check()
