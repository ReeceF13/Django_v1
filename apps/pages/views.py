from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordChangeView,
    PasswordResetConfirmView,
)
from django.utils.lorem_ipsum import words

from apps.pages.forms import (
    RegistrationForm,
    LoginForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
    UserPasswordChangeForm,
)
from django.contrib.auth import logout

##FORMS
from apps.pages.forms import RegionUpdate, StoreUpdate, RCUpdate, ACUpdate, BPUpdate
##TESTING
from apps.db.tests.tests_ import fetch_test_data
#CLASS IMPORTS
from apps.db.regions.region_query import fetch_region_data, fetch_region_data_updated
from apps.db.stores.store_query import fetch_store_data, fetch_store_data_updated
from apps.db.regional_coaches.rc_query import fetch_regional_coach_data, fetch_regional_coach_data_updated
from apps.db.regional_coaches.rc_assignmets.rc_a_query import fetch_rca_data, fetch_rca_updated
from apps.db.area_coaches.ac_query import fetch_area_coach_data, fetch_area_coach_data_updated
from apps.db.area_coaches.ac_assignments.ac_a_assignments import fetch_aca_data, fetch_aca_updated
from apps.db.business_partners.bp_query import fetch_bp_data, fetch_bp_data_updated
from apps.db.business_partners.bp_assignments.bp_a_query import fetch_bpa_data, fetch_bpa_updated
from apps.db.employees.employee_query import fetch_e_data
from datetime import datetime
from django.contrib.auth.decorators import login_required
#


from .forms import Store_Search, MyModelForm, RC_Search
from apps.db.connections.connection_string import conn_str
from apps.db.dict_fetch.fetch_data import dictfetchall
import pyodbc
import pandas as pd
from datetime import datetime

from ..models.base import BaseModel

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
# Dashboard
def default(request):
    context = {"parent": "dashboard", "segment": "default"}
    return render(request, "pages/dashboards/default.html", context)


def automotive(request):
    context = {"parent": "dashboard", "segment": "automotive"}
    return render(request, "pages/dashboards/automotive.html", context)


def smart_home(request):
    context = {"parent": "dashboard", "segment": "smart_home"}
    return render(request, "pages/dashboards/smart-home.html", context)


def crm(request):
    context = {"parent": "dashboard", "segment": "crm"}
    return render(request, "pages/dashboards/crm.html", context)


# Dashboard -> VR
def vr_default(request):
    context = {"parent": "dashboard", "sub_parent": "vr", "segment": "vr_default"}
    return render(request, "pages/dashboards/vr/vr-default.html", context)


def vr_info(request):
    context = {"parent": "dashboard", "sub_parent": "vr", "segment": "vr_info"}
    return render(request, "pages/dashboards/vr/vr-info.html", context)


# Pages
def messages(request):
    context = {"parent": "pages", "segment": "messages"}
    return render(request, "pages/pages/messages.html", context)


def widgets(request):
    context = {"parent": "pages", "segment": "widgets"}
    return render(request, "pages/pages/widgets.html", context)


def charts_page(request):
    context = {"parent": "pages", "segment": "charts"}
    return render(request, "pages/pages/charts.html", context)


def sweet_alerts(request):
    context = {"parent": "pages", "segment": "sweet_alerts"}
    return render(request, "pages/pages/sweet-alerts.html", context)


def notifications(request):
    context = {"parent": "pages", "segment": "notifications"}
    return render(request, "pages/pages/notifications.html", context)

