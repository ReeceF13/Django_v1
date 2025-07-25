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
from apps.pages.forms import *

#CLASS IMPORTS

from apps.db.table_counts.all_counts import *

from apps.db.connections.connection_string import conn_str

import pyodbc
import pandas as pd
from datetime import datetime


conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Dashboard
def default(request):
    if request.user.is_authenticated:
        # User is logged in
        current_user = request.user
        # print(f"Logged in user: {current_user.username}")
        user__ = (f" Welcome {current_user.username}")
    store_ = count_s()
    cnt_ = store_.stores_count()
    rc_cnt = store_.rc_count()
    ac_cnt = store_.ac_count()
    bp_cnt = store_.bp_count()
    store_hist = store_.store_history()

    context = {"parent": "dashboard", "segment": "default", 'user': user__, 'stores': cnt_, 'regional_': rc_cnt, 'area_': ac_cnt, 'business_': bp_cnt, 'store_hist': store_hist}
    return render(request, "pages/dashboards/default.html", context)

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
