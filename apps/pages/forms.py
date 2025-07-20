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


class MyForm(forms.Form):
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
        label="Select an Option"
    )
