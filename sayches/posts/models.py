from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import SET_NULL
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string
from users.models import BaseModel, FromSayches, BlacklistUser
from utils.upload_path import uuid_media

from config.choices import FLAIR_CHOICES, POST_OPTIONS
from config.settings.base import BASE_URL
from sayches.utils.resize_image import *

User = get_user_model()


class ValidPosts(models.Manager):
    # object manager to return posts that created_at less than 24 hours ago
    def get_queryset(self):
        return super().get_queryset().exclude(
            created_at__lt=timezone.now() - timezone.timedelta(days=1)).order_by('-created_at')


class Post(BaseModel):
    id = models.CharField(primary_key=True, editable=False, max_length=10)
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE, null=True)
    text = models.TextField(blank=False, null=True)
    have_mentions = models.BooleanField(default=False)
    post_followers = models.ManyToManyField(User, related_name="post_followed", blank=True)
    flair = models.CharField(max_length=50, choices=FLAIR_CHOICES, null=True, blank=False)
    post_option = models.CharField(max_length=50, choices=POST_OPTIONS, null=True, blank=False)
    objects = models.Manager()
    valid = ValidPosts()
    pinned_post = models.BooleanField(default=False)
    media = models.FileField(upload_to=uuid_media, null=True, blank=True)
    restrict = models.BooleanField(null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if not self.id:
            found = False
            while not found:
                postid = get_random_string(10,
                                           allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                if not Post.objects.filter(id=postid).exists():
                    self.id = postid
                    found = True
        if self.media:
            try:
                self.media = resize_image(self.media)
            except:
                pass
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("posts:post_detail", args=[self.id])

    def __str__(self):
        return self.id


class PostsTimestamp(BaseModel):
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    post_id = models.CharField(max_length=10, null=True, blank=True)
    post_timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.post_id

    class Meta:
        verbose_name_plural = "Posts Timestamp"


class Comment(BaseModel):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE, null=True)
    text = models.TextField()

    class Meta:
        ordering = ('-created_at',)

    def get_hashtags(self):
        return Hashtag.objects.filter(comments__in=[self])

    def get_user_image(self):
        image_url = self.user.profile.photo_url
        return image_url

    def get_user_name(self):
        if self.user.name == "":
            name = self.user.user_hash
        else:
            name = self.user.name
        return name

    def __str__(self):
        return self.text


class CommentsTimestamp(BaseModel):
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    post_id = models.CharField(max_length=10, null=True, blank=True)
    comment_id = models.CharField(max_length=10, null=True, blank=True)
    comment_timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.post_id

    class Meta:
        verbose_name_plural = "Comments Timestamp"


class Hashtag(BaseModel):
    CLEAN = 0
    PROPAGANDA = 1
    STATUS_TYPE = (
        (CLEAN, 'Clean'),
        (PROPAGANDA, 'Propaganda'),
    )

    posts = models.ManyToManyField(Post, related_name="hashtags")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    comments = models.ManyToManyField(Comment, related_name="chashtags", blank=True)
    # to used just for render the original text
    explicit_name = models.CharField(max_length=255, blank=True)
    # transform the original text to caseless string to use it in qs
    implicit_name = models.CharField(max_length=255, blank=True)
    hashtag_counter = models.PositiveIntegerField(default=1)
    status = models.IntegerField('status', choices=STATUS_TYPE, default=CLEAN)

    class Meta:
        ordering = ('-hashtag_counter',)

    def save(self, *args, **kwargs):
        self.implicit_name = self.explicit_name
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.explicit_name


class Mentions(BaseModel):
    posts = models.ManyToManyField(Post, related_name="mentions")
    comments = models.ManyToManyField(Comment, related_name="mentioncomments", blank=True)
    # to used just for render the original text
    explicit_name = models.CharField(max_length=255, blank=True)
    # transform the original text to caseless string to use it in qs
    implicit_name = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        self.implicit_name = self.explicit_name
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.explicit_name


class Likes(BaseModel):
    post = models.ForeignKey(Post, related_name="post_likes", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, related_name="user_likes", on_delete=models.CASCADE, null=True)
    reaction_name = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return self.post.text

    class Meta:
        verbose_name_plural = "Likes"


class ReportPost(BaseModel):
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

    post_reporter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='post_reporter', null=True,
                                      on_delete=models.SET_NULL)
    post_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='post_user', null=True,
                                  on_delete=models.SET_NULL)
    post_text = models.TextField(null=True, blank=True)
    post_id = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True)
    post_url = models.CharField(max_length=100, null=True, blank=True)
    complaint_date = models.DateTimeField(default=timezone.now)
    removal_date = models.DateTimeField(null=True, blank=True)
    flagging_reason = models.CharField(max_length=500)
    flagger_type = models.CharField(max_length=500, choices=FLAGGER_CHOICE, default="", null=True, blank=True)
    outcome = models.CharField(max_length=500, choices=OUTCOME_TYPE, default="", null=True, blank=True)
    appeal = models.CharField(max_length=100, choices=APPEAL_TYPE, default="", null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        render_body = render_to_string('feed/post/report_post_email.html',
                                       {'username': self.post_user.username, 'reason': self.flagging_reason,
                                        'action': self.outcome, 'post_id': self.post_id,
                                        'post_text': self.post_text, 'post_url': self.post_url,
                                        'domain': BASE_URL})
        if self.outcome == "Account has been suspended":
            FromSayches.from_sayches(title='Important notification about your account', message=render_body,
                                     to=self.post_user)
            BlacklistUser.objects.get_or_create(user=self.post_user, on_post=True, on_message=True)
        elif self.outcome == "No action taken":
            FromSayches.from_sayches(title='Important notification about your account', message=render_body,
                                     to=self.post_user)
        elif self.outcome == "Post was removed":
            FromSayches.from_sayches(title='Important notification about your account', message=render_body,
                                     to=self.post_user)
            try:
                Post.objects.filter(id=self.post_id).delete()
                self.post_id = None
            except Post.DoesNotExist:
                pass
        if self.appeal == "Reversed":
            message = "We have reviewed your request and unfortunately, your appeal will not be granted and your suspension will remain in place. For future reference, we recommend you to familiarise yourself with Sayches's Tos."
            FromSayches.from_sayches(title='Important notification about your account', message=message,
                                     to=self.post_user)

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Reported Posts"


class Statistics(BaseModel):
    modified_at = models.DateTimeField(auto_now=True)
    date = models.DateField(default=timezone.now)
    total_posts = models.IntegerField(default=0)
    total_hashtags = models.IntegerField(default=0)
    total_mentions = models.IntegerField(default=0)
    total_messages = models.IntegerField(default=0)
    total_anonymous = models.IntegerField(default=0)
    total_reports = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Statistics"


class LinkValidation(BaseModel):
    adult_content_website = "1"
    verified_website = "2"
    website_content = [
        (adult_content_website, 'Adult Website'),
        (verified_website, 'Suspicious Website')
    ]
    non_content_website_msg = " "
    adult_content_website_msg = " The terms of service raise very serious concerns.  "
    verified_website_msg = " WARNING: This website has been blacklisted. "
    website_content_msg = [
        (non_content_website_msg, " No default message "),
        (adult_content_website_msg,
         'The terms of service raise very serious concerns '),
        (verified_website_msg, 'WARNING: This website has been blacklisted ')
    ]
    url = models.URLField(null=True, blank=True, unique=True)
    type = models.CharField(
        max_length=2,
        choices=website_content,
        default=verified_website,
    )
    default_message = models.CharField(
        max_length=100,
        choices=website_content_msg,
        default=non_content_website_msg,
        null=True,
    )
    customized_message = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name_plural = "Links Blacklist"


class BlacklistWords(BaseModel):
    word = models.CharField(max_length=140, blank=True, null=True, unique=True)
    is_emoji = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Blacklist Words"

    @classmethod
    def get_words(cls, is_emoji):
        words = cls.objects.filter(is_emoji=is_emoji).values_list('word', flat=True)
        return words
