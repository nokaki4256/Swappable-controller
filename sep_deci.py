#入力された数値を符号、整数、小数点に変換
#プラス：255 マイナス:250 整数はそのままint 小数点以下は100倍にする>受けては1/100
def separate_decimal(num):
    
    if num < 0:
        num = abs(num)
        sign = 250#マイナスの場合
    elif num >= 0:
        sign = 255#プラスの場合
        
    num1 = int(num)

    num2 = int(round(100. * round(num - num1, 2), 0))
    
    return sign, num1, num2