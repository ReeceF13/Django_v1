from apps.db.connections.connection_string import conn_str
from apps.db.dict_fetch.fetch_data import dictfetchall
import pyodbc
import pandas as pd
from datetime import datetime

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

class fetch_region_data:
    def __init__(self):
        super().__init__()
    def region_data(self):
        cursor.execute("SELECT * FROM Regions")
        rs1 = dictfetchall(cursor)
        df = pd.DataFrame(rs1)
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df['updated_at'] = pd.to_datetime(df['updated_at'])
        df['updated_at'] = df['updated_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df.rename(columns={'region_name': 'Region'}, inplace=True)
        df.rename(columns={'created_at': 'Created At'}, inplace=True)
        df.rename(columns={'updated_at': 'Updated At'}, inplace=True)
        df.rename(columns={'created_by_id': 'Created By'}, inplace=True)
        df.rename(columns={'updated_by_id': 'Updated By'}, inplace=True)
        df = df.drop('Created By', axis=1)
        df = df.drop('Updated By', axis=1)
        df = df.to_html(index=False)
        return df

    def region_data_added(self):
        cursor.execute("SELECT * FROM Regions")
        rs1 = dictfetchall(cursor)
        df = pd.DataFrame(rs1)
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df['updated_at'] = pd.to_datetime(df['updated_at'])
        df['updated_at'] = df['updated_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df.rename(columns={'region_name': 'Region'}, inplace=True)
        df.rename(columns={'created_at': 'Created At'}, inplace=True)
        df.rename(columns={'updated_at': 'Updated At'}, inplace=True)
        df.rename(columns={'created_by_id': 'Created By'}, inplace=True)
        df.rename(columns={'updated_by_id': 'Updated By'}, inplace=True)
        df = df.drop('Created By', axis=1)
        df = df.drop('Updated By', axis=1)
        df = df.to_html(index=False)
        return df



#TESTING DATA
def region_data():
    cursor.execute("SELECT id, region_name, created_at, updated_at, created_by_id, updated_by_id FROM Regions")
    regions_data = dictfetchall(cursor)
    regions_df = pd.DataFrame(regions_data)

    # Second query
    cursor.execute("SELECT s.id, s.region_name, s.created_at, s.updated_at, s.created_by_id, s.updated_by_id, r.first_name "
                   "FROM Regions s LEFT JOIN auth_user r ON s.created_by_id = r.id")

    dfs = dictfetchall(cursor)
    df = pd.DataFrame(dfs)
    df['created_by_id'] = df['first_name']
    # third query
    # cursor.execute(
    #     "SELECT s.id, s.region_name, s.created_at, s.updated_at, s.created_by_id, s.updated_by_id, r.first_name "
    #     "FROM Regions s LEFT JOIN auth_user r ON s.updated_by_id = r.id")
    #
    # dfs = dictfetchall(cursor)
    # df = pd.DataFrame(dfs)
    #
    # df['updated_by_id'] = df['first_name']
    # result_df = pd.concat([df, df], ignore_index=True, sort=True)
    # print(result_df.to_string())
# df['created_at'] = pd.to_datetime(df['created_at'])
    # df['Formatted Date'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
    # df.rename(columns={'region_name': 'Region'}, inplace=True)
    # df.rename(columns={'created_at': 'Created At'}, inplace=True)
    # df.rename(columns={'updated_at': 'Updated At'}, inplace=True)
    # df.rename(columns={'created_by_id': 'Created By'}, inplace=True)
    # df.rename(columns={'updated_by_id': 'Updated By'}, inplace=True)
    # df = df.to_html(index=False)
    #print(df)
# region_data()