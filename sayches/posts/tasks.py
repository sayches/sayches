from celery import shared_task
from django.utils import timezone
from users.models import User

from .models import Post


@shared_task
def delete_post():
    Post.objects.filter(created_at__lt=timezone.now() - timezone.timedelta(days=1),
                        user__profile_update_time=User.TWENTY_FOUR_HOURS).exclude(pinned_post=True).delete()
    Post.objects.filter(created_at__lt=timezone.now() - timezone.timedelta(days=2),
                        user__profile_update_time=User.FORTY_EIGHT_HOURS).exclude(pinned_post=True).delete()
    Post.objects.filter(created_at__lt=timezone.now() - timezone.timedelta(days=3),
                        user__profile_update_time=User.SEVENTY_TWO_HOURS).exclude(pinned_post=True).delete()
    Post.objects.filter(created_at__lt=timezone.now() - timezone.timedelta(days=0),
                        user__profile_update_time=User.ZERO)
