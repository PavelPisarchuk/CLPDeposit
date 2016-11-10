from django import forms
from app.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'last_name', 'first_name', 'father_name', 'passport_id']


class AdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
