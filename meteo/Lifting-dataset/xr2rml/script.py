

import pandas as pd
from pandas import DataFrame
from os import listdir
from os.path import isfile, join
import datetime
import pymongo
from pymongo import MongoClient
import sys
import json


def synop_to_df(filepath):
  values = list()
  with open(filepath, "r") as file_obs:
      for line in file_obs.readlines():
        values.append(line.strip("\n").split(";"))
      column_label = values[0]
      print(column_label)
      #column_label =["_".join(x.strip("\"").strip("\n").split(" ")) for x in values[0]]
      del values[0]
      df = DataFrame(values, columns=column_label)
      df.drop(df.columns[-1], axis=1, inplace=True)
      df["dateF"] = pd.to_datetime(df["date"], infer_datetime_format=True)
  return df

print (synop_to_df(str(sys.argv[1])).head())