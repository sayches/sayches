import datetime

from django.conf import settings
from django.db import models
from django.db.models.deletion import SET_NULL
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from taggit.managers import TaggableManager
from users.models import BaseModel, User
from utils.upload_path import uuid_ad


class AdsOwners(BaseModel):
    user = models.OneToOneField(User, on_delete=SET_NULL, null=True, blank=True)
    business_name = models.CharField(max_length=100, null=False, blank=True)
    business_location = CountryField(null=True, blank=True)
    business_website = models.URLField(max_length=200, null=True, blank=True)
    full_name = models.CharField(max_length=50, null=False, blank=True)
    job_title = models.CharField(max_length=50, null=True, blank=True)
    professional_email = models.EmailField(max_length=70, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.business_name

    class Meta:
        verbose_name_plural = "Ads Owners"


class CreateAds(BaseModel):
    owner = models.ForeignKey(AdsOwners, on_delete=models.SET_NULL, null=True, blank=True)
    headline = models.CharField(max_length=25, null=True, blank=True)
    body = models.CharField(max_length=150, null=True, blank=True)
    location = CountryField(_('Ad Location'), null=True, blank=True)
    target_all_users = models.BooleanField(null=True, blank=True)
    target_user_list = models.ManyToManyField(User, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)
    image = models.ImageField(_('Ad image'), upload_to=uuid_ad,
                              default="assets/images/blanks/373x256.png", blank=True, null=True)
    keywords = TaggableManager()
    start_date = models.DateTimeField(_('Start Date'), null=True, blank=True)
    end_date = models.DateTimeField(_('End Date'), null=True, blank=True)
    ad_id = models.SlugField(max_length=20, unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Active Ads"


class AdminNotifications(BaseModel):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='notifications_user')
    nf_url = models.URLField(max_length=200)
    nf_description = models.CharField(max_length=60)
    nf_title = models.CharField(max_length=30)
    read = models.BooleanField(default=False)
    count = models.PositiveIntegerField(default=1)
    notification_followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="notify_followed",
                                                    blank=True)

    def __str__(self):
        return self.nf_title

    class Meta:
        verbose_name_plural = "Ads Notifications"


class AdsPricing(BaseModel):
    title = models.CharField(max_length=25, null=True, blank=True)
    type = models.CharField(max_length=25, null=True, blank=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(upload_to=uuid_ad, blank=True, null=True)
    price = models.FloatField(null=True, blank=True)
    per = models.CharField(max_length=50, blank=True,
                           help_text="True means ready for sale. False means consumer have to contact the admin.")
    pick = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Ads Pricing"


class Vouchers(BaseModel):
    to = models.ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
    voucher_code = models.CharField(max_length=5, null=True, blank=False, unique=True)
    plan = models.ForeignKey(AdsPricing, null=True, blank=True, on_delete=SET_NULL)
    discount_percentage = models.IntegerField(null=True, blank=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    expired = models.BooleanField(null=True, blank=True)

    @property
    def is_expired(self):
        return not (self.start_date <= datetime.date.today() and self.end_date >= datetime.date.today())

    def is_valid(self, user, plan):
        valid = True
        if self.to and self.to != user:
            valid = False
        if self.plan and self.plan != plan:
            valid = False
        return valid

    class Meta:
        verbose_name_plural = "Vouchers"

    def __str__(self):
        return self.voucher_code
