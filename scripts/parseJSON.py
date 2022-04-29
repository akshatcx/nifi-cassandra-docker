#!/usr/bin/python3
import sys
import pandas as pd
import re
KEYSPACE = 'dfs'
DTYPES = {
    'float64': 'float',
    'int64': 'float',
    'string': 'text',
    'datetime64[ns]': 'timestamp',
    'object' : 'text'
}

specialChars = '[?*()&-/: ]'
# df = pd.read_csv("../sample_files/Patient_Info.csv")
df = pd.read_json(sys.stdin)
tableName = re.sub(specialChars ,'_' ,str(sys.argv[1]).split('.')[0]) 

maxUniqueNumber = 0
maxUniqueColumn = ""

for idx, column in enumerate(df.columns):
    df.rename (columns={column:re.sub(specialChars ,'_' ,column )},inplace=True)

for column in df:
    if df[column].nunique() > maxUniqueNumber:
        maxUniqueNumber = df[column].nunique()
        maxUniqueColumn = column

# create table
print(f"CREATE TABLE IF NOT EXISTS {KEYSPACE}.{tableName} ({', '.join([col + ' ' + DTYPES[str(df.dtypes[col])] for col in df.columns])}, PRIMARY KEY ({maxUniqueColumn}));")

# insert rows
def get_values(row):
    values = []
    for col in df.columns:
        if DTYPES[str(df.dtypes[col])] == 'text' or DTYPES[str(df.dtypes[col])] == 'timestamp': values.append(f"'{str(row[col])}'")
        else: values.append(str(row[col]))
    return values

for i, row in df.iterrows():
    print(f"INSERT INTO {KEYSPACE}.{tableName} ({', '.join(df.columns)}) VALUES ({', '.join(get_values(row))});")
