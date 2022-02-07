from django.utils.timezone import localtime, now
from posts.models import Mentions
from users.models import DeletedUser, User, Activity, UserStatistics


def log_deleted_user(user):
    profile = user.profile

    DeletedUser.objects.create(user_hash=user.user_hash,
                               warrant_canary=user.warrant_canary,
                               country=user.country,
                               profile_update_time=user.profile_update_time,
                               auto_account_delete_time=user.auto_account_delete_time,
                               last_activity_date=user.last_activity_date, date_joined=user.date_joined,
                               bio=profile.bio, website=profile.website,
                               pgp_fingerprint=profile.pgp_fingerprint,
                               btc_address=profile.btc_address,
                               disposable=user.disposable,
                               notes=user.notes,
                               alias=user.alias,
                               lost_virginity=user.lost_virginity,
                               first_post=user.first_post,
                               first_login=user.first_login,
                               )
    body = f'Your account has been destroyed.'

    total_deleted_user = DeletedUser.objects.count()
    user_stataticstic(deleted_user=total_deleted_user)


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


def user_stataticstic(total_users='', actiavte_user_count='', inactiavte_user_count="", verifyed_user="",
                      deleted_user=""):
    try:
        creation_date = localtime(now()).date()
        check_user_stat = UserStatistics.objects.filter(date=creation_date).first()
        if check_user_stat:
            if verifyed_user:
                check_user_stat.total_verified_users = verifyed_user
            elif deleted_user:
                check_user_stat.total_deleted_user = deleted_user
            else:
                check_user_stat.total_active_users = actiavte_user_count
                check_user_stat.total_users = total_users
                check_user_stat.total_inactive_users = inactiavte_user_count
            check_user_stat.save()
        else:
            create_statatic = UserStatistics()
            if verifyed_user:
                create_statatic.total_verified_users = verifyed_user
            elif deleted_user:
                create_statatic.total_deleted_user = deleted_user
            else:
                create_statatic.total_active_users = actiavte_user_count
                create_statatic.total_users = total_users
                create_statatic.total_inactive_users = inactiavte_user_count
            create_statatic.save()
        return True
    except Exception:
        return False
