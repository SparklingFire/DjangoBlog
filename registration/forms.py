import re
from custom_user.models import CustomUser
from django import forms
from django.core.exceptions import ObjectDoesNotExist


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20,
                               label='Имя пользователя',
                               error_messages={'required': 'введите имя пользователя'}
                               )
    password_1 = forms.CharField(widget=forms.PasswordInput,
                                 label='Пароль',
                                 error_messages={'required': 'введите пароль'}
                                 )
    password_2 = forms.CharField(widget=forms.PasswordInput,
                                 label='Подтверждение пароля',
                                 error_messages={'required': 'подтвердите пароль'}
                                 )
    email = forms.EmailField(label='Электронный адрес',
                             error_messages={'required': 'введите электронный адрес'}
                             )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username is None:
            raise forms.ValidationError('Введите имя пользователя')
        try:
            CustomUser.objects.get(username_slug=username.lower())
            raise forms.ValidationError('Данное имя пользователя уже занято')
        except ObjectDoesNotExist:
            pass
        if len(username) < 4:
            raise forms.ValidationError('Никнейм слишком короткий')
        return username

    def clean_password_2(self):
        password_1 = self.cleaned_data.get('password_1')
        password_2 = self.cleaned_data.get('password_2')
        if len(password_1) < 5:
            raise forms.ValidationError('Пароль слишком короткий')
        if password_1 != password_2:
            raise forms.ValidationError('Пароли не совпадают')
        pattern = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$"
        if not re.findall(pattern, password_1):
            raise forms.ValidationError('Пароль слишком простой')
        return password_2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email is None:
            raise forms.ValidationError('Введите электронный адрес')
        try:
            CustomUser.objects.get(email=email)
            raise forms.ValidationError('Данный электронный адрес уже зарегистрирован')
        except ObjectDoesNotExist:
            pass
        return email


class TokenResendForm(forms.Form):
    email_or_username = forms.CharField(label='Имя пользователя или электронный адрес')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_email_or_username(self):
        email_or_username = self.cleaned_data.get('email_or_username')
        try:
            self.user = CustomUser.objects.get(username__iexact=email_or_username)
        except ObjectDoesNotExist:
            pass
            try:
                self.user = CustomUser.objects.get(email__iexact=email_or_username)
            except ObjectDoesNotExist:
                pass
        if not self.user:
            raise forms.ValidationError('user or email is not registered')
        return email_or_username
