#!/usr/bin/python3
import pandas as pd
import sys
file = pd.read_csv(sys.stdin)

# file = pd.read_csv("./monthly_data1.csv")
command = "CREATE TABLE data.precipdataa ("
for i in file.columns:
    command = command + str(i) + " " + "text" + ","
command = command + "PRIMARY KEY (" + "date" +  "));"
print(command)

# Todo
# name
# primary key
# data type 
# keyspace 


# CREATE TABLE data.precipdataa (date date, precip float, PRIMARY  KEY (date));
# print("CREATE TABLE data.sensor_data (station_id text, sensor_id text, tps timestamp, val float, PRIMARY KEY ((station_id, sensor_id), tps));")