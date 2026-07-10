import csv
import pprint
import glob
import pandas as pd

import sep_deci

def PID_data_load(CSV_NAME, P_command, I_command, D_command, a_command, b_command):
    print("PIDデータを送信データに変換")
    #データセット内のパラメータ使用に変更

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
    csv_data = pd.read_csv(CSV_NAME).values.tolist()
    print(csv_data)

    i = 0
    
    Home = []
    
    #i2c 送信用コマンドを0番目に指定
    Home_send = []

    #送信データはPIDは分ける > 全データを送るとなると54バイト必要
    #内訳:6軸×PID3種×実数値3バイト
    #パラメータ単体で考えるとP単体で18バイト
    Home.append(float(csv_data[0][7]))
    Home.append(float(csv_data[1][7]))
    Home.append(float(csv_data[2][7]))

    sign_data = 0
    int_data = 0
    deci_data = 0
    
    Home_send.append(Home_command)
        
    for i in range(len(Home)):
        sign_data, int_data, deci_data = sep_deci.separate_decimal(float(Home[i]))
        Home_send.append(sign_data)
        Home_send.append(int_data)
        Home_send.append(deci_data)
        
    print("ホームポジション 送信データ")
    print(Home_send)
    
    return Home_send

def motor_limit_load(CSV_NAME, limit_command):
    print("モータ出力リミットデータを送信データに変換")
    csv_data = pd.read_csv(CSV_NAME).values.tolist()
    print(csv_data)

    i = 0
    
    limit_send = []
    
    #i2c 送信用コマンドを0番目に指定
    limit_send.append(limit_command)

    limit_send.append(int(csv_data[0][5]))
    print("モータリミット 送信データ")
    print(limit_send)
    
    return limit_send
