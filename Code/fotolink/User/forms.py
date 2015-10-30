from django.contrib.auth.models import User
from django import forms

'''
class UserForm(forms.Form):
    name = forms.CharField(max_length=40)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

'''


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets={'password': forms.PasswordInput()}
