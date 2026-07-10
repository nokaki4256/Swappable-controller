import math

#degree入力でラジアン計算
def cos(theta):
    return math.cos(math.radians(theta))
def sin(theta):
    return math.sin(math.radians(theta))
def tan(theta):
    return math.tan(math.radians(theta))

def acos(values):
    return_data = 0

    if values > 1.0:
        return 0.0
    elif values < -1.0:
        return 180.0
    try:
        return_data = math.degrees(math.acos(values))
    except ValueError:
        return 65535
    else:
        return return_data
def asin(values):
    return_data = 0

    if values > 1.0:
        return 90.0
    elif values < -1.0:
        return 90.0
    try:
        return_data = math.degrees(math.asin(values))
    except ValueError:
        return 65535
    return return_data
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
    
    x = round(x,2)
    y = round(y,2)
    
    return x, y

def parallel_link_inv_kine(linka, linkb, linkr, xp, yp):
    
    if xp >= linka + linkr:
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
            
        alpha = round(alpha,2)
        beta = round(beta,2)
        
        print("alpha:",alpha)
        print("beta:",beta)
        
        return alpha, beta

def one_link_arm(_dataset,angle):
    #angle内のリストの順番は根本から番号振り分け1軸なら１つだけ
    axis_back_list = []
    
    linka = _dataset[0][9]
    xaxis = linka * cos(angle[0])
    yaxis = linka * sin(angle[0])
    
    axis_back_list.append(round(float(xaxis), 2))
    axis_back_list.append(round(float(yaxis), 2))
    
    return axis_back_list

def one_link_arm_inv(_dataset,axis_list):
    linka = _dataset[0][9]
    angle_back_list = []
    limit_flag = [0,0,0,0,0,0]

    alpha = round(acos(axis_list[0] / linka),2)
    
    beta = round(asin(axis_list[1] / linka),2)
        
    angle_back_list.append(round(float(alpha), 2))
    
    #計算結果との比較用に順運動学で計算
    #計算で使ったのはリンク長と逆運動学で計算した角度で計算
    calc_axis = one_link_arm(_dataset,angle_back_list)
    
    if axis_list[0] < 0:
        if axis_list[0] < calc_axis[0]:
            print("over")
            limit_flag[0] = 1
        elif axis_list[0] >= calc_axis[0]:
            print("ok")
            limit_flag[0] = 0
            
    if axis_list[0] > 0:
        if axis_list[0] <= calc_axis[0]:
            print("ok")
            limit_flag[0] = 0
        elif axis_list[0] > calc_axis[0]:
            print("over")
            limit_flag[0] = 1
    
    return angle_back_list, limit_flag, calc_axis


#データセットのリスト、x座標,y座標,z座標,順逆の選択
def branch(dataset, axis_list, angle_list,for_or_inv):
    #print(axis_list)
    unit_name = dataset[0][8]
    
    return_angle_list = []
    return_limit = 0
    return_axis = []

    if unit_name == "parallel_link":
        if for_or_inv == "inverted":
            #csvの中身を関数に代入
            La = dataset[0][9]
            Lb = dataset[1][9]
            Lr = dataset[2][9]
            Xp = axis_list[0]
            Yp = axis_list[1]
            
            alpha_angle, beta_angle = parallel_link_inv_kine(La, Lb, Lr, Xp, Yp)
            return_angle_list.append(alpha_angle)
            return_angle_list.append(beta_angle)

            Xaxis, Yaxis = parallel_link_kine(La, Lb, Lr, alpha_angle, beta_angle)
            return_axis.append(Xaxis)
            return_axis.append(Yaxis)
            
            return return_angle_list, return_limit, return_axis
            #return return_angle_list, return_limit,return_axis
        
    elif unit_name == "wheel1":
        if for_or_inv == "rotate":
            return [],0,[]
        
    elif unit_name == "one_link":
        if for_or_inv == "inverted":
            return_angle_list, return_limit,return_axis = one_link_arm_inv(dataset,axis_list)
            #print(return_angle_list)
            return return_angle_list, return_limit,return_axis

#branch("平行リンク", "inv")
