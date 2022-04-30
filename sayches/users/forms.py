import binascii
import hashlib
import re
from django import forms
from django_countries import countries
from django_countries.widgets import CountrySelectWidget
from users.models import User

class EditProfileForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        self.user_name = user.username
        super().__init__(*args, **kwargs)

    img = forms.ImageField(required=False)
    name = forms.CharField(required=False, initial="Unkown", max_length=49)
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    bio = forms.CharField(max_length=150, required=False)
    COUNTRY_CHOICES = tuple(countries)
    widgets = {'country': CountrySelectWidget()}

    def clean_username(self):
        usernames = [user.username for user in User.objects.all() if user.username != self.user_name]
        username = self.cleaned_data['username']
        if username in usernames:
            raise forms.ValidationError("This username already exist")
        return username


from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):
    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])
