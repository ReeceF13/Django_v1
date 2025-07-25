from django.urls import path
from apps.pages import views, views_testing, views_regions, views_stores, views_regional_coach, views_area_coach, views_business_partner, views_employees
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Dashboard
    path("", views.default, name="index"),
    # Pages
    path("pages/messages/", views.messages, name="messages"),
    path("pages/widgets/", views.widgets, name="widgets"),
    path("pages/charts/", views.charts_page, name="charts_page"),
    path("pages/sweet-alerts/", views.sweet_alerts, name="sweet_alerts"),
    path("pages/notifications/", views.notifications, name="notifications"),
    #STORE MANAGEMENT PAGES
    #REGIONS
    path("regions/", views_regions.regions_, name="regions"),
    path("add_region/", views_regions.regions_add, name="regions_add"),
    #STORES
    path("stores/", views_stores.view_stores, name="stores"),
    path("add_store/", views_stores.add_store, name="stores_add"),
    #REGIONAL COACH
    path("regional_coaches/", views_regional_coach.view_regional_coaches, name="r_c"),
    path("add_regional_coach/", views_regional_coach.add_regional_coach, name="add_rc"),
    path("add_regional_coach_assignment/", views_regional_coach.add_regional_coach_assignments, name="add_rc_a"),
    path("regional_coach_assignment/", views_regional_coach.view_regional_coach_assignments, name="view_rc_a"),
    #AC
    path("area_coaches/", views_area_coach.view_area_coaches, name="a_c"),
    path("add_area_coach/", views_area_coach.add_area_coach, name="add_ac"),
    path("add_area_coach_assignment/", views_area_coach.add_area_coach_assignments, name="add_ac_a"),
    path("area_coach_assignment/", views_area_coach.view_area_coach_assignments, name="view_ac_a"),
    #BP
    path("business_partners/", views_business_partner.view_business_partners, name="b_p"),
    path("add_business_partner/", views_business_partner.add_business_partner, name="add_bp"),
    path("business_partners_assignment/", views_business_partner.view_business_partner_assignments, name="view_bp_a"),
    path("add_business_partner_assignment/", views_business_partner.add_business_partner_assignment, name="add_bp_a"),
    #EMPLOYEES
    path("employees/", views_employees.view_employees, name="e_"),
    path("add_employee/", views_employees.add_employee, name="add_e"),
    #TESTING
    path("test/", views_testing.test, name="test"),
    path("handle_click/", views_testing.handle_click, name="handle_click"),
    # path("test/", views.button_pressed, name="button_pressed"),





    # Pages -> Profile
    path(
        "pages/profile/profile-overview/",
        views.profile_overview,
        name="profile_overview",
    ),
    path("pages/profile/teams/", views.teams, name="teams"),
    path("pages/profile/projects/", views.projects, name="projects"),
    # Pages -> Users
    path("pages/users/reports/", views.reports, name="reports"),
    path("pages/users/new-user/", views.new_user, name="new_user"),
    # Pages -> Accounts
    #
    path("pages/accounts/billing/", views.billing, name="billing"),
    path("pages/accounts/invoice/", views.invoice, name="invoice"),
    path("pages/accounts/security/", views.security, name="security"),
    # Authentication - Register
    path(
        "accounts/register/basic-register/", views.basic_register, name="basic_register"
    ),
    path(
        "accounts/register/cover-register/", views.cover_register, name="cover_register"
    ),
    path(
        "accounts/register/illustration-register/",
        views.illustration_register,
        name="illustration_register",
    ),
    # Authentication -> Login
    path(
        "accounts/login/basic-login/",
        views.BasicLoginView.as_view(),
        name="basic_login",
    ),
    path(
        "accounts/login/cover-login/",
        views.CoverLoginView.as_view(),
        name="cover_login",
    ),
    path(
        "accounts/login/illustration-login/",
        views.IllustrationLoginView.as_view(),
        name="illustration_login",
    ),
    # Authentication -> Reset
    path(
        "accounts/reset/basic-reset/",
        views.BasicResetView.as_view(),
        name="basic_reset",
    ),
    path(
        "accounts/reset/cover-reset/",
        views.CoverResetView.as_view(),
        name="cover_reset",
    ),
    path(
        "accounts/reset/illustration-reset/",
        views.IllustrationResetView.as_view(),
        name="illustration_reset",
    ),
    path(
        "accounts/password-change/",
        views.UserPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "accounts/password-change-done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="authentication/done/change-done.html"
        ),
        name="password_change_done",
    ),
    path(
        "accounts/password-reset-done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="authentication/done/basic.html"
        ),
        name="password_reset_done",
    ),
    path(
        "accounts/password-reset-confirm/<uidb64>/<token>/",
        views.UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "accounts/password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="authentication/complete/basic.html"
        ),
        name="password_reset_complete",
    ),
    # Authentication -> Lock
    path("accounts/lock/basic-lock/", views.basic_lock, name="basic_lock"),
    path("accounts/lock/cover-lock/", views.cover_lock, name="cover_lock"),
    path(
        "accounts/lock/illustration-lock/",
        views.illustration_lock,
        name="illustration_lock",
    ),
    # Authentication -> Verification
    path(
        "accounts/verification/basic-verification/",
        views.basic_verification,
        name="basic_verification",
    ),
    path(
        "accounts/verification/cover-verification/",
        views.cover_verification,
        name="cover_verification",
    ),
    path(
        "accounts/verification/illustration-verification/",
        views.illustration_verification,
        name="illustration_verification",
    ),
    # Error
    path("error/404/", views.error_404, name="error_404"),
    path("error/500/", views.error_500, name="error_500"),
    path("logout/", views.logout_view, name="logout"),
]
