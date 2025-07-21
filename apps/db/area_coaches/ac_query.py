from apps.db.connections.connection_string import conn_str
from apps.db.dict_fetch.fetch_data import dictfetchall
import pyodbc
import pandas as pd
from datetime import datetime

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

class fetch_area_coach_data:
    def __init__(self):
        super().__init__()
    def ac_data(self):
        try:
            cursor.execute("SELECT * FROM AreaCoaches")
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

        except:
            df = "No Data Found"
            return df