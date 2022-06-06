# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 15:54:04 2022

从读取的csv文件，向mongodb里面写入json类型，从mongodb读出数据并转化为pandas

@author: xfugm
"""
import sys
import pandas as pd
import json
from pymongo import MongoClient
import imp

imp.reload(sys)

## read in csv and to mongodb##
def csv_to_db(url1,url2,db_name,collection_name):

    client = MongoClient(url1)
    db = client[db_name]
    colln = db[collection_name]
    raw_data = pd.read_csv(url2)
    colln.insert_many(json.loads(raw_data.T.to_json()).values())
    return colln



##--------------------##
## read in mongodb 数据文件到pandas##

def db_to_pandas(url1,db_name,collection_name):
    client = MongoClient(url1)
    db = client[db_name]
    colln = db[collection_name]
    result = colln.find()
    result_pd = pd.DataFrame(list(result))
    return result_pd


def pandas_to_db(pandas,url1,db_name,collection_name):
    client = MongoClient(url1)
    db = client[db_name]
    colln = db[collection_name]
    colln.insert_many(json.loads(pandas.T.to_json()).values())
    return colln


if __name__ == '_main_':
    
    url1 = 'mongodb://localhost:27017/'
    url2 = r'D:\基金分析\-\市场基金日回报.csv'
    db_name = "Research"
    collection_name = "fund_daily_return"
    colln = csv_to_db(url1, url2, db_name, collection_name)
    
    
    
    url2 = r'D:\基金分析\-\基金名单导入.csv'
    collection_name = 'fund_repo'
    colln2 = csv_to_db(url1, url2, db_name, collection_name)
    collection_name = "fund_daily_return"
    fund_pd = db_to_pandas(url1, db_name, collection_name)
    collection_name = "fund_repo"
    fund_name = db_to_pandas(url1, db_name, collection_name)
