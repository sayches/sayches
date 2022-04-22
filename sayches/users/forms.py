import binascii
import hashlib
import re
from django import forms
from django_countries import countries
from django_countries.widgets import CountrySelectWidget
from users.models import User

from .models import UserVerification


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
    website = forms.URLField(required=False)
    COUNTRY_CHOICES = tuple(countries)
    widgets = {'country': CountrySelectWidget()}

    def clean_username(self):
        usernames = [user.username for user in User.objects.all() if user.username != self.user_name]
        username = self.cleaned_data['username']
        if username in usernames:
            raise forms.ValidationError("This username already exist")
        return username

    def clean_website(self):
        website = self.cleaned_data['website']
        if website:
            split_url = website.split(".")
            v3_address = split_url[0].split("//")
            string_check = re.compile('[@_!#$%^&*()<>?/|}{~:]')
            if len(v3_address) != 2:
                raise ValidationError("Invalid Onion Address")
            elif split_url[-1] != "onion" or string_check.search(split_url[-1]):
                raise ValidationError("Invalid Onion Address")
            elif len(v3_address[1]) != 56 or string_check.search(v3_address[1]) or not v3_address[1].endswith('d'):
                raise ValidationError("Invalid Onion Address")
            elif v3_address[0] not in ["https:", "http:"]:
                raise ValidationError("Invalid Onion Address")
        return website


class UserVerificationForm(forms.ModelForm):
    class Meta:
        model = UserVerification
        fields = ("user", "url", "verification", "verified")

    def __init__(self, *args, **kwargs):
        super(UserVerificationForm, self).__init__(*args, **kwargs)
        if kwargs.get('initial'):
            user = kwargs.get('initial').get('user')
            user_verification = UserVerification.objects.filter(user=user)
            if user_verification:
                for field, value in self.fields.items():
                    if field == 'url':
                        value.widget.attrs['disabled'] = True
                    value.widget.attrs["readonly"] = "readonly"
                    value.widget.attrs["value"] = getattr(user_verification[0], field)


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