##############STORE MANAGEMENT PAGES
def regions_(request):
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
            i2 = (str(i[2]))
            i3 = (str(i[3]))
            i4 = (str(i[4]))
            i5 = (str(i[5]))
            # print(i0)
        initial_data = {'ID': i0, 'Region_Name': i1, 'Created_At': i2, 'Updated_At': i3, 'Created_By': i4, 'Updated_By': i5}
        form = RegionUpdate(initial=initial_data)
        if 'filter' in request.POST:
            id_ = request.POST.get('ID')
            rn_ = request.POST.get('Region_Name')
            updated_at = now_
            updated_by = request.POST.get('Updated_By')
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
    if 'regionInput' in request.GET:
        global r_
        region_input = request.GET['regionInput']
        r_ = region_input
    if 'createInput' in request.GET:
        global c_
        create_input = request.GET['createInput']
        c_ = create_input
        cursor.execute("SELECT id FROM auth_user WHERE username LIKE '%' + ? + '%'", create_input)
        rs1 = dictfetchall(cursor)
        id_row = pd.DataFrame(rs1)
        for i in id_row.values:
            i1 = (str(i[0]))
        print(i1)
        region_one = fetch_region_data()
        region_ = region_one.region_data_added()
        context = {'html_table': region_}
        dfs = pd.DataFrame(
            columns=['region_name', 'created_at', 'updated_at', 'created_by_id', 'updated_by_id'])
        now_ = datetime.now().replace(microsecond=0)
        dfs.loc[0] = r_, now_, now_, i1, i1,
        for index, row in dfs.iterrows():
            cursor.execute("INSERT INTO Regions (region_name, created_at, updated_at, created_by_id, updated_by_id) "
                            "VALUES (?,?,?,?,?)",
                           row['region_name'], row['created_at'], row['updated_at'], row['created_by_id'], row['updated_by_id'])
            cursor.commit()
            return render(request, "pages/pages/records_added_pages/region_added_table.html", context)

    return render(request, "pages/pages/add_records/add_region.html")

def stores_(request):
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
            i5 = (str(i[5]))
            i6 = (str(i[6]))
            i7 = (str(i[7]))
            i8 = (str(i[8]))
        initial_data = {'ID': i0, 'Store_ID': i1, 'Store_Name': i2, 'Region': i3, 'Head_Office': i4, 'Created_At': i5, 'Updated_At': i6, 'Created_By': i7,
                        'Updated_By': i8}
        form = StoreUpdate(initial=initial_data)
        if 'filter' in request.POST:
            id_ = request.POST.get('ID')
            sd_ = request.POST.get('Store_ID')
            sn_ = request.POST.get('Store_Name')
            updated_at = now_
            updated_by = request.POST.get('Updated_By')
            dfsp = pd.DataFrame(
                columns=['id', 'store_id', 'store_name', 'updated_at', 'updated_by_id'])
            dfsp.loc[0] = id_, sd_, sn_, updated_at, updated_by
            for index, row in dfsp.iterrows():
                cursor.execute("UPDATE Stores SET store_id = ?, store_name = ?, updated_at = ?, updated_by_id = ? WHERE id = ?",
                               (row['store_id'], row['store_name'], row['updated_at'], row['updated_by_id'], row['id']))
                cursor.commit()
                store_one = fetch_store_data_updated()
                store_ = store_one.store_data_updated()
                context1 = {'html_table': store_}
                return render(request, "pages/pages/stores.html", context1)

        return render(request, "pages/pages/edit_records/edit_stores.html",
                      {'form': form, 'initial_data': initial_data})

    return render(request, "pages/pages/stores.html", context)

def store_add(request):
    now_ = datetime.now().replace(microsecond=0)
    if 'ksaInput' in request.GET:
        ksa_input = request.GET['ksaInput']
    if 'storeInput' in request.GET:
        store_input = request.GET['storeInput'].upper()
    if 'regionInput' in request.GET:
        region_input = request.GET['regionInput']
    if 'headInput' in request.GET:
        head_input = request.GET['headInput']
    if 'nameInput' in request.GET:
        name_input = request.GET['nameInput']
        cursor.execute("SELECT id FROM auth_user WHERE username LIKE '%' + ? + '%'", name_input)
        rs1 = dictfetchall(cursor)
        id_row = pd.DataFrame(rs1)
        for i in id_row.values:
            i1 = (str(i[0]))
        # print(i1)
        cursor.execute("SELECT id FROM Regions WHERE region_name LIKE '%' + ? + '%'", region_input)
        rs1 = dictfetchall(cursor)
        id_row = pd.DataFrame(rs1)
        for i in id_row.values:
            i2 = (str(i[0]))
        # print(i2)

        dfs = pd.DataFrame(
            columns=['KSA', 'Store', 'Region', 'Head_Office', 'Create_Time', 'Updated_Time', 'User', 'Updated_By_User'])
        dfs.loc[0] = ksa_input, store_input, i2, head_input, now_, now_, i1, i1,
        print(dfs.to_string())
        for index, row in dfs.iterrows():

            cursor.execute("INSERT INTO Stores (store_id, store_name, region_id, is_head_office, created_at, updated_at, created_by_id, updated_by_id) "
                            "VALUES (?,?,?,?,?,?,?,?)",
                           row['KSA'], row['Store'], row['Region'], row['Head_Office'], row['Create_Time'], row['Updated_Time'], row['User'], row['Updated_By_User'])
            cursor.commit()

            return render(request, "pages/pages/add_records/records_added_pages/store_added_table.html")
    return render(request, "pages/pages/add_records/add_store.html")
