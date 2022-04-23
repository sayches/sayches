from email.policy import default
from django import forms
from django_countries.fields import CountryField
from posts.models import Post
from subsections.models import Ads, Help

from config.choices import FLAIR_CHOICES


class flair_form_public(forms.ModelForm):

    def __init__(self, *args, **kargs):
        super(flair_form_public, self).__init__(*args, **kargs)

    flair = forms.ChoiceField(choices=FLAIR_CHOICES)

    class Meta:
        model = Post
        fields = '__all__'


class AdsStepOneForm(forms.ModelForm):
    i_agree = forms.BooleanField(initial=True)

    class Meta:
        model = Ads
        fields = [
            'i_agree',
        ]

    def clean_business_website(self, *args, **kwargs):
        from urllib.parse import urlparse
        website = self.cleaned_data.get("business_website")
        email = self.cleaned_data.get("professional_email")
        if urlparse(website).netloc != email.split("@")[1]:
            raise forms.ValidationError('Email domain must be the website domain.')
        return website


class AdsStepTwoForm(forms.ModelForm):
    ad_headline = forms.CharField(max_length=25, required=True, label='Headline', )
    ad_body = forms.CharField(max_length=150, required=True, label='Body', )
    ad_link = forms.CharField(max_length=150, required=False, label='Link', )
    ad_start_date = forms.DateField(required=True, label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}), )
    ad_end_date = forms.DateField(required=True, label='End Date', widget=forms.DateInput(attrs={'type': 'date'}), )
    ad_location = CountryField(blank_label='Location').formfield(required=True)

    class Meta:
        model = Ads
        fields = [
            'ad_headline',
            'ad_body',
            'ad_link',
            'ad_image',
            'ad_location',
            'ad_keywords',
            'ad_start_date',
            'ad_end_date',
        ]


class AdsStepFourVoucherForm(forms.Form):
    voucher = forms.CharField(max_length=5, required=False, label='Voucher Code', )

    def __init__(self, *args, **kwargs):
        super(AdsStepFourVoucherForm, self).__init__(*args, **kwargs)
        initial = kwargs.get('initial')
        if initial:
            disable = initial.get('disable')
            if disable:
                self.fields["voucher"].widget.attrs["value"] = kwargs.get('initial').get('voucher')
                self.fields["voucher"].widget.attrs["readonly"] = 'readonly'


class HelpForm(forms.ModelForm):
    username = forms.CharField(max_length=50, required=False, label='Your username')
    what_i_did = forms.CharField(max_length=50, required=False, label='This is what I DID')
    what_i_expected_to_happen = forms.CharField(label='This is what I EXPECTED to happen', required=False)
    what_actually_happened = forms.CharField(label='This is what ACTUALLY happened', required=True)
    anything_else = forms.CharField(label="Anything else you’d like to tell us", widget=forms.Textarea(),
                                    required=False)

    class Meta:
        model = Help
        fields = [
            'username',
            'what_i_did',
            'what_i_expected_to_happen',
            'what_actually_happened',
            'anything_else',
            'reference_number'
        ]

    def __init__(self, *args, **kwargs):
        super(HelpForm, self).__init__(*args, **kwargs)
        initial = kwargs.get('initial')
        if initial:
            user = initial.get('user')
            if user:
                self.fields["username"].widget.attrs["value"] = user.username
                self.fields["username"].widget.attrs["readonly"] = 'readonly'
            message = initial.get("message")
            if message:
                for field, value in self.fields.items():
                    value.widget.attrs["readonly"] = "readonly"
