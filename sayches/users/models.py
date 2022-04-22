from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField

from sayches.utils.resize_image import *
from sayches.utils.upload_path import uuid_profilepicture


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class User(AbstractUser):
    ONE_DAY = 0
    ONE_MONTH = 1
    SIX_MONTH = 6
    TWELVE_MONTH = 12

    AUTO_ACCOUNT_DELETE_CHOICES = (
        (ONE_DAY, 'DISPOSABLE'),
        (ONE_MONTH, '1'),
        (SIX_MONTH, '6'),
        (TWELVE_MONTH, '12'),
    )

    TWENTY_FOUR_HOURS = 24
    FORTY_EIGHT_HOURS = 48
    SEVENTY_TWO_HOURS = 72
    ZERO = 0

    UNKNOWN_USER = 'Unknown'
    ANONYMOUS_USER = 'Anonymous'
    UNIDENTIFIED_USER = 'Unidentified'
    NAMELESS = 'Nameless'
    ALIASES = (
        (UNKNOWN_USER, 'Unknown'),
        (UNIDENTIFIED_USER, 'Unidentified'),
        (ANONYMOUS_USER, 'Anonymous'),
        (NAMELESS, 'Nameless'),
    )

    objects = CustomUserManager()
    name = models.CharField(_("Name of User"), blank=True, max_length=49)
    user_hash = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=False,
        validators=[
            RegexValidator(
                regex='^@[\u0621-\u064Aa-zA-Z\d\-_\s]+$',
                message='Username must be Alphanumeric only',
                code='invalid_username'
            ),
        ]
    )
    country = CountryField(null=True, blank=True, blank_label='(Select Location)')
    first_login = models.BooleanField(default=False)
    first_post = models.BooleanField(default=False)
    lost_virginity = models.BooleanField(default=False)
    warrant_canary = models.BooleanField(default=True)
    alias = models.CharField(max_length=20, default=ANONYMOUS_USER, choices=ALIASES)
    notes = models.TextField(null=True, blank=True)
    auto_account_delete_time = models.IntegerField(choices=AUTO_ACCOUNT_DELETE_CHOICES, default=TWELVE_MONTH)
    last_activity_date = models.DateTimeField(default=timezone.now)
    send_email = models.BooleanField(null=True, blank=True)
    disposable = models.BooleanField(null=True, blank=True, default=False)

    def save(self, *args, **kwargs):

        if self.send_email:
            if self.warrant_canary == False:
                get_username = User.objects.get(user_hash=self.user_hash)
                open_body = "The Warrant Canary icon has been removed from your profile. Removal of the Warrant Canary serves as notification to the User that their data has been requested by a competent law enforcement authority."
                FromSayches.from_sayches(title='Important notification about your account', message=open_body,
                                         to=get_username)
                self.send_email = False
        return super().save(*args, **kwargs)

    @property
    def compare_last_activity_with_auto_delete_time(self):
        last_active = timezone.now() - self.last_activity_date
        return self.auto_account_delete_time * 30 - last_active.days

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def get_name_or_username(self):
        if self.name:
            return self.name
        elif self.alias:
            return self.alias
        return self.username

    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)

    def user_profile_age(self):
        datetime_diff = datetime.now() - self.date_joined.replace(tzinfo=None)
        self.profile_age = str(datetime_diff.days)
        return self.profile_age

    def display_user_name(self):
        if self.name:
            name = self.name
        else:
            name = self.alias
        return name


class UserRSA(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    public_pem = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "User RSA"


class LoggedInUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='logged_in_user', on_delete=CASCADE, null=True)
    session_key = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Logged In User"

    def __str__(self):
        return self.user.username