##REGIONAL COACHES
def r_c(request):
    rc_one = fetch_regional_coach_data()
    rc_ = rc_one.rc_data()
    context = {'html_table': rc_}
    now_ = datetime.now().replace(microsecond=0)
    if 'word' in request.GET:
        word_input = request.GET['word']
        params = word_input
        cursor.execute("SELECT * FROM RegionalCoaches WHERE first_name LIKE '%' + ? + '%'", params)
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
            i7 = (str(i[7]))
            i8 = (str(i[8]))
            i9 = (str(i[9]))
            i10 = (str(i[10]))
        initial_data = {'ID': i0, 'First_Name': i1, 'Last_Name': i2, 'Cell_Phone': i3, 'Email_Address': i4,
                        'Employee_Code': i5, 'Is_Active': i6, 'Created_At': i7, 'Updated_At': i8, 'Created_By': i9,
                        'Updated_By': i10}
        form = RCUpdate(initial=initial_data)
        if 'filter' in request.POST:
            id_ = request.POST.get('ID')
            fn_ = request.POST.get('First_Name')
            ln_ = request.POST.get('Last_Name')
            cp_ = request.POST.get('Cell_Phone')
            ea_ = request.POST.get('Email_Address')
            ec_ = request.POST.get('Employee_Code')
            ia_ = request.POST.get('Is_Active')
            updated_at = now_
            updated_by = request.POST.get('Updated_By')
            dfsp = pd.DataFrame(
                columns=['id', 'first_name', 'last_name', 'cell_phone', 'email_address', 'employee_code', 'is_active',
                         'updated_at', 'updated_by_id'])
            dfsp.loc[0] = id_, fn_, ln_, cp_, ea_, ec_, ia_, updated_at, updated_by
            for index, row in dfsp.iterrows():
                cursor.execute(
                    "UPDATE RegionalCoaches SET first_name = ?, last_name = ?, cell_phone = ?, email_address = ?, "
                    "employee_code = ?, is_active = ?, updated_at = ?, updated_by_id = ? WHERE id = ?",
                    (row['first_name'], row['last_name'], row['cell_phone'], row['email_address'],
                     row['employee_code'], row['is_active'], row['updated_at'], row['updated_by_id'], row['id']))
                cursor.commit()
                rc_up = fetch_regional_coach_data_updated()
                rc__ = rc_up.rc_data_updated()
                context1 = {'html_table': rc__}
                return render(request, "pages/pages/regional_coaches.html", context1)
        return render(request, "pages/pages/edit_records/edit_rc.html",
                      {'form': form, 'initial_data': initial_data})

    return render(request, "pages/pages/regional_coaches.html", context)

def add_rc(request):
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
    if 'nameInput' in request.GET:
        name_input = request.GET['nameInput']
        cursor.execute("SELECT id FROM auth_user WHERE username LIKE '%' + ? + '%'", name_input)
        rs1 = dictfetchall(cursor)
        id_row = pd.DataFrame(rs1)
        for i in id_row.values:
            i1 = (str(i[0]))
        # print(i1)

        dfs = pd.DataFrame(
            columns=['F_Name', 'L_Name', 'Cell', 'Email', 'EMP_Code', 'is_active', 'created_at', 'updated_at', 'created_by_id', 'updated_by_id'])
        dfs.loc[0] = fn_input, ln_input, c_input, e_input, emp_input, active_input, now_, now_, i1, i1,
        print(dfs.to_string())
        for index, row in dfs.iterrows():
            cursor.execute(
                "INSERT INTO RegionalCoaches (first_name, last_name, cell_phone, email_address, employee_code, is_active, created_at, updated_at, created_by_id, updated_by_id) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                row['F_Name'], row['L_Name'], row['Cell'], row['Email'], row['EMP_Code'], row['is_active'],
                row['created_at'], row['updated_at'], row['created_by_id'], row['updated_by_id'])
            cursor.commit()
            return render(request, "pages/pages/add_records/records_added_pages/rc_added.html")
    return render(request, "pages/pages/add_records/add_regional_coach.html")

