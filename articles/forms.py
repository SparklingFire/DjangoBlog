from django import forms
from .models import Article
from django.core.exceptions import ObjectDoesNotExist


class SearchForm(forms.Form):
    q = forms.CharField(
        label='',
        required=False
    )


class CreateArticleForm(forms.Form):
    title = forms.CharField(help_text='', label='',
                            widget=forms.TextInput(attrs={'placeholder': 'введите заголовок.'}),
                            error_messages={'required': 'придумайте заголовок'}
                            )
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'напишите интересный текст'}),
                           help_text='',
                           label='',
                           error_messages={'required': 'напишите интересный текст'}
                           )
    tag = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'введите список тегов через точку с запятой.'}),
                          error_messages={'required': ''}, required=False
                          )
    image = forms.ImageField(help_text='',
                             label='',
                             error_messages={'required': 'добавьте изображение к новости'}
                             )

    def clean_title(self):
        title = self.cleaned_data.get('title')
        try:
            Article.objects.get(title=title)
            raise forms.ValidationError('статья с таким заголовком уже существует')
        except ObjectDoesNotExist:
            pass
        if len(title) > 50:
            raise forms.ValidationError('максимальная длина заголовка - 50 символов')
        return title

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len([x for x in text if x.isalpha() or x.isdigit()]) < 100:
            raise forms.ValidationError('минимальный размер текста - 100 буквенных/числовых символов')
        return text

    def clean_tag(self):
        tag = self.cleaned_data.get('tag')
