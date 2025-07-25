from apps.db.connections.connection_string import conn_str
from apps.db.dict_fetch.fetch_data import dictfetchall
import pyodbc
import pandas as pd
from datetime import datetime

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

class fetch_test_data:
    def __init__(self):
        super().__init__()
    def test_data(self):
        try:
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
            # df = df.to_html(index=False)
            # print(df)
            return df
        except:
            df = "No Data Found"
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
def get_current_hierarchy():
    """
    Get current complete hierarchy for analytics
    """


    cursor.execute("SELECT s.store_id, s.store_name, r.region_name, "
                   "rc.first_name + ' ' + rc.last_name as regional_coach_name, "
                   "ac.first_name + ' ' + ac.last_name as area_coach_name, "
                   "bp.first_name + ' ' + bp.last_name as business_partner_name "
                   "FROM Stores s "
                   "LEFT JOIN Regions r ON s.region_id = r.id "
                   "LEFT JOIN RegionalCoachAssignments rca ON s.id = rca.store_id "
                   "LEFT JOIN RegionalCoaches rc ON rca.regional_coach_id = rc.id "
                   "LEFT JOIN AreaCoachAssignments aca ON rc.id = aca.regional_coach_id "
                   "LEFT JOIN AreaCoaches ac ON aca.area_coach_id = ac.id "
                   "LEFT JOIN BusinessPartnerAssignments bpa ON ac.id = bpa.area_coach_id "
                   "LEFT JOIN BusinessPartners bp ON bpa.business_partner_id = bp.id WHERE store_name='TEST_now'")
    rs1 = dictfetchall(cursor)
    df = pd.DataFrame(rs1)

    # print(df.to_string())
get_current_hierarchy()