def view_rc_a(request):
    rca_one = fetch_rca_data()
    rca_ = rca_one.rca_data()
    context = {'html_table': rca_}
    return render(request, "pages/pages/add_records/assignments/rc_assignments.html", context)

def add_rc_a(request):
    now_ = datetime.now().replace(microsecond=0)
    if 'fnInput' in request.GET:
        fn_input = request.GET['fnInput'].upper()
        cursor.execute("SELECT id FROM RegionalCoaches WHERE first_name LIKE '%' + ? + '%'", fn_input)
        rs1 = dictfetchall(cursor)
        id_row = pd.DataFrame(rs1)
        for ii in id_row.values:
            region_id = (str(ii[0]))

    if 'lnInput' in request.GET:
        ln_input = request.GET['lnInput'].upper()
        cursor.execute("SELECT id FROM Stores WHERE store_name LIKE '%' + ? + '%'", ln_input)
        rs1 = dictfetchall(cursor)
        id_row = pd.DataFrame(rs1)
        for ii in id_row.values:
            store_id = (str(ii[0]))
            print(store_id)
    if 'cInput' in request.GET:
        c_input = request.GET['cInput']
    if 'eInput' in request.GET:
        e_input = request.GET['eInput'].upper()
    if 'nameInput' in request.GET:
        name_input = request.GET['nameInput']
        cursor.execute("SELECT id FROM auth_user WHERE username LIKE '%' + ? + '%'", name_input)
        rs1 = dictfetchall(cursor)
        id_row = pd.DataFrame(rs1)
        for i in id_row.values:
            user_name = (str(i[0]))
        # print(i1)

        dfs = pd.DataFrame(
            columns=['rc_id', 'store_id', 's_date', 'e_date', 'created_at', 'updated_at', 'created_by_id', 'updated_by_id'])
        dfs.loc[0] = region_id, store_id, c_input, e_input, now_, now_, user_name, user_name
        print(dfs.to_string())
        for index, row in dfs.iterrows():
            cursor.execute(
                "INSERT INTO RegionalCoachAssignments (regional_coach_id, store_id, start_date, end_date, created_at, updated_at, created_by_id, updated_by_id) "
                "VALUES (?,?,?,?,?,?,?,?)",
                row['rc_id'], row['store_id'], row['s_date'], row['e_date'],
                row['created_at'], row['updated_at'], row['created_by_id'], row['updated_by_id'])
            cursor.commit()
            rcau_one = fetch_rca_updated()
            rcua_ = rcau_one.rca_data_updated()
            context1 = {'html_table': rcua_}
            return render(request, "pages/pages/add_records/assignments/rc_assignments.html", context1)
    return render(request, "pages/pages/add_records/assignments/add_rc_assignments.html")
#AREA COACHES
def a_c(request):
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
            i7 = (str(i[7]))
            i8 = (str(i[8]))
            i9 = (str(i[9]))
            i10 = (str(i[10]))
        initial_data = {'ID': i0, 'First_Name': i1, 'Last_Name': i2, 'Cell_Phone': i3, 'Email_Address': i4,
                        'Employee_Code': i5, 'Is_Active': i6, 'Created_At': i7, 'Updated_At': i8, 'Created_By': i9,
                        'Updated_By': i10}
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
            updated_by = request.POST.get('Updated_By')
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

def add_ac(request):
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
    if 'nameInput' in request.GET:
        name_input = request.GET['nameInput']
        cursor.execute("SELECT id FROM auth_user WHERE username LIKE '%' + ? + '%'", name_input)
        rs1 = dictfetchall(cursor)
        id_row = pd.DataFrame(rs1)
        for i in id_row.values:
            i1 = (str(i[0]))
        # print(i1)

        dfs = pd.DataFrame(
            columns=['F_Name', 'L_Name', 'Cell', 'Email', 'EMP_Code', 'is_active', 'created_at', 'updated_at', 'created_by_id', 'updated_by_id'])
        dfs.loc[0] = fn_input, ln_input, c_input, e_input, emp_input, active_input, now_, now_, i1, i1,
        # print(dfs.to_string())
        for index, row in dfs.iterrows():
            cursor.execute(
                "INSERT INTO AreaCoaches (first_name, last_name, cell_phone, email_address, employee_code, is_active, created_at, updated_at, created_by_id, updated_by_id) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                row['F_Name'], row['L_Name'], row['Cell'], row['Email'], row['EMP_Code'], row['is_active'],
                row['created_at'], row['updated_at'], row['created_by_id'], row['updated_by_id'])
            cursor.commit()
            return render(request, "pages/pages/add_records/records_added_pages/ac_added.html")
    return render(request, "pages/pages/add_records/add_area_coach.html")

