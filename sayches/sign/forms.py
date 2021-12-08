import re

from django import forms
from django.contrib.auth.password_validation import validate_password
from django_countries.fields import CountryField
from users.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput, validators=[validate_password])
    agree_terms = forms.BooleanField(required=True)
    disposable = forms.BooleanField(required=False)
    user_hash = forms.CharField(required=True, max_length=15)

    class Meta:
        model = User
        fields = ('user_hash',)

    def clean_user_hash(self):
        username = self.cleaned_data.get('user_hash')
        if username and User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(u'user name must be unique.')
        return username


class UserLoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'custom-input'}))
    remember_me = forms.BooleanField(required=False)

    def clean_login(self):
        regex = "@"
        login = self.cleaned_data.get('login')
        add_at = "@"
        if login:
            if re.search(regex, login) == None:
                return add_at + login
            else:
                return login
        else:
            raise forms.ValidationError("invalid input")


class StepsForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    country = CountryField(blank_label='(Select Location)').formfield(required=False)

    class Meta:
        model = User
        fields = ['name', 'country', 'alias']
