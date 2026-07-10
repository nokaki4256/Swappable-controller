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
#import axis_calc

import newfiler2
import data_linkage2
import csv_overwrite3
import sep_deci

import calculation_set

import Parameter_setup2

def trace(frame, event, arg):
    print("--")
    print(f"file = {frame.f_code.co_filename}, func = {frame.f_code.co_name}, lineno = {frame.f_lineno}")
    print(f"event = {event}")
    print(f"arg = {arg}")
    
def arduino_to_send(select_addr, send_data):
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

def unit_address_list():
    #ポップアップでリストを表示
    address_list = ["左腕:0x20","右腕:0x21","脚部:0x22",
                    "左コントローラ:0x30","右コントローラ:0x32","フット&ステアリング:0x31",
                    "テスト用マイコン:0x25"]
    eg.popup_listbox(values = address_list, message = "接続用アドレス一覧")
    
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

def main_window():
#[eg.Button("移行",key = "control_mode"),
    #ボタンの場合ボタンがイベントとして返す キーを設定すればキーを返す
    
    layout_left = eg.Frame("左コントローラ",
                         [[eg.Text("left1:"),eg.Text("", key = "left1")],
                          [eg.Text("left2:"),eg.Text("", key = "left2")],
                          [eg.Text("left3:"),eg.Text("", key = "left3")],
                          [eg.Text("lett4:"),eg.Text("", key = "left4")],
                          [eg.Text("leftSW:"),eg.Text("", key = "leftSW")],
                          [eg.HSeparator()],
                          [eg.Text("L axis x:"),eg.Text("", key = "left_axis_x")],
                          [eg.Text("L axis y:"),eg.Text("", key = "left_axis_y")],
                          [eg.Text("axis3:")],
                          [eg.Text("L arm angle1:"),eg.Text("", key = "L arm angle1")],
                          [eg.Text("L arm angle2:"),eg.Text("", key = "L arm angle2")],
                          ],
                         )
    
    layout_right = eg.Frame("右コントローラ",
                         [[eg.Text("AD1:")],
                          [eg.Text("AD2:")],
                          [eg.Text("AD3:")],
                          [eg.Text("AD4:")],
                          [eg.HSeparator()],
                          [eg.Text("axis1:")],
                          [eg.Text("axis2:")],
                          [eg.Text("axis3:")],
                          ],
                         )
    
    layout_center = eg.Frame("フットコントローラ",
                         [[eg.Text("foot1:"),eg.Text("", key = "foot1")],
                          [eg.Text("foot2:"),eg.Text("", key = "foot2")],
                          [eg.Text("foot3:"),eg.Text("", key = "foot3")],
                          [eg.Text("foot4:"),eg.Text("", key = "foot4")],
                          [eg.Text("foot5:"),eg.Text("", key = "foot5")],
                          [eg.HSeparator()],
                          [eg.Text("foot x:"),eg.Text("", key = "foot_axis_x")],
                          [eg.Text("foot y:"),eg.Text("", key = "foot_axis_y")],
                          [eg.Text("foot z:")],
                          ],
                         )
    
    layout = [[layout_left,
               layout_center,
               layout_right
               ],
              [eg.Text("左ユニット:"),eg.Text("", key = "leftunit")],
              [eg.Text("フットユニット："),eg.Text("", key = "footunit")],
              [eg.Text("右ユニット:")],
              [eg.Button("データセットの紐付け",key = "dataset"),
               eg.Button("パラメータコンフィグ",key = "config"),
               eg.Button("新規データセット作成",key = "new")],
              [eg.Button("左ユニット原点",key = "homeleft")],
              [eg.Button("ユニット対応アドレス一覧",key = "unit_address"),eg.Button("Exit")],
              ]

        
    return eg.Window('センサー接続の確認', layout,
                     enable_key_events=True,
                     enable_events=True,
                     size =(500,500))

