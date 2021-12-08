from django.contrib import admin

from .models import CloseWebsite, VersionNumber, CloseRegistration


class CloseWebsiteAdmin(admin.ModelAdmin):
    list_display = ["close_site", "closing_text"]


admin.site.register(CloseWebsite, CloseWebsiteAdmin)


class VersionNumberAdmin(admin.ModelAdmin):
    list_display = ['version_no', 'show_beta_icon', 'default', 'created_at']
    date_hierarchy = 'created_at'


admin.site.register(VersionNumber, VersionNumberAdmin)


class SaychesCustomizationAdmin(admin.ModelAdmin):
    list_display = ["id", 'custom_error_message', 'close_registration']


admin.site.register(CloseRegistration, SaychesCustomizationAdmin)
