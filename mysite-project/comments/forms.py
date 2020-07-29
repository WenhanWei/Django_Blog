from django import forms
from .models import Comment
# from django_summernote.fields import SummernoteTextFormField


class CommentForm(forms.ModelForm):
    # text = SummernoteTextFormField()
    class Meta:
        model = Comment
        fields = ['name', 'email', 'text']
