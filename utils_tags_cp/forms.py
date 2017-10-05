from django import forms
from .models import Image


class ChangeAvatar(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)
        labels = {'image': ''}
