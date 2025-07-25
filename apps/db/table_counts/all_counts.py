import pyodbc
import pandas as pd
from apps.db.dict_fetch.fetch_data import dictfetchall
conn_str = ("Driver={SQL Server};"
               "Server=localhost;"
               "Database=StoreManagement;"
               "UID=Reece;"
               "PWD=Madness9900;"
               "Trusted_Connection=yes;")
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

class count_s:
    def __init__(self):
        super().__init__()
    def stores_count(self):
        cursor.execute("SELECT COUNT (*) FROM Stores")
        rs1 = dictfetchall(cursor)
        df =pd.DataFrame(rs1)
        dfsd = df.to_records(index=False)
        for i in dfsd:
            i1 = (str(i[0]))
        return i1
    def rc_count(self):
        cursor.execute("SELECT COUNT (*) FROM RegionalCoaches")
        rs1 = dictfetchall(cursor)
        df =pd.DataFrame(rs1)
        dfsd = df.to_records(index=False)
        for i in dfsd:
            i1 = (str(i[0]))
        return i1
    def ac_count(self):
        cursor.execute("SELECT COUNT (*) FROM AreaCoaches")
        rs1 = dictfetchall(cursor)
        df =pd.DataFrame(rs1)
        dfsd = df.to_records(index=False)
        for i in dfsd:
            i1 = (str(i[0]))
        return i1
    def bp_count(self):
        cursor.execute("SELECT COUNT (*) FROM BusinessPartners")
        rs1 = dictfetchall(cursor)
        df =pd.DataFrame(rs1)
        dfsd = df.to_records(index=False)
        for i in dfsd:
            i1 = (str(i[0]))
        return i1
    def store_history(self):
        try:
            cursor.execute("SELECT s.*, r.region_name FROM Stores s LEFT JOIN Regions r ON s.region_id = r.id")
            first_query = dictfetchall(cursor)
            df = pd.DataFrame(first_query)

            cursor.execute(
                "SELECT TOP 10 s.store_id, s.store_name, s.region_id, s.updated_at, r.username FROM Stores s LEFT JOIN auth_user r ON s.updated_by_id = r.id ORDER BY s.updated_at DESC")
            updated_join = dictfetchall(cursor)
            dfs = pd.DataFrame(updated_join)
            dfs['region_id'] = df['region_name']
            dfs['updated_by_id'] = dfs['username']
            dfs['updated_at'] = pd.to_datetime(dfs['updated_at'])
            dfs['updated_at'] = dfs['updated_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            dfs.rename(columns={'store_id': 'Store KSA'}, inplace=True)
            dfs.rename(columns={'store_name': 'Store Name'}, inplace=True)
            dfs.rename(columns={'region_id': 'Region'}, inplace=True)
            dfs.rename(columns={'updated_at': 'Updated At'}, inplace=True)
            dfs.rename(columns={'updated_by_id': 'Updated By'}, inplace=True)
            dfs = dfs.drop('username', axis=1)
            dfs = dfs.to_html(index=False)
            return dfs

        except:
            dfs = "No Data Found"
        return dfs

def store_history():
    cursor.execute("SELECT s.*, r.region_name FROM Stores s LEFT JOIN Regions r ON s.region_id = r.id")
    first_query = dictfetchall(cursor)
    df = pd.DataFrame(first_query)

    cursor.execute("SELECT TOP 10 s.store_id, s.store_name, s.region_id, s.updated_at, r.username FROM Stores s LEFT JOIN auth_user r ON s.updated_by_id = r.id ORDER BY s.updated_at DESC")
    updated_join = dictfetchall(cursor)
    dfs = pd.DataFrame(updated_join)
    dfs['region_id'] = df['region_name']
    dfs['updated_by_id'] = dfs['username']
    dfs['updated_at'] = pd.to_datetime(dfs['updated_at'])
    dfs['updated_at'] = dfs['updated_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
    dfs.rename(columns={'store_id': 'Store KSA'}, inplace=True)
    dfs.rename(columns={'store_name': 'Store Name'}, inplace=True)
    dfs.rename(columns={'region_id': 'Region'}, inplace=True)
    dfs.rename(columns={'updated_at': 'Updated At'}, inplace=True)
    dfs.rename(columns={'updated_by_id': 'Updated By'}, inplace=True)
    dfs = dfs.drop('username', axis=1)
    # dfsd = df.to_records(index=False)
    print(dfs.to_string())
# store_history()