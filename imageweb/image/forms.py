from django import forms
from django.forms import ModelForm
from .models import Article

class CommentForm(forms.Form):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={'cols': '60', 'rows':'6'} ))


class PostForm(ModelForm):
    class Meta:
        model = Article
        fields = '__all__'