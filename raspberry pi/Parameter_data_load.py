import csv
import pprint
import glob
import pandas as pd

import sep_deci

def PID_data_load(CSV_NAME, P_command, I_command, D_command, a_command, b_command):
    print("PIDデータを送信データに変換")
    
    csv_col = 0
    csv_row = 0

    i = 0
    
    P = []
    I = []
    D = []
    a = []
    b = []
    
    #i2c 送信用コマンドを0番目に指定
    P_send = [P_command]
    I_send = [I_command]
    D_send = [D_command]
    a_send = [a_command]
    b_send = [b_command]
    
    csv_data = pd.read_csv(CSV_NAME)
    csv_col, csv_row = csv_data.shape
    print(csv_data)
    
    #送信データはPIDは分ける > 全データを送るとなると54バイト必要
    #内訳:6軸×PID3種×実数値3バイト
    #パラメータ単体で考えるとP単体で18バイト
    for i in range(csv_col):
        P.append(csv_data.iloc[i,0])
        I.append(csv_data.iloc[i,1])
        D.append(csv_data.iloc[i,2])
        a.append(csv_data.iloc[i,3])
        b.append(csv_data.iloc[i,4])

    sign_data = 0
    int_data = 0
    deci_data = 0
    
    P_separate = []
    I_separate = []
    D_separate = []
    a_separate = []
    b_separate = []
    
    for i in range(csv_col):
        try:
            sign_data, int_data, deci_data = sep_deci.separate_decimal(float(P[i]))
            P_separate.append(sign_data)
            P_separate.append(int_data)
            P_separate.append(deci_data)
            
            sign_data, int_data, deci_data = sep_deci.separate_decimal(float(I[i]))
            I_separate.append(sign_data)
            I_separate.append(int_data)
            I_separate.append(deci_data)
            
            sign_data, int_data, deci_data = sep_deci.separate_decimal(float(D[i]))
            D_separate.append(sign_data)
            D_separate.append(int_data)
            D_separate.append(deci_data)
            
            sign_data, int_data, deci_data = sep_deci.separate_decimal(float(a[i]))
            a_separate.append(sign_data)
            a_separate.append(int_data)
            a_separate.append(deci_data)
            
            sign_data, int_data, deci_data = sep_deci.separate_decimal(float(b[i]))
            b_separate.append(sign_data)
            b_separate.append(int_data)
            b_separate.append(deci_data)
        except ValueError:
            print("数値がおかしい")
        
    P_separate.append(int(P[5]))
    I_separate.append(int(I[5]))
    D_separate.append(int(D[5]))
    a_separate.append(int(a[5]))
    b_separate.append(int(b[5]))
    
    P_send.extend(P_separate)
    I_send.extend(I_separate)
    D_send.extend(D_separate)
    a_send.extend(a_separate)
    b_send.extend(b_separate)
    
    return P_send,I_send,D_send,a_send,b_send

def Home_data_load(CSV_NAME, Home_command):
    print("ホームポジションデータを送信データに変換")
    print(CSV_NAME)
    csv_list = glob.glob("*.csv")
    
    csv_col = 0
    csv_row = 0

    i = 0
    
    Home = []
    
    #i2c 送信用コマンドを0番目に指定
    Home_send = [Home_command]
    
    print("対応するファイルを抽出")
    for i in range(len(csv_list)):
        select_csv = csv_list[i]
        #開始前にアドレスに対して何を使用してるか選択する？
        if select_csv == CSV_NAME:
            print("抽出OK")
            csv_data = pd.read_csv(select_csv)
            csv_col, csv_row = csv_data.shape
            print(csv_data)
            break
    #送信データはPIDは分ける > 全データを送るとなると54バイト必要
    #内訳:6軸×PID3種×実数値3バイト
    #パラメータ単体で考えるとP単体で18バイト
    for i in range(csv_col):
        Home.append(csv_data.iloc[i,0])

    sign_data = 0
    int_data = 0
    deci_data = 0
    
    Home_separate = []
    
    for i in range(csv_col):
        sign_data, int_data, deci_data = sep_deci.separate_decimal(float(Home[i]))
        Home_separate.append(sign_data)
        Home_separate.append(int_data)
        Home_separate.append(deci_data)
        
    Home_send.extend(Home_separate)
    
    return Home_send

def motor_limit_load(CSV_NAME, limit_command):
    print("モータ出力リミットデータを送信データに変換")
    print(CSV_NAME)
    csv_list = glob.glob("*.csv")
    
    csv_col = 0
    csv_row = 0

    i = 0
    
    limit = []
    
    #i2c 送信用コマンドを0番目に指定
    limit_send = [limit_command]
    
    print("対応するファイルを抽出")
    for i in range(len(csv_list)):
        select_csv = csv_list[i]
        #開始前にアドレスに対して何を使用してるか選択する？
        if select_csv == CSV_NAME:
            print("抽出OK")
            csv_data = pd.read_csv(select_csv)
            csv_col, csv_row = csv_data.shape
            print(csv_data)
            break
    #送信データはPIDは分ける > 全データを送るとなると54バイト必要
    #内訳:6軸×PID3種×実数値3バイト
    #パラメータ単体で考えるとP単体で18バイト
    for i in range(csv_col):
        limit.append(int(csv_data.iloc[i,0]))

    limit_send.extend(limit)
    
    return limit_send
