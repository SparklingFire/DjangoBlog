from custom_user.models import CustomUser
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from . import models
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя',
                               error_messages={'required': ''},
                               widget=forms.TextInput(attrs={'placeholder': 'введите имя пользователя'})
                               )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'введите пароль'}),
                               label='Пароль',
                               error_messages={'required': ''}
                               )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is None:
            raise forms.ValidationError('Введите имя пользователя')
        if password is None:
            raise forms.ValidationError('Введите пароль')
        try:
            CustomUser.objects.get(username=username)
        except ObjectDoesNotExist:
            raise forms.ValidationError("Пользователь с таким именем не существует или неактивен")
        pos_user = authenticate(username=username, password=password)
        if pos_user is None:
            raise forms.ValidationError('Неправильное имя пользователя или пароль')
        return self.cleaned_data
