from django.utils.timezone import localtime, now
from posts.models import Mentions
from users.models import DeletedUser, User, Activity


def log_deleted_user(user):
    profile = user.profile
    DeletedUser.objects.create(user_hash=user.user_hash,
                               warrant_canary=user.warrant_canary,
                               country=user.country,
                               last_activity_date=user.last_activity_date, date_joined=user.date_joined,
                               bio=profile.bio,
                               disposable=user.disposable,
                               notes=user.notes,
                               alias=user.alias,
                               lost_virginity=user.lost_virginity,
                               first_post=user.first_post,
                               first_login=user.first_login,
                               )

def create_action(sender, receiver, verb, text=None, target=None, count=1, activity_type="default"):
    if not receiver.profile.disable_notifications:
        action = Activity(sender=sender, receiver=receiver, verb=verb, target=target, count=count,
                          activity_type=activity_type)
        action.save()
        return False


def get_mention_tags(text, sender, target):
    words = text.split()
    users_list = []
    for word in words:
        if "@" in word and len(word) > 1:
            users_list.append(word)

    mentioned_users = User.objects.filter(user_hash__in=users_list)
    if mentioned_users:
        for u in mentioned_users:
            if not u.profile.disable_notifications:
                action = Activity(sender=sender, receiver=u, verb="mentioned you", target=target)
                action.save()

    return None
