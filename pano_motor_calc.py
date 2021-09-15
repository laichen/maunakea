# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 10:55:47 2021

@author: dx.lai

此程序旨在计算牙科机PANO模式下一维直行电机的运动曲线。
计算条件：
旋转机架半圈匀速旋转拍摄牙弓，速度为半圈15s
牙弓曲线：需作为下方输入参数输入
几何：默认直行电机运动方向为与牙弓中线重合，且以会厌指向门牙方向为负方向

"""


import numpy as np
import math
from matplotlib import pyplot as plt 


#------------------基本的定义域区间、牙弓曲线等输入参数--------------------------
 
#设U臂转动时间为15s半圈，由于对称性，取其一半7.5s。
#考虑到7.5s时直线斜率无限大，需要专门处理，暂取7s，分成100步
t = np.linspace(0,7,200)

#U臂的拍摄方向的线（簇）由角度tan（th）和截距b确定。
#在特定角度下，取一系列截距b。 
#考虑到牙弓的深度一般在5左右，暂时先取-5为最大截距，正方向为1，分100步
b = np.linspace(-5,1,200)

#确定关系的定义域和定义域的精细度,配合t，先取一半。
x = np.linspace(0,3,200)


#二次方牙弓拟合曲线
dental_2 = np.poly1d([0.7474, 0.0635, -5.4247])
#四次方牙弓拟合曲线
dental_4 = np.poly1d([0.1021, 0.0292, 0.1151, -0.0396, -4.8448])

#---下述注释部分定义函数可能有问题
# def dental_4(x):
#     "四次方牙弓拟合曲线"
#     #dental = 0.1021*x^4 + 0.0292*x^3 + 0.1151*x^2 - 0.0396*x - 4.8448
#     #上述书写仅为示意，不可用于代码。unsupported operand type(s) for ^: 'Mul' and 'Add'
#     dental = np.poly1d([0.1021, 0.0292, 0.1151, -0.0396, -4.8448])
#     return dental(x)

# def dental_2(x):
#     "二次方牙弓拟合曲线"
#     #dental = 0.7474*x^2 + 0.0635*x - 5.4247 
#     #上述书写仅为示意，不可用于代码。unsupported operand type(s) for ^: 'Mul' and 'Add'
#     dental = np.poly1d([0.7474, 0.0635, -5.4247])
#     return dental(x)



#---------------------------------- 工具函数  -------------------------
def theta_m(t):
    "定义U臂转动的角度"
    th = np.pi*t/15 + np.pi/2
    return th


def lines_m(th,b,x):
    "定义U臂转动时的投影直线"
    lines = (1/math.tan(th))*x + b
    return lines    


def cal_distance(p1, p2):
    "计算平面上两点的欧氏距离"
    l = math.sqrt(math.pow((p2[0] - p1[0]), 2) + math.pow((p2[1] - p1[1]), 2))
    return l




#------------------------------ 两种场景下的计算函数 ------------------------
def Equidistance(t,b,x,dental):
    '''计算等距情况下的数值解。其中:
    t为时间区间（array），
    b为截距区间（array），
    x为定义域区间（array），
    '''
        
    #ATD Axis to Tooth Distance
    ATD_aim = 2.5
    #用于统计的”全部信息列表“
    intersect_and = []
    #m用于统计“全部信息列表”的数据点index
    m= -1
    #求出的时间和截距的列表，用于函数返回
    time_list = []
    intercept_list = []
    
    #等间隔改变”时间-角度”，从而改变斜率
    for i in t:
        #在特定”时间-角度-斜率“情况下画出各种截距的线簇
        for j in b:
            #在特定斜率，特定截距的确定直线下，寻找与牙弓曲线的交点
            for k in x:
                y1 = lines_m(theta_m(i),j,k) - dental(k)
                #满足判定条件，即可认为是交点。判定条件精度可改变，下同。
                if math.fabs(y1) < 0.005:
                    
                    #print(k,dental(k),j)
                    #计算交点和截距点的距离
                    atd = cal_distance((k,dental(k)),(0,j))
                    #记录所有信息（全部信息列表）
                    intersect_and.append((i,theta_m(i),j,k,dental(k),atd))
                    m = m + 1 
                    
            #如果列表不为空，说明存在交点。可进行下一步
            if intersect_and:          
                y2 = intersect_and[m][5]-ATD_aim
                #满足判定条件，即可认为该截距条件下的特定直线，满足等距要求。
                if math.fabs(y2) < 0.01:
                    #记录此时的时间，和截距位置，用于后续拟合直行电机运动轨迹
                    time_list.append(intersect_and[m][0])
                    intercept_list.append(intersect_and[m][2])
                    print("found a line!")
                    
            else:
                print("No intersection")
        
            
    return time_list, intercept_list



def Normal(t,b,x,dental):
    '''计算法线情况下的数值解,其中:
    t为时间区间（array），
    b为截距区间（array），
    x为定义域区间（array）
    '''
    
    #用于统计的”全部信息列表“
    intersect_and = []
    #m用于统计“全部信息列表”的数据点index
    m = -1
    #求出的时间和截距的列表，用于函数返回
    time_list = []
    intercept_list = []
    
    
    #等间隔改变”时间-角度”，从而改变斜率
    for i in t:
        #在特定”时间-角度-斜率“情况下画出各种截距的线簇
        for j in b:
            #在特定斜率，特定截距的确定直线下，寻找与牙弓曲线的交点
            for k in x:
                y1 = lines_m(theta_m(i),j,k) - dental(k)
                #满足判定条件，即可认为是交点。判定条件精度可改变，下同。
                if math.fabs(y1) < 0.01:
                    
                    #print(k,dental(k),j)
                    #计算交点和截距点的距离
                    atd = cal_distance((k,dental(k)),(0,j))
                    #记录所有信息（全部信息列表）
                    intersect_and.append((i,theta_m(i),j,k,dental(k),atd))
                    m = m + 1 
            
            #如果列表不为空，说明存在交点。可进行下一步
            if intersect_and: 
                #利用 np.polyder 求牙弓曲线的导数k1，得出交点处的牙弓曲线的切线斜率
                k1 = np.polyder(dental,1)(intersect_and[m][3])  
                #直线的斜率
                k2 = 1/(math.tan(intersect_and[m][1]))
                #若两线垂直，则斜率相乘为-1，再+1 即为0
                y2 = k1*k2 + 1
                #满足判定条件，即可认为该截距条件下的特定直线，满足等距要求。
                if math.fabs(y2) < 0.01:
                    #记录此时的时间，和截距位置，用于后续拟合直行电机运动轨迹
                    time_list.append(intersect_and[m][0])
                    intercept_list.append(intersect_and[m][2])
                    print("found a line!")
                    
            else:
                print("No intersection")
                
    return time_list, intercept_list
        

                
 



# ---------------------------- 主函数 --------------------------------------       
def main():
    #换不同函数，选择两种情形计算时间-截距的关系，返回两个列表
    time_list, intercept_list = Equidistance(t,b,x,dental_4)
    print('time list is:',time_list)
    print ('intercept list is:', intercept_list)
    
    plt.scatter(time_list,intercept_list)


if __name__ == "__main__":
    main()        
        

    

























