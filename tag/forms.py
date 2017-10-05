from django import forms
from django.forms import (modelformset_factory, BaseModelFormSet)
from .models import Tag
import re


class TagForm(forms.Form):
    tag_list = forms.CharField(help_text='', label='', widget=forms.TextInput(attrs={'placeholder': 'введите список тегов через точку с запятой.'}))

    def clean(self):
        tag_list = self.cleaned_data.get('tag_list')
        if tag_list:
            tag_list = tag_list.split(';')
        return self.cleaned_data
