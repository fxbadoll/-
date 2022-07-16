# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 16:59:47 2022
利用之前分析的半年报和年报数据，将选出的基金数据按照时间顺序连接起来
@author: xfugm
"""
import pandas as pd

year = [202112,202106,202012,202006,201912,201906]
path = r'D:\基金分析\-\\'

df = {}
for dt in year:
    df[dt] = pd.read_csv(path+'基金'+str(dt)+'持仓分析.csv')
    

fund_code = '000547.OF'
fund_data = {}

for dt in year:
    fund_data[dt] = df[dt][df[dt]['基金代码'] == fund_code]
    fund_data[dt] = fund_data[dt].squeeze()    

fund_pd = pd.DataFrame.from_dict(fund_data, orient='index')
fund_pd.to_csv(path+'基金因子分析\\'+fund_code+'.csv',encoding = 'utf-8-sig')