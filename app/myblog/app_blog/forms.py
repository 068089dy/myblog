from django import forms
from .models import Article
from .widget import MyTextInput


class ArticleForm(forms.ModelForm):
    # 为了防止admin表单未保存就干部页面，所以使用MyTextInput
    title = forms.CharField(initial=0, widget=MyTextInput())

    class Meta:
        forms.model = Article