def view_ac_a(request):
    aca_one = fetch_aca_data()
    aca_ = aca_one.aca_data()
    context = {'html_table': aca_}
    return render(request, "pages/pages/add_records/assignments/ac_assignments.html", context)

def add_ac_a(request):
    now_ = datetime.now().replace(microsecond=0)
    if 'fnInput' in request.GET:
        fn_input = request.GET['fnInput'].upper()
        cursor.execute("SELECT id FROM AreaCoaches WHERE first_name LIKE '%' + ? + '%'", fn_input)
        rs1 = dictfetchall(cursor)
        id_row = pd.DataFrame(rs1)
        for ii in id_row.values:
            region_id = (str(ii[0]))

    if 'lnInput' in request.GET:
        ln_input = request.GET['lnInput'].upper()
        cursor.execute("SELECT id FROM RegionalCoaches WHERE first_name LIKE '%' + ? + '%'", ln_input)
        rs1 = dictfetchall(cursor)
        id_row = pd.DataFrame(rs1)
        for ii in id_row.values:
            store_id = (str(ii[0]))
            print(store_id)
    if 'cInput' in request.GET:
        c_input = request.GET['cInput']
    if 'eInput' in request.GET:
        e_input = request.GET['eInput'].upper()
    if 'nameInput' in request.GET:
        name_input = request.GET['nameInput']
        cursor.execute("SELECT id FROM auth_user WHERE username LIKE '%' + ? + '%'", name_input)
        rs1 = dictfetchall(cursor)
        id_row = pd.DataFrame(rs1)
        for i in id_row.values:
            user_name = (str(i[0]))
        # print(i1)

        dfs = pd.DataFrame(
            columns=['rc_id', 'store_id', 's_date', 'e_date', 'created_at', 'updated_at', 'created_by_id', 'updated_by_id'])
        dfs.loc[0] = region_id, store_id, c_input, e_input, now_, now_, user_name, user_name
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
    return render(request, "pages/pages/add_records/assignments/add_ac_assignments.html")


#BUSINESS PARTNERS
def b_p(request):
    bp_one = fetch_bp_data()
    bp_ = bp_one.bp_data()
    context = {'html_table': bp_}
    now_ = datetime.now().replace(microsecond=0)
    if 'word' in request.GET:
        word_input = request.GET['word']
        params = word_input
        cursor.execute("SELECT * FROM BusinessPartners WHERE first_name LIKE '%' + ? + '%'", params)
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
            i7 = (str(i[7]))
            i8 = (str(i[8]))
            i9 = (str(i[9]))
            i10 = (str(i[10]))
        initial_data = {'ID': i0, 'First_Name': i1, 'Last_Name': i2, 'Cell_Phone': i3, 'Email_Address': i4,
                        'Employee_Code': i5, 'Is_Active': i6, 'Created_At': i7, 'Updated_At': i8, 'Created_By': i9,
                        'Updated_By': i10}
        form = BPUpdate(initial=initial_data)
        if 'filter' in request.POST:
            id_ = request.POST.get('ID')
            fn_ = request.POST.get('First_Name')
            ln_ = request.POST.get('Last_Name')
            cp_ = request.POST.get('Cell_Phone')
            ea_ = request.POST.get('Email_Address')
            ec_ = request.POST.get('Employee_Code')
            ia_ = request.POST.get('Is_Active')
            updated_at = now_
            updated_by = request.POST.get('Updated_By')
            dfsp = pd.DataFrame(
                columns=['id', 'first_name', 'last_name', 'cell_phone', 'email_address', 'employee_code', 'is_active',
                         'updated_at', 'updated_by_id'])
            dfsp.loc[0] = id_, fn_, ln_, cp_, ea_, ec_, ia_, updated_at, updated_by
            for index, row in dfsp.iterrows():
                cursor.execute(
                    "UPDATE BusinessPartners SET first_name = ?, last_name = ?, cell_phone = ?, email_address = ?, "
                    "employee_code = ?, is_active = ?, updated_at = ?, updated_by_id = ? WHERE id = ?",
                    (row['first_name'], row['last_name'], row['cell_phone'], row['email_address'],
                     row['employee_code'], row['is_active'], row['updated_at'], row['updated_by_id'], row['id']))
                cursor.commit()
                bp_up = fetch_bp_data_updated()
                bp__ = bp_up.bp_data_updated()
                context1 = {'html_table': bp__}
                return render(request, "pages/pages/business_partners.html", context1)
        return render(request, "pages/pages/edit_records/edit_bp.html",
                      {'form': form, 'initial_data': initial_data})
    return render(request, "pages/pages/business_partners.html", context)

