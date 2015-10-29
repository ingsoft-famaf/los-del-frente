from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms


class UserForm(forms.Form):
    name = forms.CharField(max_length=40)
    password = forms.PasswordInput()