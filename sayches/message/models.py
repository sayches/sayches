from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from users.models import BaseModel


class Chat(BaseModel):
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Members")
    time_of_last_msg = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        name = ''
        for member in self.members.all():
            name += ' ' + member.username
        return name

    def get_absolute_url(self):
        return reverse('chat:messages', kwargs={'chat_id': self.pk})

    def get_members(self):
        return ",".join([str(m) for m in self.members.all()])


class ValidMsgs(models.Manager):
    # object manager to return messages that created_at less than 24 hours ago
    def get_queryset(self):
        return super().get_queryset().exclude(
            created_at__lt=timezone.now() - timezone.timedelta(days=1)).order_by('-created_at')


class Message(BaseModel):
    chat = models.ForeignKey(Chat, related_name="chat_messages", on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_messages", on_delete=models.CASCADE,
                               null=True)
    message = models.TextField()
    sender_message = models.TextField(null=True)
    preference = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    new = models.BooleanField(default=True)
    objects = models.Manager()
    valid = ValidMsgs()

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = "Messages"

    def __str__(self):
        return self.message


class SaychesMessage(BaseModel):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='sayches_messages')
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = "Sayches"

    def __str__(self):
        return self.message
