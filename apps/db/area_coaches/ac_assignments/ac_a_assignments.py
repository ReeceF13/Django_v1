from apps.db.connections.connection_string import conn_str
from apps.db.dict_fetch.fetch_data import dictfetchall
import pyodbc
import pandas as pd
from datetime import datetime

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

class fetch_aca_data:
    def __init__(self):
        super().__init__()
    def aca_data(self):
        try:
            cursor.execute(
                "SELECT s.*, CONCAT(ac.first_name, ' ', ac.last_name) as ac, CONCAT(rc.first_name, ' ', rc.last_name) as rc "
                "FROM AreaCoachAssignments s LEFT JOIN AreaCoaches ac ON s.area_coach_id = ac.id LEFT JOIN RegionalCoaches rc ON s.regional_coach_id = rc.id")
            rs1 = dictfetchall(cursor)
            df = pd.DataFrame(rs1)
            df['area_coach_id'] = df['ac']
            df['regional_coach_id'] = df['rc']
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            df['updated_at'] = pd.to_datetime(df['updated_at'])
            df['updated_at'] = df['updated_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            df.rename(columns={'region_name': 'Region'}, inplace=True)
            df.rename(columns={'area_coach_id': 'Area Coach'}, inplace=True)
            df.rename(columns={'regional_coach_id': 'Regional Coach'}, inplace=True)
            df.rename(columns={'start_date': 'Start Date'}, inplace=True)
            df.rename(columns={'end_date': 'End Date'}, inplace=True)
            df.rename(columns={'created_at': 'Created At'}, inplace=True)
            df.rename(columns={'updated_at': 'Updated At'}, inplace=True)
            df.rename(columns={'created_by_id': 'Created By'}, inplace=True)
            df.rename(columns={'updated_by_id': 'Updated By'}, inplace=True)
            df = df.drop('Created By', axis=1)
            df = df.drop('Updated By', axis=1)
            df = df.drop('ac', axis=1)
            df = df.drop('rc', axis=1)
            df = df.to_html(index=False)
            return df
        except:
            df = "No Data Found"
            return df
class fetch_aca_updated:
    def __init__(self):
        super().__init__()
    def aca_data_updated(self):
        try:
            cursor.execute(
                "SELECT s.*, CONCAT(ac.first_name, ' ', ac.last_name) as ac, CONCAT(rc.first_name, ' ', rc.last_name) as rc "
                "FROM AreaCoachAssignments s LEFT JOIN AreaCoaches ac ON s.area_coach_id = ac.id LEFT JOIN RegionalCoaches rc ON s.regional_coach_id = rc.id")
            rs1 = dictfetchall(cursor)
            df = pd.DataFrame(rs1)
            df['area_coach_id'] = df['ac']
            df['regional_coach_id'] = df['rc']
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            df['updated_at'] = pd.to_datetime(df['updated_at'])
            df['updated_at'] = df['updated_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            df.rename(columns={'region_name': 'Region'}, inplace=True)
            df.rename(columns={'area_coach_id': 'Area Coach'}, inplace=True)
            df.rename(columns={'regional_coach_id': 'Regional Coach'}, inplace=True)
            df.rename(columns={'start_date': 'Start Date'}, inplace=True)
            df.rename(columns={'end_date': 'End Date'}, inplace=True)
            df.rename(columns={'created_at': 'Created At'}, inplace=True)
            df.rename(columns={'updated_at': 'Updated At'}, inplace=True)
            df.rename(columns={'created_by_id': 'Created By'}, inplace=True)
            df.rename(columns={'updated_by_id': 'Updated By'}, inplace=True)
            df = df.drop('Created By', axis=1)
            df = df.drop('Updated By', axis=1)
            df = df.drop('ac', axis=1)
            df = df.drop('rc', axis=1)
            df = df.to_html(index=False)
            return df
        except:
            df = "No Data Found"
            return df

def testing():
    cursor.execute(
        "SELECT s.*, CONCAT(ac.first_name, ' ', ac.last_name) as ac, CONCAT(rc.first_name, ' ', rc.last_name) as rc "
        "FROM AreaCoachAssignments s LEFT JOIN AreaCoaches ac ON s.area_coach_id = ac.id LEFT JOIN RegionalCoaches rc ON s.regional_coach_id = rc.id")
    rs1 = dictfetchall(cursor)
    dfs = pd.DataFrame(rs1)
    print(dfs.to_string())
# testing()

