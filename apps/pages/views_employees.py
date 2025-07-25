from django.shortcuts import render

##FORMS
from apps.pages.forms import *
from apps.pages.frontend_forms.forms import *
#CLASS IMPORTS

from apps.db.employees.employee_query import fetch_e_data, fetch_e_data_updated
from apps.db.table_counts.all_counts import *

from apps.db.connections.connection_string import conn_str
from apps.db.dict_fetch.fetch_data import dictfetchall
import pyodbc
import pandas as pd
from datetime import datetime

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

#EMPLOYEES
def view_employees(request):
    e_one = fetch_e_data()
    e_ = e_one.e_data()
    context = {'html_table': e_}
    return render(request, "pages/pages/employees.html", context)

def add_employee(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_logged_in = current_user.id
    now_ = datetime.now().replace(microsecond=0)
    if request.method == 'GET':
        form = Store_Dropdown(request.GET)
        if form.is_valid():
            selected_value = form.cleaned_data['my_model_choice']
            # print(selected_value)
            params = str(selected_value)
            cursor.execute("SELECT id FROM Stores WHERE store_name LIKE '%' + ? + '%'", params)
            rs1 = dictfetchall(cursor)
            id_row = pd.DataFrame(rs1)
            for i in id_row.values:
                store_id = (str(i[0]))
                print(store_id)
        if request.method == 'GET':
            form2 = E_Dropdown(request.GET)
            if form2.is_valid():
                selected_value = form2.cleaned_data['my_choice_field']
                et_input = selected_value
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
        # print(i1)

        dfs = pd.DataFrame(
            columns=['F_Name', 'L_Name', 'Cell', 'Email', 'EMP_Code', 'Store_ID', 'EMP_Type', 'is_active', 'created_at', 'updated_at', 'created_by_id', 'updated_by_id'])
        dfs.loc[0] = fn_input, ln_input, c_input, e_input, emp_input, et_input, store_id, active_input, now_, now_, user_logged_in, user_logged_in
        # print(dfs.to_string())
        for index, row in dfs.iterrows():
            cursor.execute(
                "INSERT INTO Employees (first_name, last_name, cell_phone, email_address, employee_code, store_id, "
                "employee_type, is_active, created_at, updated_at, created_by_id, updated_by_id) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                row['F_Name'], row['L_Name'], row['Cell'], row['Email'], row['EMP_Code'], row['Store_ID'],
                row['EMP_Type'], row['is_active'],
                row['created_at'], row['updated_at'], row['created_by_id'], row['updated_by_id'])
            cursor.commit()
            e_one = fetch_e_data_updated()
            e_ = e_one.e_data_updated()
            context11 = {'html_table': e_}
            return render(request, "pages/pages/employees.html", context11)

    else:
        form = Store_Dropdown()
        form2 = E_Dropdown()

    return render(request, "pages/pages/add_records/add_employee.html",
                      {'form': form, 'form2': form2})