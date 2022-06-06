# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 18:38:28 2022

@author: xfugm
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


def rolling_regress(fund, fund_data, index_data, rolling_days):
    r2 = {}
    coef = {}
    df = pd.concat([fund_data[fund]*100,index_data],axis=1)
    df.index = pd.DatetimeIndex(fund_data.index)
    df = df.drop('_id',axis=1)
    df = df.drop('日期',axis=1)
    for i in range(df.shape[0] - rolling_days):
        date = df.index[i+rolling_days]   
        data = df.iloc[i:i+rolling_days, :].astype('float64')
        A1 = data.iloc[:, 1:]
        b1 = data.iloc[:, 0]   
        model = my_general_linear_model_func(A1,b1)
        coef[date] = model.x
        r2[date] = []
        r2[date].append(list(model.x))
    return r2