import uuid

from ads.models import AdsPricing, AdsOwners, CreateAds, Vouchers
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models.deletion import SET_NULL
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from users.models import BaseModel, User, FromSayches
from utils.upload_path import uuid_ad, uuid_newsroom

PAYMENT_METHOD = (
    ('1', 'Bitcoin'),
)
PAYMENT_STATUS = (
    ('1', 'Paid'),
    ('2', 'Pending'),
    ('3', 'Refunded'),
    ('4', 'Due')
)


class Ads(BaseModel):
    STATUS = (
        ('1', 'Approved'),
        ('2', 'Rejected'),
        ('3', 'Pending'),
        ('4', 'Suspended'),
        ('5', 'Auto-Expired')
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    business_name = models.CharField(max_length=100, null=False, blank=True)
    business_location = CountryField(blank_label='Where do you do business?', null=True, blank=True)
    business_website = models.URLField(max_length=200, null=True, blank=True)
    full_name = models.CharField(max_length=50, null=False, blank=True)
    job_title = models.CharField(max_length=50, null=True, blank=True)
    professional_email = models.EmailField(max_length=70, null=True, blank=True)

    ad_headline = models.CharField(max_length=25, null=True, blank=True)
    ad_link = models.URLField(max_length=200, null=True, blank=True)
    ad_body = models.CharField(max_length=150, null=True, blank=True)
    ad_image = models.ImageField(_('Ad image'), upload_to=uuid_ad, null=True, blank=True)
    ad_location = CountryField(_('Ad Location'), blank_label='Location', null=True, blank=True)
    ad_keywords = models.CharField(max_length=150, null=True, blank=True)
    ad_start_date = models.DateField(null=True, blank=True)
    ad_end_date = models.DateField(null=True, blank=True)
    ad_plan = models.ForeignKey(AdsPricing, on_delete=models.SET_NULL, null=True, blank=True)
    ad_price = models.FloatField(null=True, blank=True)

    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=20, null=True, blank=True, default="1")
    voucher_code = models.ForeignKey(Vouchers, on_delete=SET_NULL, null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    amount_due = models.FloatField(null=True, blank=True)
    btc_amount_due = models.FloatField(null=True, blank=True)
    to_bitcoin_address = models.CharField(max_length=35, null=True, blank=True)
    payment_status = models.CharField(choices=PAYMENT_STATUS, max_length=10, null=True, blank=True, default="2")
    payment_date = models.DateTimeField(null=True, blank=True)

    status = models.CharField(choices=STATUS, default='3', max_length=10)
    notes = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=20, unique=True, null=False, blank=True)
    send_email = models.BooleanField(null=True, blank=True)
    clicks = models.ManyToManyField(User, blank=True, related_name='clicks')
    impressions = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            found = False
            while not found:
                slugify = str(uuid.uuid4())[:20]
                if not Ads.objects.filter(slug=slugify).exists():
                    self.slug = slugify
                    found = True
        if self.status == "1":
            if AdsOwners.objects.filter(
                    user=self.user,
            ).exists():
                ads_owner = AdsOwners.objects.get(user=self.user)
                pass
            else:
                ads_owner = AdsOwners.objects.create(
                    user=self.user,
                    business_name=self.business_name,
                    business_location=self.business_location,
                    business_website=self.business_website,
                    full_name=self.full_name,
                    job_title=self.job_title,
                    professional_email=self.professional_email,
                )
            create_ads, created = CreateAds.objects.get_or_create(
                ad_id=self.slug,
            )
            create_ads.owner_id = ads_owner.id
            create_ads.headline = self.ad_headline
            create_ads.body = self.ad_body
            create_ads.location = self.ad_location
            create_ads.link = self.ad_link
            create_ads.image = self.ad_image
            if self.ad_keywords:
                tag_list = [i for i in self.ad_keywords.split(',')]
                create_ads.keywords.add(*tag_list)
            create_ads.start_date = self.ad_start_date
            create_ads.end_date = self.ad_end_date
            create_ads.save()
        if self.status == "4":
            CreateAds.objects.filter(ad_id=self.slug).delete()
        if self.send_email and not kwargs.get('impressions'):
            if self.status == "1":
                open_body = 'Your ad ({0}) has been approved.'.format(self.slug)
                FromSayches.from_sayches(title='Sayches | Ad #{0}'.format(self.slug), message=open_body, to=self.user)
            if self.status == "2":
                open_body = 'Your ad ({0}) has been rejected. This type of business is not permitted to advertise on Sayches Ads.'.format(
                    self.slug)
                FromSayches.from_sayches(title='Sayches | Ad #{0}'.format(self.slug), message=open_body, to=self.user)
            if self.status == "4":
                open_body = 'Your ad ({0}) has been suspended. Your ad is against the Sayches ToS and has been disabled.'.format(
                    self.slug)
                FromSayches.from_sayches(title='Sayches | Ad #{0}'.format(self.slug), message=open_body, to=self.user)
            if self.status == "5":
                open_body = 'Your ad ({0}) has automatically expired.'.format(self.slug)
                FromSayches.from_sayches(title='Sayches | Ad #{0}'.format(self.slug), message=open_body, to=self.user)
        return super().save(*args, **kwargs)

    @classmethod
    def ad_impressions(cls, create_ad):
        try:
            ad = cls.objects.get(slug=create_ad.ad_id)
            ad.impressions += 1
            ad.save()
        except cls.DoesNotExist:
            pass

    def __str__(self):
        return self.slug

    def display_payment_status(self):
        payment_status = {id: value for id, value in PAYMENT_STATUS}
        return payment_status.get(self.payment_status)

    class Meta:
        verbose_name_plural = "Ads"


