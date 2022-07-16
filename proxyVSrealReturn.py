# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 15:19:40 2022
主要计算根据持仓计算的代理组合和实际组合净值的对比，并计算换手效率 （代理组合收益 - 真实组合收益)/换手率，再进行排名；


@author: xfugm
"""
## 本部分计算代理组合半年度内的收益情况，就是假设半年度或年度持仓不变，向后看收益水平
from csvtodb import *
from WindPy import *

year = '202106'
path = r'D:\基金分析\-\\'



data  = pd.DataFrame()
url1 = 'mongodb://localhost:27017/'
db_name = 'Research'
collection_name = 'fund_stock_position_'+year


data = db_to_pandas(url1, db_name, collection_name)

percent = data['占净值比(%)']
stk_forward_ret = data['向前半年涨跌幅']
fund_code_proxy = data['代码']

def percent_data(data,percent):
    return data*percent/100

fund_stk_ret = percent_data(stk_forward_ret, percent)

data_2 = pd.concat([fund_code_proxy,fund_stk_ret],axis = 1)
data_2.columns = ['fund_code','stk_ret']
fund_proxy = data_2.groupby('fund_code').agg('sum')



## 基金换手率数据是向前看的数据，所以要和上部分差半年，读取本基金的收益率情况

year_2 = '202112'

data  = pd.DataFrame()
url1 = 'mongodb://localhost:27017/'
db_name = 'Research'
collection_name = 'fund_turnover_'+year

data = db_to_pandas(url1, db_name, collection_name)
fund_code = data['基金代码']
fund_turnover = data['换手率']
fund_ret = data['本半年涨跌幅']

fund_real_ret = pd.concat([fund_turnover,fund_ret],axis=1)
fund_real_ret.index = fund_code

fund_compare = fund_proxy.join(fund_real_ret)

import numpy as np

fund_trade_eff = pd.DataFrame((np.array(fund_compare['本半年涨跌幅']) - np.array(fund_compare['stk_ret']))/np.array(fund_compare['换手率']))
fund_trade_eff.index = fund_compare.index
fund_trade_eff.columns = ['交易效率']
fund_compare_2 = fund_compare.join(fund_trade_eff)
fund_compare_2['report_date'] = year
fund_compare_2['交易效率排名'] = fund_trade_eff.rank()/fund_trade_eff.shape[0]


## 从文件中读取数据，并将计算出来的,再更新数据回到文件夹

data_all = pd.read_csv(r'D:\基金分析\-\基金'+year+'持仓分析.csv',encoding = 'utf-8-sig')
data_all.index = data_all['基金代码']

data_to_join = fund_compare_2[['交易效率','交易效率排名']]
if '交易效率' in data_all.columns:
    data_all = data_all.drop(['交易效率','交易效率排名'],axis=1)
data_all_2 = data_all.join(data_to_join)

data_all_2.to_csv(r'D:\基金分析\-\基金'+year+'持仓分析.csv',encoding = 'utf-8-sig')

