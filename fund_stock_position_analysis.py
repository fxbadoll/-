# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 14:16:15 2022
这个程序，将数据库中的按年度的权益基金持仓，进行因子分析，主要是整理数据和对因子进行排名，分析并输出最终结果

@author: xfugm
"""
from csvtodb import *


year = '201906'
data  = pd.DataFrame()
url1 = 'mongodb://localhost:27017/'
db_name = 'Research'
collection_name = 'fund_stock_position_'+year


data = db_to_pandas(url1, db_name, collection_name)

percent = data['占净值比(%)']
mkt_val = data['市值乘后']
est_pe = data['PE乘后']

est_grow_raw = data['万德一致预期增速']
static_pe_raw = data['静态PE']

gross_profit_margin_raw = data['毛利率']
profit_margin_raw = data['净利率']
roe_raw = data['ROE']
roic_raw = data['ROIC']
profit_quality_raw = data['经营现金流净额/净利润']
asset_liab_raw = data['资产负债率']
pb_raw = data['静态PB']

##用来将单支股票的各项指标*持仓占比%
def percent_data(data,percent):
    return data*percent/100


## 计算用持仓比例乘积后的各项指标

est_grow = percent_data(est_grow_raw, percent)
static_pe = percent_data(static_pe_raw, percent)
gross_profit_margin = percent_data(gross_profit_margin_raw, percent)
profit_margin = percent_data(profit_margin_raw, percent)
roe = percent_data(roe_raw, percent)
roic = percent_data(roic_raw, percent)
profit_quality = percent_data(profit_quality_raw, percent)
asset_liab = percent_data(asset_liab_raw, percent)
pb = percent_data(pb_raw, percent)

fund_code = data['代码']
fund_name = data['名称']
fund_report_date = data['报告期']
fund_stk_code = data['股票代码']
fund_stk_name = data['股票简称']

data_2 = pd.concat([fund_code,fund_name,fund_report_date,fund_stk_code,fund_stk_name,mkt_val,est_pe,est_grow,
                       static_pe,gross_profit_margin,profit_margin,roe,roic,profit_quality,asset_liab,pb]
                      ,axis=1)
## 如果列有变化需要更新
data_columns = ['fundcode','fundname','fundreportdate','fundstkcode','fundstkname','总市值','一致预期PE',
           '每股一致预期增速','静态pe','毛利率','净利率','roe','roic','经营现金流净额/净利润',
           '资产负债率','静态pb']
data_2.columns = data_columns


## 基础数据搞定后，开始用groupby进行分组统计
data_2_group_sum = data_2.groupby('fundcode').agg('sum')
data_2_group_rank = data_2_group_sum.rank()/data_2_group_sum.shape[0]


## 如果列有变化需要更新
data_columns_rank = ['总市值排名','一致预期PE排名','每股一致预期增速排名','静态pe排名','毛利率排名','净利率排名','roe排名','roic排名',
                     '经营现金流净额/净利润排名','资产负债率排名','静态pb排名']

data_2_group_rank.columns = data_columns_rank
# 基金风格因子中，总市值，一致预期PE，静态PE，每股收益一致预期增速，毛利率、净利率、ROE、ROIC、经营现金流/净利润、资产负债率；
data_2_holdings_result = pd.concat([data_2_group_sum,data_2_group_rank],axis=1)




# 基金风格因子中，集中度的绝对值和排名 其中包括股票个数，前十大股票占比、前三大行业占比
data_2_group_count = data_2.groupby('fundcode').agg('count')



# 对每支基金前top_num大重仓的持股比例进行统计
def add_top10_position(group,top_num=10):
    group = group.sort_values('占净值比(%)',ascending = False)
    group['prop_top'] = group['占净值比(%)'].iloc[:top_num].sum()
    return group['prop_top']

data_2_top_sum = data.groupby('代码').apply(add_top10_position)
data_2_top_sum_unique = data_2_top_sum.groupby('代码').agg('mean')


def add_top3_position(group,top_num=3):
    group = group.sort_values('占净值比(%)',ascending = False)
    group['prop_top'] = group['占净值比(%)'].iloc[:top_num].sum()
    return group['prop_top']

#对每支基金前3大行业占比统计计算
data_2_group_industry = data.groupby(['代码','中信一级行业']).agg('sum').sort_values(['代码','占净值比(%)'],ascending = False)

data_2_group_industry_top3 = data_2_group_industry.groupby('代码').apply(add_top3_position)
data_2_group_industry_top3_unique = data_2_group_industry_top3.groupby('代码').agg('mean')

data_2_jizhongdu = pd.concat([data_2_group_count['fundname'],data_2_top_sum_unique,data_2_group_industry_top3_unique],axis=1)

data_2_jizhongdu.columns = ['股票个数','前十大股票占比','前三大行业占比']
data_2_jizhongdu_rank = data_2_jizhongdu.rank()/data_2_jizhongdu.shape[0]
data_2_jizhongdu_rank.columns = ['股票个数排名','前十大股票占比排名','前三大行业占比排名']
data_2_jizhongdu_result = pd.concat([data_2_jizhongdu,data_2_jizhongdu_rank],axis=1)

#读取基金换手率数据并整理
collection_name = 'fund_turnover_'+year
data_turnover = db_to_pandas(url1, db_name, collection_name).dropna()
data_turnover_rank = data_turnover.rank()/data_turnover.shape[0]
data_turnover_rank.columns = ['_id', '基金代码', '买入股票总额排名', '卖出股票总额排名', '上一报告规模排名', '本期报告规模排名', '换手率排名']
data_turnover_result = pd.concat([data_turnover['换手率'],data_turnover_rank['换手率排名']],axis=1)
data_turnover_result.index = data_turnover['基金代码']


data_tot_result = pd.concat([data_2_holdings_result,data_2_jizhongdu_result,data_turnover_result],axis=1)




data_tot_result.to_csv(r'D:\基金分析\-\基金'+year+'持仓分析.csv',encoding = 'utf-8-sig')

