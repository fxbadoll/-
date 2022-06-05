# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 18:13:29 2022

@author: xfugm
"""


from pymongo import MongoClient
import pandas as pd
# Requires the PyMongo package.
# https://api.mongodb.com/python/current

client = MongoClient('mongodb://localhost:27017/')
db = client["Research"]
colln = db["基金库交易能力match"]
# Requires the PyMongo package.
# https://api.mongodb.com/python/current

# Requires the PyMongo package .
# https://api.mongodb.com/python/current

filter={
    'fund repo': {
        '$elemMatch': {
            '$ne': None
        }
    }
}
project={
    '_id': 0
}

result = client['Research']['基金库交易能力match'].find(
  filter=filter,
  projection=project
)

result_pd = pd.DataFrame(list(result))