#!/usr/bin/env python
# coding: utf-8

# In[1]:

# In[ ]:

import pandas as pd
from pandas import DataFrame
from os import listdir
from os.path import isfile, join
import datetime
import pymongo
from pymongo import MongoClient
import sys

# In[ ]:


#dirpath = str(sys.argv[2])
#print(dirpath)

# In[ ]:

#dirpath = '/Users/nyacaoub/Documents/weather-reports-archives/2019'
def get_files(dirpath): 
    files = [dirpath+f for f in listdir(dirpath) if (isfile(join(dirpath, f)) and ".DS_Store" not in f)]
    return files 

def synop_to_df(filepath):
  values = list()
  with open(filepath, "r") as file_obs:
      for line in file_obs.readlines():
        values.append(line.strip("\n").split(";"))
      column_label = values[0]
      #column_label =["_".join(x.strip("\"").strip("\n").split(" ")) for x in values[0]]
      del values[0]
      df = DataFrame(values, columns=column_label)
      df["dateF"] = pd.to_datetime(df["date"], infer_datetime_format=True)
  return df

# In[ ]:
#print(get_files(str(sys.argv[1])))


def insert_mongoDB(col_name, dirpath):
    for filepath in get_files(dirpath):
        df = synop_to_df(filepath)
        df.to_csv(filepath, index=False, header=True)
    conn = pymongo.MongoClient("localhost" , 27017)
    for filepath in get_files(dirpath):
        data = pd.read_csv(filepath)
        conn['Meteo-France'][col_name].insert_many(data.to_dict('records'))

# In[ ]:

insert_mongoDB(str(sys.argv[1]), str(sys.argv[2]))

