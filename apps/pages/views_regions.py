from django.shortcuts import render

##FORMS
from apps.pages.forms import *

from apps.pages.frontend_forms.forms import *
#CLASS IMPORTS
from apps.db.regions.region_query import fetch_region_data, fetch_region_data_updated

from apps.db.table_counts.all_counts import *

from apps.db.connections.connection_string import conn_str
from apps.db.dict_fetch.fetch_data import dictfetchall
import pyodbc
import pandas as pd
from datetime import datetime

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

##############STORE MANAGEMENT PAGES
def regions_(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_logged_in = current_user.id
    region_one = fetch_region_data()
    region_ = region_one.region_data()
    context = {'html_table': region_}
    now_ = datetime.now().replace(microsecond=0)
    if 'word' in request.GET:
        word_input = request.GET['word']
        params = word_input
        cursor.execute("SELECT * FROM Regions WHERE region_name LIKE '%' + ? + '%'", params)
        rs1 = dictfetchall(cursor)
        df = pd.DataFrame(rs1)
        dfsd = df.to_records(index=False)
        for i in dfsd:
            i0 = (str(i[0]))
            i1 = (str(i[1]))
            # print(i0)
        initial_data = {'ID': i0, 'Region_Name': i1}
        form = RegionUpdate(initial=initial_data)
        if 'filter' in request.POST:
            id_ = request.POST.get('ID')
            rn_ = request.POST.get('Region_Name')
            updated_at = now_
            updated_by = user_logged_in
            dfsp = pd.DataFrame(
                columns=['id', 'region_name', 'updated_at', 'updated_by_id'])
            dfsp.loc[0] = id_, rn_, updated_at, updated_by
            for index, row in dfsp.iterrows():
                cursor.execute("UPDATE Regions SET region_name = ?, updated_at = ?, updated_by_id = ? WHERE id = ?",
                               (row['region_name'], row['updated_at'], row['updated_by_id'], row['id']))

                cursor.commit()
                region_one = fetch_region_data_updated()
                region_ = region_one.region_data_updated()
                context1 = {'html_table': region_}
                return render(request, "pages/pages/region_table.html", context1)

        return render(request, "pages/pages/edit_records/edit_regions.html", {'form': form, 'initial_data': initial_data})

    return render(request, "pages/pages/region_table.html", context)

def regions_add(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_logged_in = current_user.id
    if 'regionInput' in request.GET:
        region_input = request.GET['regionInput'].upper()
        r_ = region_input
        dfs = pd.DataFrame(
            columns=['region_name', 'created_at', 'updated_at', 'created_by_id', 'updated_by_id'])
        now_ = datetime.now().replace(microsecond=0)
        dfs.loc[0] = r_, now_, now_, user_logged_in, user_logged_in
        for index, row in dfs.iterrows():
            cursor.execute("INSERT INTO Regions (region_name, created_at, updated_at, created_by_id, updated_by_id) "
                            "VALUES (?,?,?,?,?)",
                           row['region_name'], row['created_at'], row['updated_at'], row['created_by_id'], row['updated_by_id'])
            cursor.commit()
            region_one = fetch_region_data_updated()
            region_ = region_one.region_data_updated()
            context1 = {'html_table': region_}
            return render(request, "pages/pages/region_table.html", context1)
    return render(request, "pages/pages/add_records/add_region.html")