def add_bp(request):
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
    if 'nameInput' in request.GET:
        name_input = request.GET['nameInput']
        cursor.execute("SELECT id FROM auth_user WHERE username LIKE '%' + ? + '%'", name_input)
        rs1 = dictfetchall(cursor)
        id_row = pd.DataFrame(rs1)
        for i in id_row.values:
            i1 = (str(i[0]))
        # print(i1)

        dfs = pd.DataFrame(
            columns=['F_Name', 'L_Name', 'Cell', 'Email', 'EMP_Code', 'is_active', 'created_at', 'updated_at', 'created_by_id', 'updated_by_id'])
        dfs.loc[0] = fn_input, ln_input, c_input, e_input, emp_input, active_input, now_, now_, i1, i1,
        # print(dfs.to_string())
        for index, row in dfs.iterrows():
            cursor.execute(
                "INSERT INTO BusinessPartners (first_name, last_name, cell_phone, email_address, employee_code, is_active, created_at, updated_at, created_by_id, updated_by_id) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                row['F_Name'], row['L_Name'], row['Cell'], row['Email'], row['EMP_Code'], row['is_active'],
                row['created_at'], row['updated_at'], row['created_by_id'], row['updated_by_id'])
            cursor.commit()
            return render(request, "pages/pages/add_records/records_added_pages/bp_added.html")
    return render(request, "pages/pages/add_records/add_business_partner.html")
def view_bp_a(request):
    bpa_one = fetch_bpa_data()
    bpa_ = bpa_one.bpa_data()
    context = {'html_table': bpa_}
    return render(request, "pages/pages/add_records/assignments/bp_asignments.html", context)

def add_bp_a(request):
    now_ = datetime.now().replace(microsecond=0)
    if 'fnInput' in request.GET:
        fn_input = request.GET['fnInput'].upper()
        cursor.execute("SELECT id FROM BusinessPartners WHERE first_name LIKE '%' + ? + '%'", fn_input)
        rs1 = dictfetchall(cursor)
        id_row = pd.DataFrame(rs1)
        for ii in id_row.values:
            region_id = (str(ii[0]))

    if 'lnInput' in request.GET:
        ln_input = request.GET['lnInput'].upper()
        cursor.execute("SELECT id FROM AreaCoaches WHERE first_name LIKE '%' + ? + '%'", ln_input)
        rs1 = dictfetchall(cursor)
        id_row = pd.DataFrame(rs1)
        for ii in id_row.values:
            store_id = (str(ii[0]))
            print(store_id)
    if 'cInput' in request.GET:
        c_input = request.GET['cInput']
    if 'eInput' in request.GET:
        e_input = request.GET['eInput'].upper()
    if 'nameInput' in request.GET:
        name_input = request.GET['nameInput']
        cursor.execute("SELECT id FROM auth_user WHERE username LIKE '%' + ? + '%'", name_input)
        rs1 = dictfetchall(cursor)
        id_row = pd.DataFrame(rs1)
        for i in id_row.values:
            user_name = (str(i[0]))
        # print(i1)

        dfs = pd.DataFrame(
            columns=['rc_id', 'store_id', 's_date', 'e_date', 'created_at', 'updated_at', 'created_by_id', 'updated_by_id'])
        dfs.loc[0] = region_id, store_id, c_input, e_input, now_, now_, user_name, user_name
        print(dfs.to_string())
        for index, row in dfs.iterrows():
            cursor.execute(
                "INSERT INTO BusinessPartnerAssignments (business_partner_id, area_coach_id, start_date, end_date, created_at, updated_at, created_by_id, updated_by_id) "
                "VALUES (?,?,?,?,?,?,?,?)",
                row['rc_id'], row['store_id'], row['s_date'], row['e_date'],
                row['created_at'], row['updated_at'], row['created_by_id'], row['updated_by_id'])
            cursor.commit()
            bpua_one = fetch_bpa_updated()
            bpuaa_ = bpua_one.bpa_data_updated()
            context11 = {'html_table': bpuaa_}
            return render(request, "pages/pages/add_records/assignments/bp_asignments.html", context11)
    return render(request, "pages/pages/add_records/assignments/add_bp_assignments.html")
