from django import forms
from .models import Article, Blog, Content


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'title', 'content', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-file'}),
        }


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['name', 'title', 'content', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-file'}),
        }


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['name', 'title', 'content', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-file'}),
        }