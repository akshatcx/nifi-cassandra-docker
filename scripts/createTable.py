#!/usr/bin/python3
import pandas as pd
import sys
file = pd.read_csv(sys.stdin)

KEYSPACE = 'dfs'
# file = pd.read_csv("./monthly_data1.csv")

maxUniqueNumber = 0
maxUniqueColumn = ""
for column in file:
    if(file[column].nunique()>maxUniqueNumber):
        maxUniqueNumber = file[column].nunique()
        maxUniqueColumn = column

pandasDataTypeToCassandraDataType = {
    'float64':'float',
    'string':'text',
    'date':'timestamp',
    'object' : 'text'
}

command = f"CREATE TABLE IF NOT EXISTS {KEYSPACE}."+str(sys.argv[1]).split('.')[0]+"  ("
for i in file.columns:
    command = command + str(i) + " " + pandasDataTypeToCassandraDataType[str(file.dtypes[i])] + ","
command = command + "PRIMARY KEY (" + maxUniqueColumn +  "));"


print(command)

# Todo
# name
# primary key
# data type
# keyspace


# CREATE TABLE data.precipdataa (date date, precip float, PRIMARY  KEY (date));
# print("CREATE TABLE data.sensor_data (station_id text, sensor_id text, tps timestamp, val float, PRIMARY KEY ((station_id, sensor_id), tps));")
