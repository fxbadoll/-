# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 09:27:13 2022

@author: steve
"""

import pandas as pd
from statsmodels.formula.api import glm
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from statsmodels.formula.api import glm
from shgo import*


def my_general_linear_model_func(A1,b1):
    num_x = np.shape(A1)[1]
    def my_func(x):
        ls = 0.5*(b1-np.dot(A1,x))**2
        result = np.sum(ls)
        return result
    def g1(x):
        return np.sum(x) #sum of X >= 0
    def g2(x):
        return 1-np.sum(x) #sum of X <= 1
    cons = ({'type': 'ineq', 'fun': g1}
            ,{'type': 'ineq', 'fun': g2})
    x0 = np.zeros(num_x)
    bnds = [(0,1)]
    for i in range(num_x-1):
        bnds.append((0,1))
    res1 = shgo(my_func, 
                bounds = bnds, 
                constraints=cons)
    
    return res1

df=pd.read_csv(r"C:\Users\xfugm\Desktop\ICBC_基金研究\juchao.csv")
rolling_days=20
intercept=False
df.index = df.iloc[:, 0]  # 将日期变为索引
df = df.iloc[:, 1:]             
df[df.isnull()] = 0  # 缺失值填充        
df = df.astype(float)  # 将数据框object格式转换为float
# dateTransfer = np.vectorize(self._dateTransfer)   # 向量化日期转换函数                
# df.index = dateTransfer(df.index) # 转换索引日期格式          
df.index = pd.DatetimeIndex(df.index)
date_begin='2019-1-3'
date_end='2022-5-13'
x = {}
r2 = {}
coef = {}
df = df.loc[(df.index>=date_begin) & (df.index<=date_end), :]   # 按照参数给定起始、截止时间选择数据
df = df.sort_index(ascending=True)  # 按日期升序排序


for i in range(df.shape[0] - rolling_days):
            date = df.index[i+rolling_days]   
            data = df.iloc[i:i+rolling_days, :]
            A1 = data.iloc[:, 1:]
            b1 = data.iloc[:, 0]   
            model =  my_general_linear_model_func(A1,b1)
            coef[date] = model.x
            r2[date] = []
            r2[date].append(list(model.x))
x = pd.DataFrame.from_dict(r2,orient='index')
coef = pd.DataFrame.from_dict(coef, orient='index')
coef.to_csv('D:/python代码/回归系数带约束.csv',encoding='utf-8')