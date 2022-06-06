# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 18:18:23 2022

@author: xfugm
"""
import sys
import pandas as pd
import json
from pymongo import MongoClient
import imp

imp.reload(sys)

# Requires the PyMongo package.
# https://api.mongodb.com/python/current




def mongodb_aggreage(url,db_name,collection_name,filters):
    client = MongoClient(url)
    result = client[db_name][collection_name].aggregate(filters)
    return result

if __name__ == "_main_":
    url = 'mongodb://localhost:27017/'
    db_name = "Research"
    collection_name = 'juchao_index'
    filters = [
        {
            '$project': {
                '日期': 1
            }
        }
    ]
    result = mongodb_aggreage(url, db_name, collection_name, filters)