#EMPLOYEES
def e_(request):
    e_one = fetch_e_data()
    e_ = e_one.e_data()
    context = {'html_table': e_}
    return render(request, "pages/pages/employees.html", context)

# def add_e(request):
#     now_ = datetime.now().replace(microsecond=0)
#     if 'fnInput' in request.GET:
#         fn_input = request.GET['fnInput'].upper()
#     if 'lnInput' in request.GET:
#         ln_input = request.GET['lnInput'].upper()
#     if 'cInput' in request.GET:
#         c_input = request.GET['cInput']
#     if 'eInput' in request.GET:
#         e_input = request.GET['eInput'].upper()
#     if 'empInput' in request.GET:
#         emp_input = request.GET['empInput']
#     if 'activeInput' in request.GET:
#         active_input = request.GET['activeInput']
#     if 'nameInput' in request.GET:
#         name_input = request.GET['nameInput']
#         cursor.execute("SELECT id FROM auth_user WHERE username LIKE '%' + ? + '%'", name_input)
#         rs1 = dictfetchall(cursor)
#         id_row = pd.DataFrame(rs1)
#         for i in id_row.values:
#             i1 = (str(i[0]))
#         # print(i1)
#
#         dfs = pd.DataFrame(
#             columns=['F_Name', 'L_Name', 'Cell', 'Email', 'EMP_Code', 'is_active', 'created_at', 'updated_at', 'created_by_id', 'updated_by_id'])
#         dfs.loc[0] = fn_input, ln_input, c_input, e_input, emp_input, active_input, now_, now_, i1, i1,
#         # print(dfs.to_string())
#         for index, row in dfs.iterrows():
#             cursor.execute(
#                 "INSERT INTO Employees (first_name, last_name, cell_phone, email_address, employee_code, is_active, created_at, updated_at, created_by_id, updated_by_id) "
#                 "VALUES (?,?,?,?,?,?,?,?,?,?)",
#                 row['F_Name'], row['L_Name'], row['Cell'], row['Email'], row['EMP_Code'], row['is_active'],
#                 row['created_at'], row['updated_at'], row['created_by_id'], row['updated_by_id'])
#             cursor.commit()
#             return render(request, "pages/pages/add_records/records_added_pages/bp_added.html")
#     return render(request, "pages/pages/add_records/add_business_partner.html")

def test(request):
    pass
#     region_one = fetch_region_data()
#     region_ = region_one.region_data()
#     context = {'html_table': region_}
#
#
#     now_ = datetime.now().replace(microsecond=0)
#
#     if 'word' in request.GET:
#         word_input = request.GET['word']
#         params = word_input
#         cursor.execute("SELECT * FROM Regions WHERE region_name LIKE '%' + ? + '%'", params)
#         rs1 = dictfetchall(cursor)
#         df = pd.DataFrame(rs1)
#         dfsd = df.to_records(index=False)
#         for i in dfsd:
#             i0 = (str(i[0]))
#             i1 = (str(i[1]))
#             i2 = (str(i[2]))
#             i3 = (str(i[3]))
#             i4 = (str(i[4]))
#             i5 = (str(i[5]))
#             # print(i0)
#         initial_data = {'ID': i0, 'Region_Name': i1, 'Created_At': i2, 'Updated_At': i3, 'Created_By': i4, 'Updated_By': i5}
#         form = RegionUpdate(initial=initial_data)
#         if 'filter' in request.POST:
#             id_ = request.POST.get('ID')
#             rn_ = request.POST.get('Region_Name')
#             updated_at = now_
#             updated_by = request.POST.get('Updated_By')
#             dfsp = pd.DataFrame(
#                 columns=['id', 'region_name', 'updated_at', 'updated_by_id'])
#             dfsp.loc[0] = id_, rn_, updated_at, updated_by
#             for index, row in dfsp.iterrows():
#                 cursor.execute("UPDATE Regions SET region_name = ?, updated_at = ?, updated_by_id = ? WHERE id = ?",
#                                (row['region_name'], row['updated_at'], row['updated_by_id'], row['id']))
#
#                 cursor.commit()
#                 region_one = fetch_region_data_updated()
#                 region_ = region_one.region_data_updated()
#                 context1 = {'html_table': region_}
#                 return render(request, "pages/pages/testing/test.html", context1)
#
#
#         return render(request, "pages/pages/testing/test_table.html", {'form': form, 'initial_data': initial_data})
#
#
#     return render(request, "pages/pages/testing/test.html", context)




