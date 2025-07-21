from apps.db.connections.connection_string import conn_str
from apps.db.dict_fetch.fetch_data import dictfetchall
import pyodbc
import pandas as pd
from datetime import datetime

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

class fetch_store_data:
    def __init__(self):
        super().__init__()
    def store_data(self):
        try:
            cursor.execute("SELECT * FROM Stores")
            stores_data = dictfetchall(cursor)
            df = pd.DataFrame(stores_data)

            cursor.execute("SELECT s.*, r.region_name FROM Stores s LEFT JOIN Regions r ON s.region_id = r.id")
            rs1 = dictfetchall(cursor)
            dfs = pd.DataFrame(rs1)

            dfs['region_id'] = dfs['region_name']
            dfs['created_at'] = pd.to_datetime(dfs['created_at'])
            dfs['created_at'] = dfs['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            dfs['updated_at'] = pd.to_datetime(df['updated_at'])
            dfs['updated_at'] = dfs['updated_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            dfs.rename(columns={'store_id': 'KSA'}, inplace=True)
            dfs.rename(columns={'store_name': 'Store'}, inplace=True)
            dfs.rename(columns={'region_id': 'Region'}, inplace=True)
            dfs.rename(columns={'is_head_office': 'Head Office'}, inplace=True)
            dfs.rename(columns={'created_at': 'Created At'}, inplace=True)
            dfs.rename(columns={'updated_at': 'Updated At'}, inplace=True)
            dfs.rename(columns={'created_by_id': 'Created By'}, inplace=True)
            dfs.rename(columns={'updated_by_id': 'Updated By'}, inplace=True)
            dfs = dfs.drop('Created By', axis=1)
            dfs = dfs.drop('Updated By', axis=1)
            dfs = dfs.drop('region_name', axis=1)
            dfs = dfs.to_html(index=False)
            return dfs
        except:
            dfs = "No Data Found"
            return dfs

def store_data_test():
    cursor.execute("SELECT * FROM Stores")
    stores_data = dictfetchall(cursor)
    df = pd.DataFrame(stores_data)
    cursor.execute("SELECT s.*, r.region_name FROM Stores s LEFT JOIN Regions r ON s.region_id = r.id")
    rs1 = dictfetchall(cursor)
    dfs = pd.DataFrame(rs1)
    print(dfs.to_string())

    dps = dfs['region_id'] = dfs['region_name']
    print(dps)
    dfs['created_at'] = pd.to_datetime(dfs['created_at'])
    dfs['created_at'] = dfs['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
    dfs['updated_at'] = pd.to_datetime(df['updated_at'])
    dfs['updated_at'] = dfs['updated_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
    dfs.rename(columns={'store_id': 'KSA'}, inplace=True)
    dfs.rename(columns={'store_name': 'Store'}, inplace=True)
    dfs.rename(columns={'region_id': 'Region'}, inplace=True)
    dfs.rename(columns={'is_head_office': 'Head Office'}, inplace=True)
    dfs.rename(columns={'created_at': 'Created At'}, inplace=True)
    dfs.rename(columns={'updated_at': 'Updated At'}, inplace=True)
    dfs.rename(columns={'created_by_id': 'Created By'}, inplace=True)
    dfs.rename(columns={'updated_by_id': 'Updated By'}, inplace=True)
    dfs = dfs.drop('Created By', axis=1)
    dfs = dfs.drop('Updated By', axis=1)
    dfs = dfs.to_html(index=False)


    # if i in df2.values:
    #     print('YAY')


    #print(df)
# store_data_test()