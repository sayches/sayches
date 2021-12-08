from django import forms

from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']


class MessageFromProfile(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
