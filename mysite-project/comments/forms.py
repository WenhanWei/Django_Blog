from django import forms
from .models import Comment
from django_summernote.widgets import SummernoteWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'text']
        widgets = {
            'text': SummernoteWidget(),
        }
