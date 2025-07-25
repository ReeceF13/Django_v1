from apps.db.connections.connection_string import conn_str
from apps.db.dict_fetch.fetch_data import dictfetchall
import pyodbc
import pandas as pd
from datetime import datetime

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

class fetch_rca_data:
    def __init__(self):
        super().__init__()
    def rca_data(self):
        try:
            cursor.execute(
                "SELECT s.*, CONCAT(ac.first_name, ' ', ac.last_name) as ac, store_name as store "
                "FROM RegionalCoachAssignments s LEFT JOIN RegionalCoaches ac ON s.regional_coach_id = ac.id LEFT JOIN Stores rc ON s.regional_coach_id = rc.id")
            rs1 = dictfetchall(cursor)
            df = pd.DataFrame(rs1)

            df['created_at'] = pd.to_datetime(df['created_at'])
            df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            df['updated_at'] = pd.to_datetime(df['updated_at'])
            df['updated_at'] = df['updated_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            df['regional_coach_id'] = df['ac']
            df['store_id'] = df['store']
            df.rename(columns={'store_id': 'Store'}, inplace=True)
            df.rename(columns={'regional_coach_id': 'Regional Coach'}, inplace=True)
            df.rename(columns={'created_at': 'Created At'}, inplace=True)
            df.rename(columns={'updated_at': 'Updated At'}, inplace=True)
            df.rename(columns={'created_by_id': 'Created By'}, inplace=True)
            df.rename(columns={'updated_by_id': 'Updated By'}, inplace=True)
            df.rename(columns={'start_date': 'Start Date'}, inplace=True)
            df.rename(columns={'end_date': 'End Date'}, inplace=True)
            df = df.drop('Created By', axis=1)
            df = df.drop('Updated By', axis=1)
            df = df.drop('ac', axis=1)
            df = df.drop('store', axis=1)
            df = df.to_html(index=False)
            return df
        except:
            df = "No Data Found"
            return df
class fetch_rca_updated:
    def __init__(self):
        super().__init__()
    def rca_data_updated(self):
        try:
            cursor.execute(
                "SELECT s.*, CONCAT(ac.first_name, ' ', ac.last_name) as ac, store_name as store "
                "FROM RegionalCoachAssignments s LEFT JOIN RegionalCoaches ac ON s.regional_coach_id = ac.id LEFT JOIN Stores rc ON s.regional_coach_id = rc.id")
            rs1 = dictfetchall(cursor)
            df = pd.DataFrame(rs1)

            df['created_at'] = pd.to_datetime(df['created_at'])
            df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            df['updated_at'] = pd.to_datetime(df['updated_at'])
            df['updated_at'] = df['updated_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            df['regional_coach_id'] = df['ac']
            df['store_id'] = df['store']
            df.rename(columns={'store_id': 'Store'}, inplace=True)
            df.rename(columns={'regional_coach_id': 'Regional Coach'}, inplace=True)
            df.rename(columns={'created_at': 'Created At'}, inplace=True)
            df.rename(columns={'updated_at': 'Updated At'}, inplace=True)
            df.rename(columns={'created_by_id': 'Created By'}, inplace=True)
            df.rename(columns={'updated_by_id': 'Updated By'}, inplace=True)
            df.rename(columns={'start_date': 'Start Date'}, inplace=True)
            df.rename(columns={'end_date': 'End Date'}, inplace=True)
            df = df.drop('Created By', axis=1)
            df = df.drop('Updated By', axis=1)
            df = df.drop('ac', axis=1)
            df = df.drop('store', axis=1)
            df = df.to_html(index=False)
            return df
        except:
            df = "No Data Found"
            return df

def testing():
    cursor.execute(
        "SELECT s.*, CONCAT(ac.first_name, ' ', ac.last_name) as ac, store_name as store "
        "FROM RegionalCoachAssignments s LEFT JOIN RegionalCoaches ac ON s.regional_coach_id = ac.id LEFT JOIN Stores rc ON s.regional_coach_id = rc.id")
    rs1 = dictfetchall(cursor)
    df = pd.DataFrame(rs1)

    df['created_at'] = pd.to_datetime(df['created_at'])
    df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    df['updated_at'] = df['updated_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['regional_coach_id'] = df['ac']
    df['store_id'] = df['store']
    df.rename(columns={'store_id': 'Store'}, inplace=True)
    df.rename(columns={'regional_coach_id': 'Regional Coach'}, inplace=True)
    df.rename(columns={'created_at': 'Created At'}, inplace=True)
    df.rename(columns={'updated_at': 'Updated At'}, inplace=True)
    df.rename(columns={'created_by_id': 'Created By'}, inplace=True)
    df.rename(columns={'updated_by_id': 'Updated By'}, inplace=True)
    df.rename(columns={'start_date': 'Start Date'}, inplace=True)
    df.rename(columns={'end_date': 'End Date'}, inplace=True)
    df = df.drop('Created By', axis=1)
    df = df.drop('Updated By', axis=1)
    df = df.drop('ac', axis=1)
    df = df.drop('store', axis=1)
    print(df.to_string())
# testing()