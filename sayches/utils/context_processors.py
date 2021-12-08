from ads.models import CreateAds, AdminNotifications
from django.conf import settings
from message.models import Message, SaychesMessage
from sudo.models import CloseWebsite, VersionNumber
from users.models import Activity
from users.models import BlacklistUser


def settings_context(request):
    ad = CreateAds.objects.last()
    site_customization = VersionNumber.objects.filter(default=True).last()
    sayches_settings = CloseWebsite.objects.last()
    close_site = False
    closing_text = ''

    if sayches_settings:
        sayches_settings = sayches_settings
        close_site = sayches_settings.close_site
        closing_text = sayches_settings.closing_text

    version_no = ''
    show_beta_icon = False
    disable_messages = False
    if site_customization:
        version_no = site_customization.version_no
        show_beta_icon = site_customization.show_beta_icon

    if request.user.is_active:
        admin_count = AdminNotifications.objects.exclude(
            notification_followers__in=[request.user]).filter(user=request.user).count()
        admin_msg_count = SaychesMessage.objects.filter(is_read=False, user=request.user).count()
        all_user_chats = request.user.chat_set.all()
        user_unread_chats_count = Message.objects.filter(is_read=False, chat__in=all_user_chats).exclude(
            author=request.user).order_by('chat').distinct('chat').count()
        admin_nfs = AdminNotifications.objects.filter(user=request.user).order_by('-created_at')[:5]
        notification_follower = AdminNotifications.objects.filter(
            notification_followers__in=[request.user]).filter(user=request.user).order_by('?')
        if notification_follower:
            notification_follower = notification_follower.first()
        not_notification_follower = AdminNotifications.objects.exclude(
            notification_followers__in=[request.user]).filter(user=request.user)
        nfs = Activity.objects.filter(receiver_id=request.user).order_by('-created_at')[:5]
        nfs_no = Activity.objects.filter(read=False).filter(receiver_id=request.user)
        nfs_after_ajax = Activity.objects.filter(receiver_id=request.user).order_by('-created_at')[:5]
        if admin_nfs:
            nfs_count = nfs_no.count() + admin_count
        else:
            nfs_count = nfs_no.count()

        check_message_block = BlacklistUser.objects.filter(user=request.user, on_message=True).first()
        is_message_block = False
        if check_message_block:
            is_message_block = True

        if admin_msg_count:
            user_unread_chats_count += 1
        if not request.user.is_superuser:
            disable_messages = request.user.profile.disable_messages

        return {"settings": settings, "ad": ad, "admin_nfs": admin_nfs, "nfs": nfs,
                "nfs_count": nfs_count, "nfs_after_ajax": nfs_after_ajax,
                "notification_follower": notification_follower,
                'not_notification_follower': not_notification_follower,
                "user_unread_chats_count": user_unread_chats_count,
                "version_no": version_no,
                "show_beta_icon": show_beta_icon,
                "is_message_block": is_message_block,
                "closing_text": closing_text,
                "close_site": close_site,
                "disable_messages": disable_messages
                }
    else:
        return {"settings": settings, "version_no": version_no, "show_beta_icon": show_beta_icon,
                "closing_text": closing_text,
                "close_site": close_site, "disable_messages": disable_messages
                }
