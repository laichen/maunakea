# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 10:55:47 2021

@author: dx.lai
"""


# #作者
# #生姜用户
# # 以sin(x)和e^(-x)为例，用python3实现数学建模中多个函数求交点
# import numpy as np
# import math
# from matplotlib import pyplot as plt 
# x1=[]
# y1=[]
# x2=[]
# y2=[]
# a=np.linspace(0,10,1000)
# def line1(x1):
#     y1=math.sin(x1)
#     return y1
# def line2(x2):
#     y2=math.exp(-x2)
#     return y2
# def f3(k):
#     y3=math.sin(k)
#     return y3
# def f4(k):
#     y4=math.exp(-k)
#     return y4
# plt.figure("sin(x) & e^(-x) function")
# for i in a:
#     x1.append(i)
#     y1.append(line1(i))
#     x2.append(i)
#     y2.append(line2(i))
# x_position=0
# y_position=0
# plt.scatter(x_position,y_position , marker = 'x',color = 'black', s = 40 ,label = 'origin')
# j=0
# for k in a:
#      y5=f3(k)-f4(k)
#      if math.fabs(y5)<0.005:         
#          j=j+1 
#          plt.scatter(k ,f4(k) , marker = '*',color = 'green', s = 40 ,label = 'intersection'+str(j))
#          plt.text(k ,f4(k) ,(round(k,4),round(f4(k),4)),color='green')
# plt.text(2.7,0.75, "y=sin(x)", weight="bold", color="blue")         
# plt.plot(x1, y1, color='blue', label="sin(x)")
# plt.text(4.5,0.1, "y=e^(-x)", weight="bold", color="red") 
# plt.plot(x2, y2, color='red', label="e^(-x)")
# plt.title("sin(x) & e^(-x) function")
# plt.legend()
# plt.show()


import numpy as np
import math
from matplotlib import pyplot as plt 

#设U臂转动时间为15s半圈，由于对称性，取其一半7.5s。
#考虑到7.5s时直线斜率无限大，需要专门处理，暂取7s，分成10步
t = np.linspace(0,7,100)

#U臂的拍摄方向的线（簇）由角度tan（th）和截距b确定。
#在特定角度下，取一系列截距b。 
#考虑到牙弓的深度一般在5左右，暂时先取-5为最大截距，正方向为1，分100步
b = np.linspace(-5,1,100)

#确定关系的定义域和定义域的精细度
x = np.linspace(-3,3,100)






def theta_m(t):
    "定义U臂转动的角度"
    th = np.pi*t/15 + np.pi/2
    return th


def lines_m(th,b,x):
    "定义U臂转动时的投影直线"
    lines = math.tan(th)*x + b
    return lines    

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
    


#二次方牙弓拟合曲线
dental_2 = np.poly1d([0.7474, 0.0635, -5.4247])
#四次方牙弓拟合曲线
dental_4 = np.poly1d([0.1021, 0.0292, 0.1151, -0.0396, -4.8448])


def cal_distance(p1, p2):
    "计算平面上两点的欧氏距离"
    l = math.sqrt(math.pow((p2[0] - p1[0]), 2) + math.pow((p2[1] - p1[1]), 2))
    return l


 
def Equidistance(t,b,x,dental):
    '''计算等距情况下的数值解。其中:
    t为时间区间（array），
    b为截距区间（array），
    x为定义域区间（array），
    '''
    
    
    #ATD Axis to Tooth Distance
    ATD_aim = 3
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
                    
                    print(k,dental(k),j)
                    #计算交点和截距点的距离
                    atd = cal_distance((k,dental(k)),(0,j))
                    #记录所有信息（全部信息列表）
                    intersect_and.append((i,theta_m(i),j,k,dental(k),atd))
                    m = m + 1 
                    
            #如果列表不为空，说明存在交点。可进行下一步
            if intersect_and:          
                y2 = intersect_and[m][5]-ATD_aim
                #满足判定条件，即可认为该截距条件下的特定直线，满足等距要求。
                if math.fabs(y2) < 0.005:
                    #记录此时的时间，和截距位置，用于后续拟合直行电机运动轨迹
                    time_list.append(i)
                    intercept_list.append(j)
                    
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
                if math.fabs(y1) < 0.005:
                    
                    print(k,dental(k),j)
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
                k2 = math.tan(intersect_and[m][1])
                #若两线垂直，则斜率相乘为-1，再+1 即为0
                y2 = k1*k2 + 1
                #满足判定条件，即可认为该截距条件下的特定直线，满足等距要求。
                if math.fabs(y2) < 0.005:
                    #记录此时的时间，和截距位置，用于后续拟合直行电机运动轨迹
                    time_list.append(i)
                    intercept_list.append(j)
                    
            else:
                print("No intersection")
                
    return time_list, intercept_list
        

                
        
def main():
    #换不同函数，选择两种情形计算时间-截距的关系，返回两个列表
    time_list, intercept_list = Equidistance(t,b,x,dental_4)
    plt.scatter(time_list,intercept_list)


if __name__ == "__main__":
    main()        
        

    

























