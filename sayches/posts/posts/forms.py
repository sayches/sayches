from django import forms


class SearchPost(forms.Form):
    query = forms.CharField()
