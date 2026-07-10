import smbus
import time

bus = smbus.SMBus(1)#インスタンス定義 > i2cを使うための定型文

import Parameter_data_load

def PID_Pulse_default(address, CSV, Pulse):
    print(Pulse)
    Pulse_width = [170]
    Pulse_width.append(Pulse)
    try:
        count = 0
        while count != 5:                
            P = []
            I = []
            D = []
            a = []
            b = []
            
            P, I, D, a, b = Parameter_data_load.PID_data_load(CSV, 160, 161, 162, 210, 211)
            
            #引数２番めはデータの入ってるレジスタの指定
            #このレジスタは容量的に30バイト
            #連続で30バイト近いデータを送る場合指定する必要あり       
            for i in range(5):
                if i == 0:
                    print(P)
                    bus.write_block_data(address, 0, P)
                    time.sleep(0.01)

                elif i == 1:
                    print(I)
                    bus.write_block_data(address, 1, I)
                    time.sleep(0.01)

                elif i == 2:
                    print(D)
                    bus.write_block_data(address, 2, D)
                    time.sleep(0.01)
                    
                elif i == 3:
                    print(a)
                    bus.write_block_data(address, 3, a)
                    time.sleep(0.01)
                
                elif i == 4:
                    print(b)
                    bus.write_block_data(address, 4, b)
                    time.sleep(0.01)
                    
            bus.write_block_data(address, 5, Pulse_width)
            time.sleep(0.01)
                
            #引数3は取得するデータ数の指定
            #引数2は上記と同様 結局よくわからん
            #受けて側の引数2番目は30バイトの受け皿?

            recieve_data = bus.read_i2c_block_data(address, 0, 1)
            
            print(recieve_data)
            if recieve_data[0] == 164:
                print("ユニットの通信を確認")
                print("PIDとパルス幅とその他の初期設定を反映してるはず")
                break
            elif recieve_data[0] == 165:
                print("初期データは反映済み 何も変わってない...? 接続はしてるよ")
                break
            else:
                if count != 5:
                    print("未接続？　再送信")
                elif count == 5:
                    print("I2C未接続の可能性が高いかも")
            #time.sleep(2)
            count = count + 1
    except OSError:
        print("相手側のI2Cが切れた可能性あり")
        print("再送信")
    except ValueError:
        print("数値がおかしい？")
        print("やり直し")

def PID_Pulse_overwrite(address, CSV, Pulse):
    Pulse_width = [171]
    Pulse_width.append(Pulse)
    try:
        count = 0
        while count != 5:                
            P = []
            I = []
            D = []
            a = []
            b = []
            
            P, I, D, a, b = Parameter_data_load.PID_data_load(CSV, 166, 167, 168, 213, 214)
            
            #引数２番めはデータの入ってるレジスタの指定
            #このレジスタは容量的に30バイト
            #連続で30バイト近いデータを送る場合指定する必要あり       
            for i in range(3):
                if i == 0:
                    print(P)
                    bus.write_block_data(address, 3, P)
                    time.sleep(0.01)

                elif i == 1:
                    print(I)
                    bus.write_block_data(address, 4, I)
                    time.sleep(0.01)

                elif i == 2:
                    print(D)
                    bus.write_block_data(address, 5, D)
                    time.sleep(0.01)
                    
                elif i == 3:
                    print(D)
                    bus.write_block_data(address, 6, a)
                    time.sleep(0.01)
                
                elif i == 4:
                    print(D)
                    bus.write_block_data(address, 7, b)
                    time.sleep(0.01)
                    
            bus.write_block_data(address, 3, Pulse_width)
            time.sleep(0.01)
                
            #引数3は取得するデータ数の指定
            #引数2は上記と同様 結局よくわからん
            #受けて側の引数2番目は30バイトの受け皿?

            recieve_data = bus.read_i2c_block_data(address, 0, 1)
            
            print(recieve_data)
            if recieve_data[0] == 169:
                print("PIDとパルス幅の上書きを反映")
                break
            elif recieve_data[0] == 176:
                print("何もしてない...? 接続はしてるよ")
                break
            else:
                if count != 5:
                    print("未接続？　再送信")
                elif count == 5:
                    print("I2C未接続の可能性が高いかも")
            count = count + 1
    except OSError:
        print("相手側のI2Cが切れた可能性あり")
        print("再送信")

def Home_Position_default(address, CSV):
    try:
        count = 0
        while count != 5:                
            Home = []
            
            Home = Parameter_data_load.Home_data_load(CSV, 174)
            
            #引数２番めはデータの入ってるレジスタの指定
            #このレジスタは容量的に30バイト
            #連続で30バイト近いデータを送る場合指定する必要あり       
            print(Home)
            bus.write_block_data(address, 6, Home)
            time.sleep(0.01)
                    
                
            #引数3は取得するデータ数の指定
            #引数2は上記と同様 結局よくわからん
            #受けて側の引数2番目は30バイトの受け皿?

            recieve_data = bus.read_i2c_block_data(address, 0, 1)
            
            print(recieve_data)
            if recieve_data[0] == 175:
                print("ホームポジションのデフォルトを反映")
                break
            elif recieve_data[0] == 176:
                print("何もしてない...? 接続はしてるよ")
                break
            else:
                if count != 5:
                    print("未接続？　再送信")
                elif count == 5:
                    print("I2C未接続の可能性が高いかも")
            count = count + 1
    except OSError:
        print("相手側のI2Cが切れた可能性あり")
        print("再送信")

def Motor_Limit_default(address, CSV):
    try:
        count = 0
        while count != 5:                
            limit = []
            
            limit = Parameter_data_load.motor_limit_load(CSV, 172)
            
            #引数２番めはデータの入ってるレジスタの指定
            #このレジスタは容量的に30バイト
            #連続で30バイト近いデータを送る場合指定する必要あり       
            print(limit)
            bus.write_block_data(address, 6, limit)
            time.sleep(0.01)
            
            #引数3は取得するデータ数の指定
            #引数2は上記と同様 結局よくわからん
            #受けて側の引数2番目は30バイトの受け皿?

            recieve_data = bus.read_i2c_block_data(address, 0, 1)
            
            print(recieve_data)
            if recieve_data[0] == 173:
                print("モータリミットのデフォルトを反映")
                break
            elif recieve_data[0] == 176:
                print("何もしてない...? 接続はしてるよ")
                break
            else:
                if count != 5:
                    print("未接続？　再送信")
                elif count == 5:
                    print("I2C未接続の可能性が高いかも")
            count = count + 1
    except OSError:
        print("相手側のI2Cが切れた可能性あり")
        print("再送信")

