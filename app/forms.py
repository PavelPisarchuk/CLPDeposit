from django import forms
from app.models import User

userfields = ["username", "password"]
adminfields = ["email"]
clientfields = ["last_name", "first_name", "father_name",]# "passport_id", "address", "birthday", "phone"]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = userfields + clientfields


class AdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = userfields + adminfields
