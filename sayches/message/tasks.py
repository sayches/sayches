from celery import shared_task
from django.utils import timezone

from .models import Message


@shared_task
def delete_messages():
    messages = Message.objects.filter(created_at__lt=timezone.now() - timezone.timedelta(days=1))
    messages.delete()
