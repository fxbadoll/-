# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 17:37:57 2022
基金回归的主函数，从数据库中读出数据，并进行滚动的带约束回归，并写出到文件夹

@author: xfugm
"""
from csvtodb import *
from db_aggregate import *
from regress_with_contraint import *
import seaborn as sns
import matplotlib.pyplot as plt

## 读取数据库中的数据，分别读取基金日收益和指数日收益

db_name = "Research"
collection_name = "fund_daily_return"
url1 = 'mongodb://localhost:27017/'

fund_pd = db_to_pandas(url1, db_name, collection_name)
collection_name = "fund_repo"
fund_name = db_to_pandas(url1, db_name, collection_name)

fund_code_lt = list(fund_name['fund_code'])

fund_to_regr = fund_pd[fund_code_lt]

collection_name = "juchao_index"
juchao_index_pd = db_to_pandas(url1, db_name, collection_name)


# 按照30天进行滚动回归分析，日期从开始到结束，并输出到文件夹

rolling_days=30
intercept=False

date_begin='2020-1-3'
date_end='2022-6-6'

x = {}
r2 = {}
coef = {}

date_index = juchao_index_pd['日期']
fund_to_regr.index = date_index
fund_to_regr.index = pd.DatetimeIndex(fund_to_regr.index)
juchao_index_pd.index = pd.DatetimeIndex(fund_to_regr.index)
fund_to_regr = fund_to_regr.loc[(fund_to_regr.index>=date_begin) & (fund_to_regr.index<=date_end), :]*100
juchao_index_pd = juchao_index_pd.loc[(juchao_index_pd.index>=date_begin) & (juchao_index_pd.index<=date_end), :]


# fund_to_regr[fund_to_regr.isnull()] = 0 
# juchao_index_pd[juchao_index_pd.isnull()] = 0 


fund_list = list(fund_to_regr.columns)
fund_list = ['000390.OF']
r = {}    
for fund in fund_list:

    r2 = rolling_regress(fund, fund_to_regr, juchao_index_pd, rolling_days)
    r[fund] = []
    r[fund] = r2


regress_info = ['xiaopanjiazhi','xiaopanchengzhang','dapanjiazhi','dapanchengzhang']

date_key = list(r[fund])
r_test = {}
for fund in fund_list:
    r_temp = r[fund]
    for i in date_key:
        r_test[i] = r_temp[i][0]
    r_test_pd = pd.DataFrame(r_test.values(),columns = regress_info,index = r_test.keys())
    # r_test_pd = pd.DataFrame.from_dict(r_test,orient='index')
    url = r"C:\Users\xfugm\Desktop\ICBC_基金研究\回归数据\\" + fund + '.csv' 
    r_test_pd.to_csv(url)




    
