#!/usr/bin/python3
import sys
import pandas as pd

KEYSPACE = 'dfs'
DTYPES = {
    'float64': 'float',
    'string': 'text',
    'datetime64[ns]': 'timestamp',
    'object' : 'text'
}

# df = pd.read_json("../sample_files/monthly_json.json")
df = pd.read_json(sys.stdin)
tableName = str(sys.argv[1]).split('.')[0]

maxUniqueNumber = 0
maxUniqueColumn = ""

for column in df:
    if df[column].nunique() > maxUniqueNumber:
        maxUniqueNumber = df[column].nunique()
        maxUniqueColumn = column

# create table
print(f"CREATE TABLE IF NOT EXISTS {KEYSPACE}.{tableName} ({', '.join([col + ' ' + DTYPES[str(df.dtypes[col])] for col in df.columns])}, PRIMARY KEY ({maxUniqueColumn}));")

# insert rows
# INSERT INTO dfs.dummy_data (date , precip) VALUES ('1893-01-01' , 1.32);
def get_values(row):
    values = []
    for col in df.columns:
        if DTYPES[str(df.dtypes[col])] == 'text' or DTYPES[str(df.dtypes[col])] == 'timestamp': values.append(f"'{str(row[col])}'")
        else: values.append(str(row[col]))
    return values

for i, row in df.iterrows():
    print(f"INSERT INTO {KEYSPACE}.{tableName} ({', '.join(df.columns)}) VALUES ({', '.join(get_values(row))});")
