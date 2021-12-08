from django.contrib import admin

from .models import Chat, Message, SaychesMessage


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    filter_horizontal = ['members']
    list_filter = ['time_of_last_msg']
    readonly_fields = ('members', 'time_of_last_msg', 'is_read')
    list_display = ('get_members', 'is_read', 'time_of_last_msg', 'is_read', 'created_at')
    date_hierarchy = 'created_at'


class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'author', 'preference', 'is_read', 'new', 'created_at')
    list_filter = ['created_at']
    readonly_fields = ('chat', 'author', 'message', 'sender_message', 'preference', 'is_read', 'new')
    date_hierarchy = 'created_at'


admin.site.register(Message, MessageAdmin)


class SaychesMessageAdmin(admin.ModelAdmin):
    list_display = ('message', 'is_read', 'created_at')
    list_filter = ['created_at']
    date_hierarchy = 'created_at'


admin.site.register(SaychesMessage, SaychesMessageAdmin)
