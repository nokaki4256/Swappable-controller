import math
import matplotlib.pyplot as plt
import numpy as np

#degree入力でラジアン計算
def cos(theta):
    return math.cos(math.radians(theta))
def sin(theta):
    return math.sin(math.radians(theta))
def tan(theta):
    return math.tan(math.radians(theta))

def acos(values):
    return_data = 0
    try:
        return_data = math.degrees(math.acos(values))
    except ValueError:
        return 65535
    else:
        return return_data
def asin(values):
    return math.degrees(math.asin(values))
def atan(values):
    return math.degrees(math.atan(values))

def pow2(values):
    return pow(values,2)

def sqrt(values):
    return math.sqrt(values)

def arm_1axis_kine(theta):
    x = cos(theta)
    y = sin(theta)
    return x,y

def parallel_link_kine(linka, linkb, linkr, alpha, beta):

    x = (linkb * cos(180 - alpha)) + ((linka + linkr) * cos(beta))
    y = (linkb * sin(180 - alpha)) + ((linka + linkr) * sin(beta))
    return x, y

def parallel_link_inv_kine(linka, linkb, linkr, xp, yp):
    
    if xp > linka + linkr:
        xp = linka + linkr
        
    print("xp:",xp)
    print("yp:",yp) 
    
    Lop = sqrt(pow2(xp) + pow2(yp))
    
    gamma = asin(yp/Lop)
    
    sub_calc1 = pow2(Lop) + pow2(linkb) - pow2(linka + linkr)
    sub_calc2 = 2.0 * linkb * Lop
    
    _acos = acos(sub_calc1 / sub_calc2)
    
    if _acos != 65535:
        
        alpha = 180.0 - gamma - acos(sub_calc1 / sub_calc2)
        if alpha < 10:
            alpha = 10
        elif alpha > 165:
            alpha = 165
        
        sub_calc3 = pow2(linkb) + pow2(linka + linkr) - pow2(Lop)
        sub_calc4 =2.0 * linkb * (linka + linkr)
        
        _acos = acos(sub_calc3 / sub_calc4)
        
        if _acos != "ValueError acos":
            beta = acos(sub_calc3 / sub_calc4) - alpha
            
            if beta < 0:
                beta = 0
            elif beta > 85:
                beta = 85
        
        elif _acos == 65535:
            alpha = 65535
            beta  = 65535
            
        print("alpha:",alpha)
        print("beta:",beta)
        
        return alpha, beta

def main():
    i = 0
    j = 0
    
    xp_max = []
    yp_max = []
    
    xp_min = []
    yp_min = []
    
    xp1 = []
    yp1 = []
    
    xp2 = []
    yp2 = []
    
    _alpha1 = 175
    _beta1 = 0
    
    _alpha2 = 20
    _beta2 = 0
    
    #分解能
    resolution = 0.1
    
    x = 200
    y = 100
    alpha, beta = parallel_link_inv_kine(100, 100, 105, x, y)
    
    alpha = round(alpha, 1)
    beta = round(beta, 1)
    print("alpha:",alpha)
    print("beta:",beta)

    for i in range(int(90.0 / resolution)):
        for j in range(int(141.0 / resolution)):
            _x , _y = parallel_link_kine(100, 100, 105, _alpha1, _beta1)
            xp_max.append(_x)
            yp_max.append(_y)
            _alpha1 = _alpha1 - resolution

            #_x , _y = parallel_link_kine(100, 100, 105, _alpha2, _beta2)
            #_alpha2 = _alpha2 - resolution
            #xp_min.append(_x)
            #yp_min.append(_y)

        _beta1 = _beta1 + resolution
        _beta2 = _beta2 + resolution

    _alpha1 = 175
    _beta1 = 0
    
    _alpha2 = 20
    _beta2 = 0

    for i in range(int(90.0 / resolution)):
        _x1 , _y1 = parallel_link_kine(100, 100, 105, _alpha1, _beta1)
        _alpha1 = _alpha1 + resolution
        _beta1 = _beta1 + resolution
        xp1.append(_x1)
        yp1.append(_y1)
        
        _x2 , _y2 = parallel_link_kine(100, 100, 105, _alpha2, _beta2)
        _beta2 = _beta2 + resolution
        xp2.append(_x2)
        yp2.append(_y2)      
    #xp,ypの最大最小を表示
        
    fig, ax = plt.subplots()
    ax.plot(xp_max, yp_max, ".")
    ax.plot(xp1, yp1, ".")
    ax.plot(xp2, yp2, ".")
    plt.show()
    
main()
