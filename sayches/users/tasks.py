from celery import shared_task
from django.utils import timezone
from users.models import User, FromSayches
from users.utils import log_deleted_user


@shared_task
def delete_user():
    users = User.objects.all()
    for user in users:
        day = timezone.now() - user.date_joined
        if 1 < user.compare_last_activity_with_auto_delete_time < 4:
            body = f'Your account will be destroyed after {user.compare_last_activity_with_auto_delete_time} days from now.' \
                   f' Please take further action if you still need it.'
            FromSayches.from_sayches(title='Sayches | Reminder Before Destroying', message=body, to=user)
        elif user.compare_last_activity_with_auto_delete_time < 0:
            try:
                log_deleted_user(user)
                user.delete()
            except:
                pass
        elif user.disposable and day.days >= 1:
            try:
                log_deleted_user(user)
                user.delete()
            except:
                pass
