from celery import shared_task
from django.utils import timezone
from users.models import User, FromSayches
from users.utils import log_deleted_user


@shared_task
def delete_user():
    users = User.objects.all()
    for user in users:
        day = timezone.now() - user.date_joined
        if user.disposable and day.days >= 1:
            try:
                log_deleted_user(user)
                user.delete()
            except:
                pass
