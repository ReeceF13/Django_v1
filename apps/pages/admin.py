from django.contrib import admin

from django.apps import apps
from django.contrib import admin
from django.contrib import admin
from apps.models.core import Region, Store, RegionalCoach, AreaCoach, BusinessPartner, Employee
from apps.models.assignments import RegionalCoachAssignment, AreaCoachAssignment, BusinessPartnerAssignment
# Register your models here.

# app_models = apps.get_app_config('pages').get_models()
# for model in app_models:
#     try:
#
#         admin.site.register(model)
#
#     except Exception:
#         pass



@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['region_name', 'store_count', 'created_at']
    search_fields = ['region_name']

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['store_id', 'store_name', 'region', 'is_head_office', 'employee_count']
    list_filter = ['region', 'is_head_office', 'created_at']
    search_fields = ['store_id', 'store_name']

@admin.register(RegionalCoach)
class RegionalCoachAdmin(admin.ModelAdmin):
    list_display = ['employee_code', 'full_name', 'email_address', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['employee_code', 'first_name', 'last_name']

@admin.register(RegionalCoachAssignment)
class RegionalCoachAssignmentAdmin(admin.ModelAdmin):
    list_display = ['regional_coach', 'store', 'start_date', 'end_date', 'is_current']
    list_filter = ['start_date', 'end_date']
    search_fields = ['regional_coach__employee_code', 'store__store_id']

@admin.register(AreaCoach)
class AreaCoachAdmin(admin.ModelAdmin):
    list_display = ['employee_code', 'full_name', 'email_address', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['employee_code', 'first_name', 'last_name']

@admin.register(AreaCoachAssignment)
class AreaCoachAssignmentAdmin(admin.ModelAdmin):
    list_display = ['area_coach', 'start_date', 'end_date', 'is_current']
    list_filter = ['start_date', 'end_date']
    search_fields = ['area_coach__employee_code']

@admin.register(BusinessPartner)
class BusinessPartnerAdmin(admin.ModelAdmin):
    list_display = ['employee_code', 'full_name', 'email_address', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['employee_code', 'first_name', 'last_name']

@admin.register(BusinessPartnerAssignment)
class BusinessPartnerAssignmentAdmin(admin.ModelAdmin):
    list_display = ['business_partner', 'start_date', 'end_date', 'is_current']
    list_filter = ['start_date', 'end_date']
    search_fields = ['business_partner__employee_code']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_code', 'full_name', 'email_address', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['employee_code', 'first_name', 'last_name']