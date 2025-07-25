import logger
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    UsernameField,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from apps.db.connections.connection_string import conn_str
from apps.db.dict_fetch.fetch_data import dictfetchall
import pyodbc
import pandas as pd
from datetime import datetime

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

from apps.models.core import *
from django.db import models
from django.core.exceptions import ValidationError
import re


class Region_Dropdown(forms.Form):
    my_model_choice = forms.ModelChoiceField(queryset=Region.objects.all(), label="Region")
class Store_Only(BaseModel):
    """
    Individual stores and head office
    """
    store_id = models.CharField(
        max_length=10,
        unique=True,
        validators=[validate_store_id],
        help_text="Format: 3 letters + 1-5 numbers (e.g., ADP1)"
    )
    store_name = models.CharField(max_length=30)
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name='stores',
        null=True,
        blank=True
    )
    is_head_office = models.BooleanField(default=False)

    class Meta:
        db_table = 'Stores'
        ordering = ['store_id']

    def __str__(self):
        return f"{self.store_name}"
class Store_Dropdown(forms.Form):
    my_model_choice = forms.ModelChoiceField(queryset=Store_Only.objects.all(), label="Store")


class RegionalCoach_Only(BaseModel):
    """
    Regional coaches who oversee multiple stores
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


    class Meta:
        db_table = 'RegionalCoaches'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
class RC_Dropdown(forms.Form):
    my_model_choice = forms.ModelChoiceField(queryset=RegionalCoach_Only.objects.all(), label="Regional Coach")

class AreaCoach_Only(BaseModel):
    """
    Area coaches who oversee regional coaches
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cell_phone = models.CharField(max_length=15, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    employee_code = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'AreaCoaches'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
class AC_Dropdown(forms.Form):
    my_model_choice = forms.ModelChoiceField(queryset=AreaCoach_Only.objects.all(), label="Area Coach")

class BusinessPartner_Only(BaseModel):
    """
    Business partners who oversee area coaches
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    cell_phone = models.CharField(max_length=15, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    employee_code = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'BusinessPartners'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
class BP_Dropdown(forms.Form):
    my_model_choice = forms.ModelChoiceField(queryset=BusinessPartner_Only.objects.all(), label="Business Partner")
class Employee_Only(BaseModel):
    my_choice = forms.ChoiceField(choices=[('value1', 'Option 1'), ('value2', 'Option 2')])

class E_Dropdown(forms.Form):
    my_choice_field = forms.ChoiceField(
        choices=[
            ('EMPLOYEE', 'EMPLOYEE'),
            ('AREA COACH', 'AREA COACH'),
            ('REGIONAL COACH', 'REGIONAL COACH'),
            ('BUSINESS PARTNER', 'BUSINESS PARTNER'),
        ],
        label='Employee Type'
    )
