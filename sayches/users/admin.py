from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django_celery_beat.models import (PeriodicTask, CrontabSchedule, ClockedSchedule, IntervalSchedule, SolarSchedule)
from users.forms import UserChangeForm, UserCreationForm
from users.models import LoggedInUser, PreUser

from sayches.utils.export_csv import ExportCsvMixin
from .models import Activity, BlacklistUser, SendEmail, DeletedUser, \
    UserStatistics, UserRSA, CannedResponse
from .models import Profile, ReportUser, UserVerification, FromSayches

admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(PeriodicTask)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(SolarSchedule)


@admin.register(UserRSA)
class UserRSAAdmin(admin.ModelAdmin):
    list_display = ('user',)
    readonly_fields = ["user", "public_pem"]


User = get_user_model()


def deactivate_users(modeladmin, request, queryset):
    for user in queryset:
        user.is_active = False
        user.save()


def staff_user(modeladmin, request, querset):
    for user in querset:
        user.is_staff = True
        user.save()


staff_user.short_description = 'apply staff permission'
deactivate_users.short_description = 'Deactivate'


@admin.register(FromSayches)
class FromSaychesAdmin(admin.ModelAdmin):
    search_fields = ('to', 'title', 'message')
    list_display = ["to", "title", "message", "created_at"]
    list_filter = ['created_at']


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    search_fields = ('name', 'user_hash', 'email', 'notes')
    add_form = UserCreationForm
    fieldsets = (("User", {"fields":
                               ("user_hash", "country", "profile_update_time",
                                "warrant_canary",
                                "first_login", "first_post", "lost_virginity", "disposable", "auto_account_delete_time",
                                "last_activity_date", "notes", "send_email")}),)
    list_display = ["username", "name", "country", "warrant_canary", "first_post", "lost_virginity", "disposable",
                    "is_active", "is_superuser", "notes"]
    search_fields = ["name", "username"]
    actions = [deactivate_users, staff_user]
    list_filter = ['date_joined', 'is_staff', 'warrant_canary', 'country']

    def save_model(self, request, obj, form, change):
        obj.save()
        Profile.objects.get_or_create(user=obj)
        return super().save_model(request, obj, form, change)


class LoggedInUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key')
    readonly_fields = ["user", "session_key"]


admin.site.unregister(User)
admin.site.register(LoggedInUser, LoggedInUserAdmin)
admin.site.register(Session)
admin.site.register(User, UserAdmin)
admin.site.register(CannedResponse)


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'photo', 'bio', 'pgp_fingerprint', 'btc_address', 'website',
        'disable_notifications', 'disable_messages', 'disable_ping',)
    search_fields = ('bio', 'pgp_fingerprint', 'btc_address', 'website')
    readonly_fields = [
        'user', 'bio', 'pgp_fingerprint', 'btc_address', 'website',
        'disable_notifications', 'disable_messages', 'disable_ping', 'photo'
    ]
    date_hierarchy = 'created_at'


admin.site.register(Profile, ProfileAdmin)


@admin.register(UserVerification)
class UserVerificationAdmin(admin.ModelAdmin, ExportCsvMixin):
    ordering = ['-id']
    list_per_page = 15
    date_hierarchy = 'created_at'
    list_display = (
        'id', 'user', 'url', 'verification', 'verified')

    actions = ["export_as_csv"]


class ReportPostAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_per_page = 15
    list_display = (
        'id', 'user_reporter', 'user', 'complaint_date', 'removal_date', 'flagging_reason', 'flagger_type', 'outcome',
        'appeal', 'notes')
    list_filter = ['removal_date', 'complaint_date']
    actions = ["export_as_csv"]
    readonly_fields = ["user_reporter", "user", "complaint_date", "flagging_reason", ]
    date_hierarchy = 'created_at'
    search_fields = ('user_reporter', 'user', 'notes')


admin.site.register(ReportUser, ReportPostAdmin)


@admin.register(PreUser)
class PreUserAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id', 'name', 'email', 'is_added_by_admin')
    actions = ["export_as_csv"]
    date_hierarchy = 'created_at'


class DeletedUserAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_per_page = 15
    readonly_fields = ('id', 'user_hash', 'country', 'bio', 'pgp_fingerprint', 'btc_address',
                       'website', 'warrant_canary', 'profile_update_time', 'last_activity_date', 'disposable',
                       'notes', 'alias', 'lost_virginity', 'first_post', 'first_login',
                       'auto_account_delete_time', 'date_joined', 'deleted_date_time')
    list_display = ('id', 'user_hash', 'profile_update_time', 'last_activity_date',
                    'auto_account_delete_time', 'deleted_date_time')
    list_filter = ['auto_account_delete_time', 'last_activity_date', 'profile_update_time']
    actions = ["export_as_csv"]
    date_hierarchy = 'created_at'


@admin.register(SendEmail)
class SendEmailAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('_from', '_to', '_subject', '_message', 'created_at')
    list_filter = ['_from', 'created_at']
    actions = ["export_as_csv"]
    date_hierarchy = 'created_at'
    search_fields = ('_from', '_to', '_subject', '_message')


admin.site.register(DeletedUser, DeletedUserAdmin)


class UserStatisticsAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_per_page = 15
    list_display = ('id', 'date', 'total_users', 'total_active_users', 'total_inactive_users', 'total_verified_users',
                    "total_deleted_user")
    actions = ["export_as_csv"]
    list_filter = ['date', 'total_users', 'total_active_users', 'total_inactive_users', 'total_verified_users',
                   'total_deleted_user']
    date_hierarchy = 'date'


admin.site.register(UserStatistics, UserStatisticsAdmin)


class BlacklistUserAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_per_page = 15
    list_display = ('id', 'user', 'on_post', 'on_login', 'on_message', "suspended_message")
    actions = ["export_as_csv"]
    date_hierarchy = 'created_at'


admin.site.register(BlacklistUser, BlacklistUserAdmin)


class ActivityNotifications(admin.ModelAdmin):
    list_display = ["id", 'sender', 'receiver', 'target_id', 'created_at', 'count']
    readonly_fields = ["id", "sender", "receiver", "verb", "target_ct", "target_id", "target", "activity_type", "read",
                       "count"]
    list_filter = ['created_at']
    date_hierarchy = 'created_at'


admin.site.register(Activity, ActivityNotifications)
