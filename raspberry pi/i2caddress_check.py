import smbus
import time

import TkEasyGUI as eg


def add_check():
    #eg.popup("アドレス確認を開始")
    bus_number = 1
    bus = smbus.SMBus(bus_number)
    
    check_address = []

    #print(f"I2Cバス(bus_number)のアドレスをスキャン中...")

    for device_address in range(128):
        try:
            bus.write_byte(device_address,0)
            print("確認済みのアドレス:",hex(device_address))
            if device_address != 0:
                check_address.append(device_address)
            
        except OSError:
            pass
        time.sleep(0.01)

    return check_address
