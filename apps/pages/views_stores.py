from django.shortcuts import render
##FORMS
from apps.pages.forms import *
from apps.pages.frontend_forms.forms import *
#CLASS IMPORTS
from apps.db.stores.store_query import fetch_store_data, fetch_store_data_updated
from apps.db.table_counts.all_counts import *
from apps.db.connections.connection_string import conn_str
from apps.db.dict_fetch.fetch_data import dictfetchall
import pyodbc
import pandas as pd
from datetime import datetime
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

def view_stores(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_logged_in = current_user.id
    store_one = fetch_store_data()
    store_ = store_one.store_data()
    context = {'html_table': store_}
    now_ = datetime.now().replace(microsecond=0)
    if 'word' in request.GET:
        word_input = request.GET['word']
        params = word_input
        cursor.execute("SELECT * FROM Stores WHERE store_name LIKE '%' + ? + '%'", params)
        rs1 = dictfetchall(cursor)
        df = pd.DataFrame(rs1)
        dfsd = df.to_records(index=False)
        for i in dfsd:
            i0 = (str(i[0]))
            i1 = (str(i[1]))
            i2 = (str(i[2]))
            i3 = (str(i[3]))
            i4 = (str(i[4]))
        initial_data = {'ID': i0, 'Store_ID': i1, 'Store_Name': i2, 'Region_ID': i3, 'Head_Office': i4}
        form = StoreUpdate(initial=initial_data)
        if 'filter' in request.POST:
            id_ = request.POST.get('ID')
            sd_ = request.POST.get('Store_ID')
            sn_ = request.POST.get('Store_Name')
            hd_ = request.POST.get('Head_Office')
            updated_at = now_
            updated_by = user_logged_in
            dfsp = pd.DataFrame(
                columns=['id', 'store_id', 'store_name', 'head_office', 'updated_at', 'updated_by_id'])
            dfsp.loc[0] = id_, sd_, sn_,hd_, updated_at, updated_by
            for index, row in dfsp.iterrows():
                cursor.execute("UPDATE Stores SET store_id = ?, store_name = ?, is_head_office = ?, updated_at = ?, updated_by_id = ? WHERE id = ?",
                               (row['store_id'], row['store_name'], row['head_office'], row['updated_at'], row['updated_by_id'], row['id']))
                cursor.commit()
                store_one = fetch_store_data_updated()
                store_ = store_one.store_data_updated()
                context1 = {'html_table': store_}
                return render(request, "pages/pages/stores.html", context1)

        return render(request, "pages/pages/edit_records/edit_stores.html",
                      {'form': form, 'initial_data': initial_data})

    return render(request, "pages/pages/stores.html", context)

def add_store(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_logged_in = current_user.id

    now_ = datetime.now().replace(microsecond=0)
    if request.method == 'GET':
        form2 = Region_Dropdown(request.GET)
        if form2.is_valid():
            selected_value = form2.cleaned_data['my_model_choice']
            params = str(selected_value)
            # print(type(params))
            cursor.execute("SELECT id FROM Regions WHERE region_name LIKE '%' + ? + '%'", params)
            rs1 = dictfetchall(cursor)
            id_row = pd.DataFrame(rs1)
            for i in id_row.values:
                i2 = (str(i[0]))
            print(i2)
    if 'ksaInput' in request.GET:
        ksa_input = request.GET['ksaInput'].upper()
    if 'storeInput' in request.GET:
        store_input = request.GET['storeInput'].upper()
    if 'headInput' in request.GET:
        head_input = request.GET['headInput']
        dfs = pd.DataFrame(
            columns=['KSA', 'Store', 'Region', 'Head_Office', 'Create_Time', 'Updated_Time', 'User', 'Updated_By_User'])
        dfs.loc[0] = ksa_input, store_input, i2, head_input, now_, now_, user_logged_in, user_logged_in,
        print(dfs.to_string())

        for index, row in dfs.iterrows():

            cursor.execute("INSERT INTO Stores (store_id, store_name, region_id, is_head_office, created_at, updated_at, created_by_id, updated_by_id) "
                            "VALUES (?,?,?,?,?,?,?,?)",
                           row['KSA'], row['Store'], row['Region'], row['Head_Office'], row['Create_Time'], row['Updated_Time'], row['User'], row['Updated_By_User'])
            cursor.commit()
            return view_stores(request)
    else:
        form2 = Region_Dropdown()
    return render(request, "pages/pages/add_records/add_store.html", {'form2': form2})