class FromSayches(BaseModel):
    to = models.ForeignKey(User, on_delete=SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "From Sayches"

    @classmethod
    def from_sayches(cls, to, title, message):
        FromSayches.objects.create(to=to, title=title, message=message)
        notification = 'You got new message from Sayches. Go to Settings > From Sayches'
        Activity.objects.create(receiver=to, verb=notification)


class Bell(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="ring_user", on_delete=models.CASCADE)
    targeted_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="ring_from", on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.user.username + 'pinged' + self.targeted_user.username


class PingPong(BaseModel):
    pinger_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="pinger", on_delete=models.CASCADE)
    pinged_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="pinged", on_delete=models.CASCADE)
    pong = models.BooleanField(default=False)
    pong_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.pinger_user.username + 'pinged' + self.pinged_user.username


class Profile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=uuid_profilepicture, null=True, blank=True)
    bio = models.CharField(max_length=150, blank=True)
    pgp_fingerprint = models.CharField(max_length=49, null=True, blank=True)
    btc_address = models.CharField(max_length=42, null=True, blank=True)
    website = models.URLField(null=True, blank=True, max_length=70)
    disable_notifications = models.BooleanField(default=False, null=True)
    disable_messages = models.BooleanField(default=False, null=True)
    disable_ping = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.user.username

    @property
    def photo_url(self):
        suspended_user = BlacklistUser.objects.filter(user=self.user)

        if suspended_user:
            return static('assets/images/avatars/suspended.png')
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        if self.user.user_profile_age() == '0':
            if self.user.disposable:
                return static('assets/images/avatars/incognitoAvatar_2_360x360.png')
            return static('assets/images/avatars/babyAvatar_360x360.png')

        return static('assets/images/avatars/incognitoAvatar_360x360.png')

    @property
    def image_url(self):
        return self.photo_url

    def save(self, *args, **kwargs):
        if self.photo:
            self.photo = resize_image(self.photo)
        return super().save(*args, **kwargs)


