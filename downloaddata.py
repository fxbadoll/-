# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 17:04:33 2021

@author: Alien-m15
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from WindPy import *
w.start()

date_st = '2021-01-01'
date_end = '2021-10-17'

date_all = w.tdays(date_st, date_end).Data[0]

conv_sec_id_lt=[]
conv_sec_name_lt=[]

for i in date_all:

    date_1 = i.strftime("%Y-%m-%d")
    conv_sec_id = w.wset("sectorconstituent","date="+date_1+";windcode=000832.CSI").Data[1]
    conv_sec_name = w.wset("sectorconstituent","date="+date_1+";windcode=000832.CSI").Data[2]
    
    conv_sec_id_lt.append(conv_sec_id)
    conv_sec_name_lt.append(conv_sec_name)

conv_sec_id_pd = pd.DataFrame(conv_sec_id_lt,index = date_all)
conv_sec_name_pd = pd.DataFrame(conv_sec_name_lt,index = date_all)

path = r'D:\downloaddata'
conv_sec_id_pd.to_excel(path+"/conv_sec_id.xlsx")
conv_sec_name_pd.to_excel(path+"/conv_sec_name.xlsx")


conv_prem_ratio = []
conv_clause_prc = []
conv_under_code = []
for i in range(conv_sec_id_pd.shape[0]):
    date_1 = date_all[i].strftime("%Y-%m-%d")
    con_id = list(conv_sec_id_pd.iloc[i,:].dropna())
    con_val_stk = w.wss(con_id, "convpremiumratio","tradeDate="+date_1).Data[0]
    con_clause_prc = w.wss(con_id, "clause_conversion2_swapshareprice", "tradeDate="+date_1).Data[0]
    
    con_under_code = w.wss(con_id, "underlyingcode", "tradeDate="+date_1).Data[0]
    
    conv_prem_ratio.append(con_val_stk)
    conv_clause_prc.append(con_clause_prc)
    conv_under_code.append(con_under_code)
    
conv_prem_ratio_pd=pd.DataFrame(conv_prem_ratio)
conv_clause_prc_pd = pd.DataFrame(conv_clause_prc)
conv_under_code_pd = pd.DataFrame(conv_under_code)

conv_prem_ratio_pd.to_excel(path+"/conv_prem_ratio.xlsx")
conv_clause_prc_pd.to_excel(path+"/conv_clause_prc.xlsx")
conv_under_code_pd.to_excel(path+"/conv_under_code.xlsx")

under_prc_lt=[]
con_id_lt = []
for i in range(conv_under_code_pd.shape[0]):
    date_1 = date_all[i].strftime("%Y-%m-%d")
    con_id = list(conv_under_code_pd.iloc[i,:].dropna().unique())
    con_id_lt.append(con_id)
    under_prc = w.wss(con_id, "close", "tradeDate="+date_1).Data[0]
    under_prc_lt.append(under_prc)
    
con_id_pd=pd.DataFrame(con_id_lt)
under_prc_pd = pd.DataFrame(under_prc_lt)    
con_id_pd.to_excel(path+"/under_code.xlsx")
under_prc_pd.to_excel(path+"/underclose.xlsx")