# Pages -> Profile
def profile_overview(request):
    context = {
        "parent": "pages",
        "sub_parent": "profile",
        "segment": "profile_overview",
    }
    return render(request, "pages/profile/overview.html", context)


def teams(request):
    context = {"parent": "pages", "sub_parent": "profile", "segment": "teams"}
    return render(request, "pages/profile/teams.html", context)
#
#
def projects(request):
    context = {"parent": "pages", "sub_parent": "profile", "segment": "projects"}
    return render(request, "pages/profile/projects.html", context)
#
#
# # Pages -> Users
def reports(request):
    context = {"parent": "pages", "sub_parent": "users", "segment": "reports"}
    return render(request, "pages/users/reports.html", context)


def new_user(request):
    context = {"parent": "pages", "sub_parent": "users", "segment": "new_user"}
    return render(request, "pages/users/new-user.html", context)

####################################
# Pages -> Accounts



def billing(request):
    context = {"parent": "accounts", "segment": "billing"}
    return render(request, "pages/account/billing.html", context)


def invoice(request):
    context = {"parent": "accounts", "segment": "invoice"}
    return render(request, "pages/account/invoice.html", context)


def security(request):
    context = {"parent": "accounts", "segment": "security"}
    return render(request, "pages/account/security.html", context)
#
#
# # Pages -> Projects
def general(request):
    context = {"parent": "projects", "segment": "general"}
    return render(request, "pages/projects/general.html", context)



# Authentication -> Register
def basic_register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/accounts/login/basic-login/")
    else:
        form = RegistrationForm()

    context = {"form": form}
    return render(request, "authentication/signup/basic.html", context)


def cover_register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/accounts/login/cover-login/")
    else:
        form = RegistrationForm()

    context = {"form": form}
    return render(request, "authentication/signup/cover.html", context)


def illustration_register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/accounts/login/illustration-login/")
    else:
        form = RegistrationForm()

    context = {"form": form}
    return render(request, "authentication/signup/illustration.html", context)


# Authentication -> Login
class BasicLoginView(LoginView):
    template_name = "authentication/signin/basic.html"
    form_class = LoginForm


class CoverLoginView(LoginView):
    template_name = "authentication/signin/cover.html"
    form_class = LoginForm


class IllustrationLoginView(LoginView):
    template_name = "authentication/signin/illustration.html"
    form_class = LoginForm

# Authentication -> Reset
class BasicResetView(PasswordResetView):
    template_name = "authentication/reset/basic.html"
    form_class = UserPasswordResetForm


class CoverResetView(PasswordResetView):
    template_name = "authentication/reset/cover.html"
    form_class = UserPasswordResetForm


class IllustrationResetView(PasswordResetView):
    template_name = "authentication/reset/illustration.html"
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "authentication/reset-confirm/basic.html"
    form_class = UserSetPasswordForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = "authentication/change/basic.html"
    form_class = UserPasswordChangeForm


# Authentication -> Lock
def basic_lock(request):
    return render(request, "authentication/lock/basic.html")


def cover_lock(request):
    return render(request, "authentication/lock/cover.html")


def illustration_lock(request):
    return render(request, "authentication/lock/illustration.html")


# Authentication -> Verification
def basic_verification(request):
    return render(request, "authentication/verification/basic.html")


def cover_verification(request):
    return render(request, "authentication/verification/cover.html")


def illustration_verification(request):
    return render(request, "authentication/verification/illustration.html")


# Error
def error_404(request, exception=None):
    return render(request, "authentication/error/404.html")


def error_500(request, exception=None):
    return render(request, "authentication/error/500.html")


def logout_view(request):
    logout(request)
    return redirect("/accounts/login/basic-login/")
