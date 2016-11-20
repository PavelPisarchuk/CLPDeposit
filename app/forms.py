from django import forms
from app.models import User,Bill

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

class MessageForm(forms.Form):
    message = forms.CharField(max_length=300, label='Сообщение')
    header = forms.CharField(max_length=100, label='Заголовок')

class SearchForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')
    passport_id = forms.CharField(max_length=14, label='Идентификационный номер')