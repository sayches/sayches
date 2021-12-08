import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from message.models import Message


@receiver(post_save, sender=Message)
def update_time_of_last_msg(sender, instance, created, **kwargs):
    if created:
        chat = instance.chat
        chat.time_of_last_msg = datetime.datetime.now()
        chat.save()