def main_control():
    slave_address = i2caddress_check.add_check()

    i = 0
    
    #0x30(48):左コントローラ
    #0x31(49):フットコントローラ
    #0x32(50):右コントローラ
    left_control_address = 0
    foot_control_address = 0
    
    #通信が必要なアドレスは随時追加
    for i in range(len(slave_address)):
        if slave_address[i] == 48:
            left_control_address = slave_address[i]
        if slave_address[i] == 49:
            foot_control_address = slave_address[i]

    linkage_list = pd.read_csv("tester_linkage.csv").values.tolist()
    
    test_list = ["list1", "list2", "list3", "list4"]
    cursor_dict = {"Up":"select", "Down":"select", "Right":"select", "Left":"select"}
    
    window = main_window()
    key_press = ""
    miss_key = ""

    default_flag = [0,0,0]
    unit_dataset_csv = []
    unit_dataset = []
    
    #ユニットCSVを開いてリストに格納
    left_unit_dataset = pd.read_csv("dataset/" + linkage_list[0][2]).values.tolist()
    foot_unit_dataset = pd.read_csv("dataset/" + linkage_list[1][2]).values.tolist()
    right_unit_dataset = pd.read_csv("dataset/" + linkage_list[2][2]).values.tolist()
    
    dataset_csv_list = glob.glob("*.csv", root_dir = "dataset")
    print(dataset_csv_list)
    
    left_axis = []
    foot_axis = []
    rev_left_angle = []
    rev_foot_angle = []
    
    overwrite_flag = 0
    overwrite_name = ""
    # event loop
    while True:
        
        linkage_list_copy = linkage_list.copy()
        dataset_csv_list_copy = dataset_csv_list.copy()

        event, values = window.read(timeout=300,timeout_key='timeout')
        
        if event == "new":
            print("新規データセット作成")
            newfiler2.new_dataset()
        if event == "dataset":
            print("紐付けデータの変更")
            data_linkage2.linkage2()
            linkage_list = pd.read_csv("tester_linkage.csv").values.tolist()
        if event == "config":
            print("パラメータコンフィグ")
            print(dataset_csv_list_copy)
            overwrite_name = csv_overwrite3.over_write3(dataset_csv_list_copy)
            overwrite_flag = 1
        if event == "homeleft":
            print("左ユニット原点復帰")
            #データセット内のホームポジションデータを使用する
            left_axis[0] = float(left_unit_dataset[0][7])
            left_axis[1] = float(left_unit_dataset[1][7])
            left_axis[2] = float(left_unit_dataset[2][7])
        if event == "unit_address":
            unit_address_list()
        #sys.settrace(trace)
        #print(values["event_type"])
        if event in ["Exit", eg.WIN_CLOSED] or key_press == "Escape":
            break
        
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
            left_control = []
            right_control= []
            steering_control = []

            #各コントローラデータを一つのリストにまとめて入れる
            #左腕アーム操作ユニットのデータ受信
            try:
                bus.write_block_data(left_control_address, 7, command)
            except OSError:
                print("左コントローラの送信がおかしい？")
            try:
                left_control = bus.read_i2c_block_data(left_control_address, 0, 21)
                left_rev = []
                                
                for i in range(5):
                    if left_control[3 * i + 1] == 255:
                        _left_rev = left_control[3 * i + 2] + 0.01 * left_control[3 * i + 3]
                        _left_rev = round(_left_rev,2)
                        if _left_rev > 255 or _left_rev < -255:
                            _left_rev = 0
                    elif left_control[3 * i + 1] == 250:
                        _left_rev = (-1.0) * (left_control[3 * i + 2] + 0.01 * left_control[3 * i + 3])
                        _left_rev = round(_left_rev,2)
                    left_rev.append(_left_rev)
            except OSError:
                print("左コントローラの受信おかしい？")
            except IndexError:
                print("インデックスエラー")
            except UnboundLocalError:
                print("とりあえず無視")
            #フットのデータ受信
            try:
                bus.write_block_data(foot_control_address, 7, command)
            except OSError:
                print("フットコントローラ送信がおかしい？")

            try:
                foot_control = bus.read_i2c_block_data(foot_control_address, 0, 21)
                foot_rev = []

                for i in range(5):
                    if foot_control[3 * i + 1] == 255:
                        _foot_rev = foot_control[3 * i + 2] + 0.01 * foot_control[3 * i + 3]
                        _foot_rev = round(_foot_rev,2)
                        if _foot_rev > 255 or _foot_rev < -255:
                            _foot_rev = 0
                    elif foot_control[3 * i + 1] == 250:
                        _foot_rev = (-1.0) * (foot_control[3 * i + 2] + 0.01 * foot_control[3 * i + 3])
                        _foot_rev = round(_foot_rev,2)
                    foot_rev.append(_foot_rev)
                #print(left_rev)

            except OSError:
                print("フットコントローラの受信がおかしい？")
            except IndexError:
                print("インデックスエラー")
            except UnboundLocalError:
                print("とりあえず無視")
                
            window["left1"].update(left_rev[0])
            window["left2"].update(left_rev[1])
            window["left3"].update(left_rev[2])
            window["left4"].update(left_rev[3])
            window["leftSW"].update(left_rev[4])
            
            window["foot1"].update(foot_rev[0])
            window["foot2"].update(foot_rev[1])
            window["foot3"].update(foot_rev[2])
            window["foot4"].update(foot_rev[3])
            window["foot5"].update(foot_rev[4])
            
            select_address = 0
            #データ送信
            #処理的にはホームポジションに対して座標を増減
            #増減した座標を各アームの計算式に当てはめる
            #逆運動学からユニットに送信する角度データと
            #その角度データを元に順運動学から現在座標を計算
            for select_address in slave_address:
                if select_address == 0x20:
                    if default_flag[0] == 0:
                        print("左腕ユニットへ初期パラメータを送信")
                        window["leftunit"].update(left_unit_dataset[0][8])

                        Parameter_setup2.default_data_send(select_address, linkage_list_copy[0][2])
                        default_flag[0] = 1
                        
                        left_x = left_unit_dataset[0][7]
                        left_y = left_unit_dataset[1][7]
                        left_z = left_unit_dataset[2][7]
                        
                        left_axis.append(float(left_x))
                        left_axis.append(float(left_y))
                        left_axis.append(float(left_z))
                        
                    elif default_flag[0] == 1:
                        print(overwrite_flag)
                        if overwrite_flag == 1:
                            if linkage_list[0][2] == overwrite_name:
                                Parameter_setup2.PID_Pulse_overwrite(select_address, linkage_list_copy[0][2])
                                overwrite_flag = 0
                                print("上書きしたはず")
                        #目標値の加減算はここで
                        #x座標
                        left_axis[0] = round(left_axis[0] + left_rev[0], 2)
                        #y座標
                        left_axis[1] = round(left_axis[1] + left_rev[1], 2)
                        #z座標
                        left_axis[2] = round(left_axis[2] + left_rev[2], 2)
                        #ハンド
                        #left_axis[4] = round(left_axis[4] + left_rev[4], 2)
                        #print(left_axis)
                        
                        #送信するのはデータセットのリスト、座標リスト,　受信した角度リスト,順逆の選択
                        send_left_angle, left_limit_flag, left_calc_axis = calculation_set.branch(left_unit_dataset,
                                                                                                  left_axis,
                                                                                                  rev_left_angle,
                                                                                                  "inverted")
                        #リミットフラグが立っていた場合リミットが掛かった座標データをリミット座標に再設定する
                        left_axis[0] = left_calc_axis[0]
                        left_axis[1] = left_calc_axis[1]
                        window["left_axis_x"].update(left_axis[0])
                        window["left_axis_y"].update(left_axis[1])

                        window["L arm angle1"].update(send_left_angle[0])
                        window["L arm angle2"].update(send_left_angle[1])
                        #ここで
                        #接続してるユニットに角度データを送信
                        i = 0
                        left_send_data = []
                        
                        for i in range(len(send_left_angle)):
                            
                            left_sign, left_num1, left_num2 = sep_deci.separate_decimal(send_left_angle[i])
                            left_send_data.append(left_sign)
                            left_send_data.append(left_num1)
                            left_send_data.append(left_num2)

                        _rev = arduino_to_send(0x20, left_send_data)
                        print(_rev)
                if select_address == 0x21:
                    print("右腕ユニットへ初期パラメータを送信")
                    print(linkage_list[2][2])
                    """
                    right_position_x = unit_dataset[2][0][7]
                    right_position_y = unit_dataset[2][1][7]
                    right_position_z = unit_dataset[2][2][7]
                    """

                #フットユニットへのデータ送信
                if select_address == 0x22:
                    #print("脚部ユニットへ初期パラメータをデータ送信")
                    #print(linkage_list[1][2])
                    if default_flag[2] == 0:
                        print("フットユニットへ初期パラメータを送信")
                        window["footunit"].update(foot_unit_dataset[0][8])

                        Parameter_setup2.default_data_send(select_address, linkage_list_copy[1][2])
                        default_flag[2] = 1
                        
                        #ホームポジションデータの送信

                        foot_x = foot_unit_dataset[0][7]
                        foot_y = foot_unit_dataset[1][7]
                        foot_z = foot_unit_dataset[2][7]
                        
                        foot_axis.append(float(foot_x))
                        foot_axis.append(float(foot_y))
                        foot_axis.append(float(foot_z))
                        
                    elif default_flag[2] == 1:
                        print(overwrite_flag)
                        if overwrite_flag == 1:
                            if linkage_list[0][2] == overwrite_name:
                                Parameter_setup2.PID_Pulse_overwrite(select_address, linkage_list_copy[0][2])
                                overwrite_flag = 0
                                print("上書きしたはず")
                                
                        #送信するのはデータセットのリスト、座標リスト,　受信した角度リスト,順逆の選択
                        send_foot_angle, foot_limit_flag, foot_calc_axis = calculation_set.branch(foot_unit_dataset,
                                                                                                  foot_axis,
                                                                                                  rev_foot_angle,
                                                                                                  "rotate")
                        #リミットフラグが立っていた場合リミットが掛かった座標データをリミット座標に再設定する
                        foot_axis[0] = foot_rev[0]
                        foot_axis[1] = foot_rev[1]
                        window["foot_axis_x"].update(foot_rev[0])
                        window["foot_axis_y"].update(foot_rev[1])
                        #接続してるユニットに角度データを送信
                        i = 0
                        foot_send_data = []

                        for i in range(len(foot_rev)):
                            
                            foot_sign, foot_num1, foot_num2 = sep_deci.separate_decimal(foot_rev[i])
                            foot_send_data.append(foot_sign)
                            foot_send_data.append(foot_num1)
                            foot_send_data.append(foot_num2)
                            
                        #print(foot_send_data)

                        _rev = arduino_to_send(0x22, foot_send_data)
                        print(_rev)
    window.hide()

main_control()

