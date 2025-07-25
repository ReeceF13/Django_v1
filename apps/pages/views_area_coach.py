from django.shortcuts import render

##FORMS
from apps.pages.forms import *
from apps.pages.frontend_forms.forms import *
#CLASS IMPORTS
from apps.db.area_coaches.ac_query import fetch_area_coach_data, fetch_area_coach_data_updated
from apps.db.area_coaches.ac_assignments.ac_a_assignments import fetch_aca_data, fetch_aca_updated

from apps.db.table_counts.all_counts import *

from apps.db.connections.connection_string import conn_str
from apps.db.dict_fetch.fetch_data import dictfetchall
import pyodbc
import pandas as pd
from datetime import datetime


conn = pyodbc.connect(conn_str)
cursor = conn.cursor()


#AREA COACHES
def view_area_coaches(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_logged_in = current_user.id
    ac_one = fetch_area_coach_data()
    ac_ = ac_one.ac_data()
    context = {'html_table': ac_}
    now_ = datetime.now().replace(microsecond=0)
    if 'word' in request.GET:
        word_input = request.GET['word']
        params = word_input
        cursor.execute("SELECT * FROM AreaCoaches WHERE first_name LIKE '%' + ? + '%'", params)
        rs1 = dictfetchall(cursor)
        df = pd.DataFrame(rs1)
        dfsd = df.to_records(index=False)
        for i in dfsd:
            i0 = (str(i[0]))
            i1 = (str(i[1]))
            i2 = (str(i[2]))
            i3 = (str(i[3]))
            i4 = (str(i[4]))
            i5 = (str(i[5]))
            i6 = (str(i[6]))
        initial_data = {'ID': i0, 'First_Name': i1, 'Last_Name': i2, 'Cell_Phone': i3, 'Email_Address': i4,
                        'Employee_Code': i5, 'Is_Active': i6}
        form = ACUpdate(initial=initial_data)
        if 'filter' in request.POST:
            id_ = request.POST.get('ID')
            fn_ = request.POST.get('First_Name')
            ln_ = request.POST.get('Last_Name')
            cp_ = request.POST.get('Cell_Phone')
            ea_ = request.POST.get('Email_Address')
            ec_ = request.POST.get('Employee_Code')
            ia_ = request.POST.get('Is_Active')
            updated_at = now_
            updated_by = user_logged_in
            dfsp = pd.DataFrame(
                columns=['id', 'first_name', 'last_name', 'cell_phone', 'email_address', 'employee_code', 'is_active',
                         'updated_at', 'updated_by_id'])
            dfsp.loc[0] = id_, fn_, ln_, cp_, ea_, ec_, ia_, updated_at, updated_by
            for index, row in dfsp.iterrows():
                cursor.execute(
                    "UPDATE AreaCoaches SET first_name = ?, last_name = ?, cell_phone = ?, email_address = ?, "
                    "employee_code = ?, is_active = ?, updated_at = ?, updated_by_id = ? WHERE id = ?",
                    (row['first_name'], row['last_name'], row['cell_phone'], row['email_address'],
                     row['employee_code'], row['is_active'], row['updated_at'], row['updated_by_id'], row['id']))
                cursor.commit()
                ac_up = fetch_area_coach_data_updated()
                ac__ = ac_up.ac_data_updated()
                context1 = {'html_table': ac__}
                return render(request, "pages/pages/area_coaches.html", context1)
        return render(request, "pages/pages/edit_records/edit_ac.html",
                      {'form': form, 'initial_data': initial_data})
    return render(request, "pages/pages/area_coaches.html", context)

def add_area_coach(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_logged_in = current_user.id
    now_ = datetime.now().replace(microsecond=0)
    if 'fnInput' in request.GET:
        fn_input = request.GET['fnInput'].upper()
    if 'lnInput' in request.GET:
        ln_input = request.GET['lnInput'].upper()
    if 'cInput' in request.GET:
        c_input = request.GET['cInput']
    if 'eInput' in request.GET:
        e_input = request.GET['eInput'].upper()
    if 'empInput' in request.GET:
        emp_input = request.GET['empInput']
    if 'activeInput' in request.GET:
        active_input = request.GET['activeInput']

        dfs = pd.DataFrame(
            columns=['F_Name', 'L_Name', 'Cell', 'Email', 'EMP_Code', 'is_active', 'created_at', 'updated_at', 'created_by_id', 'updated_by_id'])
        dfs.loc[0] = fn_input, ln_input, c_input, e_input, emp_input, active_input, now_, now_, user_logged_in, user_logged_in
        # print(dfs.to_string())
        for index, row in dfs.iterrows():
            cursor.execute(
                "INSERT INTO AreaCoaches (first_name, last_name, cell_phone, email_address, employee_code, is_active, created_at, updated_at, created_by_id, updated_by_id) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                row['F_Name'], row['L_Name'], row['Cell'], row['Email'], row['EMP_Code'], row['is_active'],
                row['created_at'], row['updated_at'], row['created_by_id'], row['updated_by_id'])
            cursor.commit()
            ac_up = fetch_area_coach_data_updated()
            ac__ = ac_up.ac_data_updated()
            context1 = {'html_table': ac__}
            return render(request, "pages/pages/area_coaches.html", context1)

    return render(request, "pages/pages/add_records/add_area_coach.html")

def view_area_coach_assignments(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_logged_in = current_user.id
    aca_one = fetch_aca_data()
    aca_ = aca_one.aca_data()
    context = {'html_table': aca_}
    if 'word' in request.GET:
        word_input = request.GET['word']
        params = word_input

        cursor.execute("SELECT * FROM AreaCoachAssignments WHERE id LIKE '%' + ? + '%'", params)
        rs1 = dictfetchall(cursor)
        df = pd.DataFrame(rs1)
        # print(df.to_string())
        dfsd = df.to_records(index=False)
        for i in dfsd:
            i0 = (str(i[0]))
            i1 = (str(i[1]))
            i2 = (str(i[2]))
            i3 = (str(i[3]))
            i4 = (str(i[4]))
        initial_data = {'ID': i0, 'Area_Coach_ID': i1, 'Regional_Coach_ID': i2, 'Start_Date': i3, 'End_Date': i4}
        form = ACAUpdate(initial=initial_data)
        now_ = datetime.now().replace(microsecond=0)
        if 'filter' in request.POST:
            id_ = request.POST.get('ID')
            sd_ = request.POST.get('Start_Date')
            ed_ = request.POST.get('End_Date')
            updated_at = now_
            updated_by = user_logged_in
            dfsp = pd.DataFrame(
                columns=['id', 's_date', 'e_date', 'updated_at', 'updated_by_id'])
            dfsp.loc[0] = id_, sd_, ed_, updated_at, updated_by
            for index, row in dfsp.iterrows():
                cursor.execute(
                    "UPDATE AreaCoachAssignments SET start_date = ?, end_date= ?, "
                    "updated_at = ?, updated_by_id = ? WHERE id = ?",
                    (row['s_date'], row['e_date'], row['updated_at'], row['updated_by_id'], row['id']))
                cursor.commit()
                aca_up = fetch_aca_updated()
                aca__ = aca_up.aca_data_updated()
                context1 = {'html_table': aca__}
                return render(request, "pages/pages/add_records/assignments/ac_assignments.html", context1)

        return render(request, "pages/pages/edit_records/edit_aca.html",
                      {'form': form, 'initial_data': initial_data})
    return render(request, "pages/pages/add_records/assignments/ac_assignments.html", context)

def add_area_coach_assignments(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_logged_in = current_user.id
    if request.method == 'GET':
        form2 = AC_Dropdown(request.GET)
        form3 = RC_Dropdown(request.GET)
        if form2.is_valid():
            selected_value = form2.cleaned_data['my_model_choice']
            # print(selected_value)
            params = str(selected_value)
            print(params)
            cursor.execute("SELECT id FROM AreaCoaches WHERE CONCAT(first_name, ' ', last_name) LIKE ?", ['%' + params + '%'])
            rs1 = dictfetchall(cursor)
            id_row = pd.DataFrame(rs1)
            for i in id_row.values:
                ac_id = (str(i[0]))
                print(f"ac id is {ac_id}")

        if form3.is_valid():
            selected_value2 = form3.cleaned_data['my_model_choice']
            params1 = str(selected_value2)
            cursor.execute("SELECT id FROM RegionalCoaches WHERE CONCAT(first_name, ' ', last_name) LIKE ?", ['%' + params1 + '%'])
            rs1 = dictfetchall(cursor)
            id_row = pd.DataFrame(rs1)
            for i in id_row.values:
                rc_id = (str(i[0]))
                # print(f"rc id is {rc_id}")
    now_ = datetime.now().replace(microsecond=0)
    if 'cInput' in request.GET:
        c_input = request.GET['cInput']
    if 'eInput' in request.GET:
        e_input = request.GET['eInput'].upper()
        # print(i1)
        dfs = pd.DataFrame(
            columns=['rc_id', 'store_id', 's_date', 'e_date', 'created_at', 'updated_at', 'created_by_id', 'updated_by_id'])
        dfs.loc[0] = ac_id, rc_id, c_input, e_input, now_, now_, user_logged_in, user_logged_in
        print(dfs.to_string())
        for index, row in dfs.iterrows():
            cursor.execute(
                "INSERT INTO AreaCoachAssignments (area_coach_id, regional_coach_id, start_date, end_date, created_at, updated_at, created_by_id, updated_by_id) "
                "VALUES (?,?,?,?,?,?,?,?)",
                row['rc_id'], row['store_id'], row['s_date'], row['e_date'],
                row['created_at'], row['updated_at'], row['created_by_id'], row['updated_by_id'])
            cursor.commit()
            acau_one = fetch_aca_updated()
            acua_ = acau_one.aca_data_updated()
            context1 = {'html_table': acua_}
            return render(request, "pages/pages/add_records/assignments/ac_assignments.html", context1)

    else:
        form2 = RC_Dropdown()
        form3 = AC_Dropdown()
    return render(request, "pages/pages/add_records/assignments/add_ac_assignments.html", {'form2': form2, 'form3': form3})