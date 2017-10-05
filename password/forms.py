from custom_user.models import CustomUser
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate


class PasswordRecoveryForm(forms.Form):
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'введите электронный адрес'}))

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            self.user = CustomUser.objects.get(email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError('такая почта не зарегистрирована')
        return email


class PasswordResetForm(forms.Form):
    new_password_1 = forms.CharField(widget=forms.PasswordInput, label='Новый пароль')
    new_password_2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')

    def clean_new_password_2(self):
        new_password_1 = self.cleaned_data.get('new_password_1')
        new_password_2 = self.cleaned_data.get('new_password_2')
        if len(new_password_1) < 5:
            raise forms.ValidationError('Пароль слишком короткий')
        if new_password_1 != new_password_2:
            raise forms.ValidationError('Пароли не совпадают')
        return new_password_1


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'старый пароль'}),
                                   label='',
                                   error_messages={'required': ''}
                                   )
    new_password_1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'новый пароль'}),
                                     label='',
                                     error_messages={'required': ''}
                                     )
    new_password_2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'повторите новый пароль'}),
                                     label='',
                                     error_messages={'required': ''})

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        old_password = self.cleaned_data.get('old_password')
        new_password_1 = self.cleaned_data.get('new_password_1')
        new_password_2 = self.cleaned_data.get('new_password_2')
        auth = authenticate(username=self.user.username, password=old_password)
        if auth is None:
            raise forms.ValidationError('Неправильный пароль')
        if len(new_password_1) < 5:
            raise forms.ValidationError('Новый пароль слишком короткий')
        if new_password_1 != new_password_2:
            raise forms.ValidationError('Новый пароль не совпадает')
        return self.cleaned_data
