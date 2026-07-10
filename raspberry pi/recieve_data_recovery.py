def recovery(sign, _int, deci):
    
    sign_data = 0.0
    int_data = 0.0
    deci_data = 0.0
    
    sign_data = sign
    int_data = _int
    deci_data = deci
    
    if sign_data == 255:
        sign_data = 1.0
        deci_data = deci_data * 0.01
        recovery_data = sign_data * (int_data + deci_data)
        
    elif sign_data == 250:
        sign_data = -1.0
        deci_data = deci_data * 0.01
        recovery_data = sign_data * (int_data + deci_data)
        
    return recovery_data