class UserVerification(BaseModel):
    CATEGORIE_TYPEE = [("New/Media", "New/Media"), ("Sports", "Sports"), ("Government/Politics", "Government/Politics"),
                       ("Music", "Music"), ("Fashion", "Fashion"), ("Blogger/Influencer", "Blogger/Influencer"),
                       ("Business/Brand/Organisation", "Business/Brand/Organisation"), ("Other", "Other")]
    VERIFICATION_STATUS = [("Fraudulent", "Fraudulent"), ("Bot", "Bot"), ("Official", "Official"),
                           ("Verified", "Verified")]
    APPLICATION_STATUS = [("Approved", "Approved"), ("Rejected", "Rejected"), ("Removed", "Removed")]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    url = models.URLField(null=True, blank=False)
    verification = models.CharField(choices=VERIFICATION_STATUS, max_length=100, blank=True, null=True)
    verified = models.BooleanField(default=False)
    application_status = models.CharField(choices=APPLICATION_STATUS, max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.application_status == "Approved":
            body = "Your Sayches account was successfully verified."
            FromSayches.from_sayches(title='Your account is verified', message=body, to=self.user)
        elif self.application_status == "Rejected":
            body = "We are unable to verify the URL you provided. As a result, your account will not receive a verification badge."
            FromSayches.from_sayches(title='Your account does not meet the verification criteria', message=body,
                                     to=self.user)

        return super().save(*args, **kwargs)

    def __str__(self):
        try:
            return self.user.username
        except:
            return self.url

    @property
    def image_url(self):
        return self.photo_url

    class Meta:
        verbose_name_plural = "Verifications"


class ReportUser(BaseModel):
    FLAGGER_CHOICE = (
        ('', ''),
        ('Automated flagging', 'Automated flagging'),
        ('Government agency', 'Government agency'),
        ('Individual trusted flagger', 'Individual trusted flagger'),
        ('NGO', 'NGO'),
        ('User', 'User'),
    )
    APPEAL_TYPE = (
        ('', ''),
        ('Reversed', 'Reversed'),
        ('Upheld', 'Upheld')
    )
    OUTCOME_TYPE = (
        ('', ''),
        ('Account has been suspended', 'Account has been suspended'),
        ('No action taken', 'No action taken'),
        ('Post was removed', 'Post was removed'),
    )

    user_reporter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_reporter', null=True,
                                      on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', null=True, on_delete=models.SET_NULL)
    complaint_date = models.DateTimeField(default=timezone.now)
    removal_date = models.DateTimeField(null=True, blank=True)
    flagging_reason = models.CharField(max_length=500)
    flagger_type = models.CharField(max_length=500, choices=FLAGGER_CHOICE, default="", null=True, blank=True)
    outcome = models.CharField(max_length=500, choices=OUTCOME_TYPE, default="", null=True, blank=True)
    appeal = models.CharField(max_length=100, choices=APPEAL_TYPE, default="", null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        render_body = render_to_string('profile/report_user_email.html',
                                       {'username': self.user.username, 'reason': self.flagging_reason,
                                        'action': self.outcome})
        if self.outcome == "Account has been suspended":
            FromSayches.from_sayches(title='Important notification about your account', message=render_body,
                                     to=self.user)
            BlacklistUser.objects.get_or_create(user=self.user, on_post=True, on_message=True, on_login=True)
        elif self.outcome == "No action taken":
            FromSayches.from_sayches(title='Important notification about your account', message=render_body,
                                     to=self.user)
        elif self.outcome == "Post was removed":
            FromSayches.from_sayches(title='Important notification about your account', message=render_body,
                                     to=self.user)
        if self.appeal == "Reversed":
            message = "We have reviewed your request and unfortunately, your appeal will not be granted and your suspension will remain in place. For future reference, we recommend you to familiarise yourself with Sayches's Tos."
            FromSayches.from_sayches(title='Important notification about your account', message=message, to=self.user)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Reported Users"

class DeletedUser(BaseModel):
    user_hash = models.CharField(max_length=15, null=True, blank=False)
    country = CountryField(null=True, blank=False, blank_label='(Select Location)')
    warrant_canary = models.BooleanField(default=True)
    auto_account_delete_time = models.IntegerField(choices=User.AUTO_ACCOUNT_DELETE_CHOICES, default=User.TWELVE_MONTH)
    last_activity_date = models.DateTimeField(default=timezone.now)
    date_joined = models.DateTimeField(default=timezone.now)
    deleted_date_time = models.DateTimeField(auto_now_add=True, null=True)
    bio = models.CharField(max_length=150, blank=True, null=True)
    pgp_fingerprint = models.CharField(max_length=49, null=True, blank=True)
    btc_address = models.CharField(max_length=45, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    disposable = models.BooleanField(null=True)
    notes = models.TextField(null=True)
    alias = models.CharField(max_length=20, null=True)
    lost_virginity = models.BooleanField(null=True)
    first_post = models.BooleanField(null=True)
    first_login = models.BooleanField(null=True)

    class Meta:
        verbose_name_plural = "Deleted Users"

class BlacklistUser(BaseModel):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    on_post = models.BooleanField(default=False)
    on_login = models.BooleanField(default=False)
    on_message = models.BooleanField(default=False)
    suspended_message = models.TextField(null=True, blank=True,
                                         default="Sayches suspends accounts which violate the Sayches Rules")

    class Meta:
        verbose_name_plural = "Suspended Users"


class Activity(BaseModel):
    TYPE_CHOICES = [
        ("bell", "Bell"),
        ("default", "default"),
        ("ping", "Ping")
    ]

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sended_nfs', on_delete=models.CASCADE, null=True,
                               blank=True)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_nfs', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_obj',
                                  on_delete=models.CASCADE)
    target_id = models.CharField(null=True, blank=True, max_length=20)
    target = GenericForeignKey('target_ct', 'target_id')
    activity_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="default")
    read = models.BooleanField(default=False)
    count = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = "Activities"
