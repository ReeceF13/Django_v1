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
def region():
    cursor.execute("SELECT id, region_name, updated_at FROM Regions WHERE updated_at = (SELECT MAX(updated_at) FROM Regions)")
    rs1 = dictfetchall(cursor)
    df = pd.DataFrame(rs1)
    print(df)
# region()
def store():
    cursor.execute("SELECT id, store_name, updated_at FROM Stores WHERE updated_at = (SELECT MAX(updated_at) FROM Stores)")
    rs1 = dictfetchall(cursor)
    df = pd.DataFrame(rs1)
    print(df)
#store()
def rc():
    cursor.execute("SELECT id, first_name, last_name, updated_at FROM RegionalCoaches WHERE updated_at = (SELECT MAX(updated_at) FROM RegionalCoaches)")
    rs1 = dictfetchall(cursor)
    df = pd.DataFrame(rs1)
    print(df)
# rc()
def rca():
    cursor.execute("SELECT regional_coach_id, store_id, updated_at FROM RegionalCoachAssignments WHERE updated_at = (SELECT MAX(updated_at) FROM RegionalCoachAssignments)")
    rs1 = dictfetchall(cursor)
    df = pd.DataFrame(rs1)
    print(df)
#rca()
def ac():
    cursor.execute("SELECT id, first_name, last_name, updated_at FROM AreaCoaches WHERE updated_at = (SELECT MAX(updated_at) FROM AreaCoaches)")
    rs1 = dictfetchall(cursor)
    df = pd.DataFrame(rs1)
    print(df)
ac()