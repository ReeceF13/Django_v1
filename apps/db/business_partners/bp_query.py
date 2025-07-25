from apps.db.connections.connection_string import conn_str
from apps.db.dict_fetch.fetch_data import dictfetchall
import pyodbc
import pandas as pd
from datetime import datetime

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

class fetch_bp_data:
    def __init__(self):
        super().__init__()
    def bp_data(self):
        try:
            cursor.execute("SELECT * FROM BusinessPartners")
            rs1 = dictfetchall(cursor)
            df = pd.DataFrame(rs1)
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            df['updated_at'] = pd.to_datetime(df['updated_at'])
            df['updated_at'] = df['updated_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            df.rename(columns={'first_name': 'First Name'}, inplace=True)
            df.rename(columns={'last_name': 'Last Name'}, inplace=True)
            df.rename(columns={'cell_phone': 'Cell Phone'}, inplace=True)
            df.rename(columns={'email_address': 'Email'}, inplace=True)
            df.rename(columns={'employee_code': 'Employee Code'}, inplace=True)
            df.rename(columns={'is_active': 'Active'}, inplace=True)
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
class fetch_bp_data_updated:
    def __init__(self):
        super().__init__()
    def bp_data_updated(self):
        try:
            cursor.execute("SELECT * FROM BusinessPartners")
            rs1 = dictfetchall(cursor)
            df = pd.DataFrame(rs1)
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            df['updated_at'] = pd.to_datetime(df['updated_at'])
            df['updated_at'] = df['updated_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            df.rename(columns={'first_name': 'First Name'}, inplace=True)
            df.rename(columns={'last_name': 'Last Name'}, inplace=True)
            df.rename(columns={'cell_phone': 'Cell Phone'}, inplace=True)
            df.rename(columns={'email_address': 'Email'}, inplace=True)
            df.rename(columns={'employee_code': 'Employee Code'}, inplace=True)
            df.rename(columns={'is_active': 'Active'}, inplace=True)
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