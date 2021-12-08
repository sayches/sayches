from django import forms
from django_countries.fields import CountryField
from posts.models import Post
from subsections.models import Ads, AdsOwners, Help

from config.choices import FLAIR_CHOICES


class flair_form_public(forms.ModelForm):

    def __init__(self, *args, **kargs):
        super(flair_form_public, self).__init__(*args, **kargs)

    flair = forms.ChoiceField(choices=FLAIR_CHOICES)

    class Meta:
        model = Post
        fields = '__all__'


class AdsStepOneForm(forms.ModelForm):
    business_name = forms.CharField(max_length=100, required=True, label='What is your business name?')
    full_name = forms.CharField(max_length=50, required=True, label='What is your full name?')
    job_title = forms.CharField(max_length=50, required=True, label='What is your job title?')
    professional_email = forms.EmailField(label='What is your professional email address?', required=True)
    business_website = forms.URLField(label='What is your business official website?', required=True)
    business_location = CountryField(blank_label='Where do you do business?').formfield(required=False)

    class Meta:
        model = Ads
        fields = [
            'business_name',
            'full_name',
            'job_title',
            'professional_email',
            'business_website',
            'business_location',
        ]

    def __init__(self, *args, **kwargs):
        super(AdsStepOneForm, self).__init__(*args, **kwargs)
        user = kwargs.get('initial').get('user')
        ads_owner = AdsOwners.objects.filter(user=user)
        self.fields["business_location"].widget.attrs["required"] = True
        if ads_owner:
            for field, value in self.fields.items():
                if field == 'business_location':
                    value.widget.attrs['disabled'] = True
                    self.fields['business_location'].initial = ads_owner[0].business_location
                value.widget.attrs["readonly"] = "readonly"
                value.widget.attrs["value"] = getattr(ads_owner[0], field)

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
    email = forms.EmailField(max_length=100, required=True, label='Your email address')
    what_i_did = forms.CharField(max_length=50, required=False, label='This is what I DID')
    what_i_expected_to_happen = forms.CharField(label='This is what I EXPECTED to happen', required=False)
    what_actually_happened = forms.CharField(label='This is what ACTUALLY happened', required=True)
    anything_else = forms.CharField(label="Anything else you’d like to tell us", widget=forms.Textarea(),
                                    required=False)

    class Meta:
        model = Help
        fields = [
            'username',
            'email',
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
                if user.is_authenticated:
                    self.fields["username"].widget.attrs["value"] = user.username
                    self.fields["username"].widget.attrs["readonly"] = 'readonly'
            message = initial.get("message")
            if message:
                for field, value in self.fields.items():
                    value.widget.attrs["readonly"] = "readonly"
