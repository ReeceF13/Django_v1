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

from apps.models.base import BaseModel
from django.db import models
from django.core.exceptions import ValidationError
import re


def validate_store_id(value):
    """Validate store ID format: 3 letters + 1-5 numbers"""
    pattern = r'^[A-Z]{3}[0-9]{1,5}$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Store ID must be 3 uppercase letters followed by 1-5 numbers (e.g., ADP1, ADP98765)'
        )
class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        label=_("Password Confirmation"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Username",
                }
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email",
            }
        )
    )


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "New Password",
            }
        ),
        label="New Password",
    )
    new_password2 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm New Password"}
        ),
        label="Confirm New Password",
    )


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Old Password"}
        ),
        label="Old Password",
    )
    new_password1 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "New Password"}
        ),
        label="New Password",
    )
    new_password2 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm New Password"}
        ),
        label="Confirm New Password",
    )



from django import forms
from .models import Category

class MyModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name'] # Or other fields you want to display

    # You can also explicitly define the ModelChoiceField if needed
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Select a Category")


class Store_Search(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            with conn.cursor() as cursor:
                # Single query to get both id and name
                cursor.execute("SELECT store_id, store_name FROM Stores")
                stores = dictfetchall(cursor)

                # Create choices list properly
                self.fields['my_dropdown'].choices = [
                    (store['store_id'], store['store_name'])
                    for store in stores
                ]

        except Exception as e:
            logger.error(f"Database error in MyForm: {e}")
            # Provide empty choices as fallback
            self.fields['my_dropdown'] = []

    my_dropdown = forms.ChoiceField(
        choices=[],

    )
class RC_Search(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            with conn.cursor() as cursor:
                # Single query to get both id and name
                cursor.execute("SELECT id, first_name, last_name FROM RegionalCoaches")
                rc_s = dictfetchall(cursor)

                # Create choices list properly
                ordering = ['last_name', 'first_name']
                self.fields['my_dropdown'].choices = [
                    (rc_['id'], rc_['first_name'])
                    for rc_ in rc_s
                ]

        except Exception as e:
            logger.error(f"Database error in MyForm: {e}")
            # Provide empty choices as fallback
            self.fields['my_dropdown'] = []

    my_dropdown = forms.ChoiceField(
        choices=[],
        label="Select Regional Coach"
    )

class RegionUpdate(forms.Form):
    ID = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Region_Name = forms.CharField(max_length=100)
    Created_At = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Updated_At = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Created_By = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Updated_By = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email

class StoreUpdate(forms.Form):
    ID = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Store_ID = forms.CharField(max_length=100)
    Store_Name = forms.CharField(max_length=100)
    Region = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Head_Office = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Created_At = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Updated_At = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Created_By = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Updated_By = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email

class RCUpdate(forms.Form):
    ID = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    First_Name = forms.CharField(max_length=100)
    Last_Name = forms.CharField(max_length=100)
    Cell_Phone = forms.CharField(max_length=100)
    Email_Address = forms.CharField(max_length=100)
    Employee_Code = forms.CharField(max_length=100)
    Is_Active = forms.CharField(max_length=100)
    Created_At = forms.CharField(max_length=100,)
    Updated_At = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Created_By = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Updated_By = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email

class ACUpdate(forms.Form):
    ID = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    First_Name = forms.CharField(max_length=100)
    Last_Name = forms.CharField(max_length=100)
    Cell_Phone = forms.CharField(max_length=100)
    Email_Address = forms.CharField(max_length=100)
    Employee_Code = forms.CharField(max_length=100)
    Is_Active = forms.CharField(max_length=100)
    Created_At = forms.CharField(max_length=100,)
    Updated_At = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Created_By = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Updated_By = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email

class BPUpdate(forms.Form):
    ID = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    First_Name = forms.CharField(max_length=100)
    Last_Name = forms.CharField(max_length=100)
    Cell_Phone = forms.CharField(max_length=100)
    Email_Address = forms.CharField(max_length=100)
    Employee_Code = forms.CharField(max_length=100)
    Is_Active = forms.CharField(max_length=100)
    Created_At = forms.CharField(max_length=100,)
    Updated_At = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Created_By = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Updated_By = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email