from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import CreateAds, AdminNotifications, AdsPricing, Vouchers


@admin.register(AdsPricing)
class AdsPricingAdmin(admin.ModelAdmin):
    list_display = ["id", 'title', 'type', 'description', 'price']
    date_hierarchy = 'created_at'
    search_fields = ('title', 'type', 'description')


class CreateAdsAdmin(admin.ModelAdmin):
    list_display = ['ad_id', 'owner', 'headline', 'body', 'location', 'link', 'start_date', 'end_date']
    readonly_fields = (
        'owner', 'headline', 'body', 'location', 'target_all_users', 'target_user_list', 'link', 'image', 'keywords',
        'start_date', 'end_date', 'ad_id')
    list_filter = ('owner', 'location', 'start_date', 'end_date')
    date_hierarchy = 'created_at'
    search_fields = ('owner', 'headline', 'body', 'location', 'link')

    def ad_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.url, width=110, height=110, ))


admin.site.register(CreateAds, CreateAdsAdmin)


class AdminNotificationsAdmin(admin.ModelAdmin):
    list_display = ["id", 'nf_title', 'count', 'created_at']
    readonly_fields = ["count", "read"]
    filter_horizontal = ('user', 'notification_followers')
    list_filter = ['created_at']
    date_hierarchy = 'created_at'
    search_fields = ('nf_title', 'nf_url', 'nf_description')


admin.site.register(AdminNotifications, AdminNotificationsAdmin)


class VouchersAdmin(admin.ModelAdmin):
    list_display = ["id", 'to', 'voucher_code', 'discount_percentage', 'start_date', 'end_date', 'expired']
    list_filter = ['created_at', 'discount_percentage', 'expired']
    date_hierarchy = 'created_at'
    search_fields = ('to', 'voucher_code')


admin.site.register(Vouchers, VouchersAdmin)
