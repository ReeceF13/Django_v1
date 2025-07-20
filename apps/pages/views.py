from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordChangeView,
    PasswordResetConfirmView,
)
from apps.pages.forms import (
    RegistrationForm,
    LoginForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
    UserPasswordChangeForm,
)
from django.contrib.auth import logout
from apps.db.regions.region_query import fetch_region_data
from apps.db.stores.store_query import fetch_store_data
from apps.db.regional_coaches.rc_query import fetch_regional_coach_data
from datetime import datetime
from django.contrib.auth.decorators import login_required
from apps.pages.models import Region_r


from .forms import MyForm, MyModelForm
from apps.db.connections.connection_string import conn_str
from apps.db.dict_fetch.fetch_data import dictfetchall
import pyodbc
import pandas as pd
from datetime import datetime

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
            return render(request, "pages/pages/region_added_table.html", context)

    return render(request, "pages/pages/add_records/add_region.html")

def stores_(request):
    store_one = fetch_store_data()
    store_ = store_one.store_data()
    context = {'html_table': store_}
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

            return render(request, "pages/pages/add_records/store_added_table.html")
    return render(request, "pages/pages/add_records/add_store.html")
##REGIONAL COACHES
def r_c(request):
    rc_one = fetch_regional_coach_data()
    rc_ = rc_one.rc_data()
    context = {'html_table': rc_}
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
            return render(request, "pages/pages/add_records/rc_added.html")
    return render(request, "pages/pages/add_records/add_regional_coach.html")
def test(request):
    if request.method == 'POST':
        form = MyForm(request.POST)  # Or MyModelForm(request.POST)
        if form.is_valid():
            selected_option = form.cleaned_data['my_dropdown']  # Access the selected value
            # Process the data
            return redirect('success_page')
    else:
        form = MyForm()  # Or MyModelForm()
    return render(request, 'pages/pages/testing/test.html', {'form': form})

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


def projects(request):
    context = {"parent": "pages", "sub_parent": "profile", "segment": "projects"}
    return render(request, "pages/profile/projects.html", context)


# Pages -> Users
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


# Pages -> Projects
def general(request):
    context = {"parent": "projects", "segment": "general"}
    return render(request, "pages/projects/general.html", context)


def timeline(request):
    context = {"parent": "projects", "segment": "timeline"}
    return render(request, "pages/projects/timeline.html", context)


def new_project(request):
    context = {"parent": "projects", "segment": "new_project"}
    return render(request, "pages/projects/new-project.html", context)


# Applications
# def kanban(request):
#     context = {"parent": "applications", "segment": "kanban"}
#     return render(request, "pages/applications/kanban.html", context)


# def wizard(request):
#     context = {"parent": "applications", "segment": "wizard"}
#     return render(request, "pages/applications/wizard.html", context)


def datatables(request):
    context = {"parent": "applications", "segment": "datatables"}
    return render(request, "pages/applications/datatables.html", context)


def calendar(request):
    context = {"parent": "applications", "segment": "calendar"}
    return render(request, "pages/applications/calendar.html", context)


def analytics(request):
    context = {"parent": "applications", "segment": "analytics"}
    return render(request, "pages/applications/analytics.html", context)


# Ecommerce
def overview(request):
    context = {"parent": "ecommerce", "segment": "overview"}
    return render(request, "pages/ecommerce/overview.html", context)


def referral(request):
    context = {"parent": "ecommerce", "segment": "referral"}
    return render(request, "pages/ecommerce/referral.html", context)


# Ecommerce -> Products
def new_product(request):
    context = {
        "parent": "ecommerce",
        "sub_parent": "products",
        "segment": "new_product",
    }
    return render(request, "pages/ecommerce/products/new-product.html", context)


def edit_product(request):
    context = {
        "parent": "ecommerce",
        "sub_parent": "products",
        "segment": "edit_product",
    }
    return render(request, "pages/ecommerce/products/edit-product.html", context)


def product_page(request):
    context = {
        "parent": "ecommerce",
        "sub_parent": "products",
        "segment": "product_page",
    }
    return render(request, "pages/ecommerce/products/product-page.html", context)


def products_list(request):
    context = {
        "parent": "ecommerce",
        "sub_parent": "products",
        "segment": "products_list",
    }
    return render(request, "pages/ecommerce/products/products-list.html", context)


# Ecommerce -> Orders
def order_list(request):
    context = {"parent": "ecommerce", "sub_parent": "orders", "segment": "order_list"}
    return render(request, "pages/ecommerce/orders/list.html", context)


def order_details(request):
    context = {
        "parent": "ecommerce",
        "sub_parent": "orders",
        "segment": "order_details",
    }
    return render(request, "pages/ecommerce/orders/details.html", context)


# Team
def team_messages(request):
    context = {"parent": "team", "segment": "team_messages"}
    return render(request, "pages/team/messages.html", context)


def team_new_user(request):
    context = {"parent": "team", "segment": "team_new_user"}
    return render(request, "pages/team/new-user.html", context)


def team_overview(request):
    context = {"parent": "team", "segment": "team_overview"}
    return render(request, "pages/team/overview.html", context)


def team_projects(request):
    context = {"parent": "team", "segment": "team_projects"}
    return render(request, "pages/team/projects.html", context)


def team_reports(request):
    context = {"parent": "team", "segment": "team_reports"}
    return render(request, "pages/team/reports.html", context)


def team_teams(request):
    context = {"parent": "team", "segment": "team_teams"}
    return render(request, "pages/team/teams.html", context)


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
