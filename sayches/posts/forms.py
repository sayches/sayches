from django import forms

from .models import Comment


class CommentCreation(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class SearchPost(forms.Form):
    query = forms.CharField()