class Help(BaseModel):
    STATUS = (
        ('1', 'Pending'),
        ('2', 'Open'),
        ('3', 'Resolved'),
        ('4', 'Closed')
    )
    username = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=150, null=False, blank=False)
    what_i_did = models.TextField(max_length=600, null=True, blank=True)
    what_i_expected_to_happen = models.TextField(max_length=600, null=True, blank=True)
    what_actually_happened = models.TextField(max_length=600, null=True, blank=True)
    anything_else = models.TextField(max_length=600, null=True, blank=True)
    status = models.CharField(choices=STATUS, default='1', max_length=10)
    admin_notes = models.TextField(null=True, blank=True)
    reference_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            get_username = User.objects.get(user_hash=self.username)
        except:
            get_username = None

        if self.status == "3":
            body = 'Your ticket is marked as resolved. If you still need assistance, please reply to this email.'
            if get_username != None:
                FromSayches.from_sayches(title='Sayches | Help #{0}'.format(self.reference_number), message=body,
                                         to=get_username)
            send_mail('Sayches | Help #{0}'.format(self.reference_number), body, settings.DEFAULT_FROM_EMAIL,
                      [self.email])

        elif self.status == "4":
            body = 'Your ticket is marked as closed. If you still need assistance, please reply to this email.'
            if get_username != None:
                FromSayches.from_sayches(title='Sayches | Help #{0}'.format(self.reference_number), message=body,
                                         to=get_username)
            send_mail('Sayches | Help #{0}'.format(self.reference_number), body, settings.DEFAULT_FROM_EMAIL,
                      [self.email])
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class Doc(BaseModel):
    name = models.CharField(max_length=25, null=False, blank=False)
    content = RichTextUploadingField(blank=True, null=True)
    slug = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name


class News(BaseModel):
    TAG = (
        ('', ''),
        ('Article', 'Article'),
        ('Press Release', 'Press Release'),
        ('External', 'External'),
        ('Release Notes', 'Release Notes'),
        ('Guest Post', 'Guest Post'),
    )
    author_image = models.ImageField(upload_to=uuid_newsroom, null=True, blank=True)
    author_name = models.CharField(max_length=100, null=True, blank=True)
    publish_date = models.DateField('date published', null=False, blank=False)
    article_title = models.CharField(max_length=250, null=False, blank=False)
    article_content = RichTextUploadingField(blank=False, null=False)
    article_image = models.ImageField(upload_to=uuid_newsroom, null=True, blank=True)
    tag = models.CharField(max_length=50, choices=TAG, default="", blank=True)
    external = models.URLField(null=True, blank=True)
    slug = models.CharField(max_length=250, null=False, blank=False, unique=True)

    def __str__(self):
        return self.article_title

    class Meta:
        verbose_name_plural = "News"
