from django import forms
from .models import Message


class SendMessageForm(forms.Form):
    text = forms.CharField(label='', widget=forms.Textarea, error_messages={'required': 'введите текст сообщения'})

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text.strip()) == 0:
            raise forms.ValidationError('введите текст сообщения')
        return text
