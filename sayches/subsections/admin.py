from django.contrib import admin
from django.utils.safestring import mark_safe

from sayches.utils.export_csv import ExportCsvMixin
from .models import Doc, News, Help, Ads


@admin.register(Ads)
class AdsAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ["slug", 'user', 'ad_headline', 'status', 'notes',
                    'created_at']
    readonly_fields = (
        'ad_price', 'slug', 'payment_method', 'voucher_code', 'discount', 'amount_due', 'btc_amount_due',
        'to_bitcoin_address', 'user', 'ad_plan', 'impressions', 'clicks', 'created_at')
    list_filter = ('user', 'ad_start_date', 'ad_end_date', 'status', 'ad_price')
    date_hierarchy = 'created_at'
    search_fields = (
        'ad_headline', 'ad_link', 'ad_body', 'ad_location', 'ad_keywords',
        'slug', 'notes', 'status'
    )

    def ad_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.url, width=110, height=110, ))

    actions = ["export_as_csv"]


@admin.register(Doc)
class DocAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ["id", 'name', 'slug']
    actions = ["export_as_csv"]
    date_hierarchy = 'created_at'
    search_fields = ('name', 'content', 'slug')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ["id", 'author_name', 'publish_date', 'article_title', 'author_name', 'tag', 'slug']
    actions = ["export_as_csv"]
    list_filter = ('publish_date', 'tag')
    date_hierarchy = 'created_at'
    search_fields = ('author_name', 'article_title', 'slug', 'article_content')

    def author_image_photo(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.author_image.url,
            width=110,
            height=110,
        )
        )

    def article_image_photo(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.article_image.url,
            width=110,
            height=110,
        )
        )


class HelpAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ["id", 'username', 'what_i_did', 'what_i_expected_to_happen', 'what_actually_happened',
                    'anything_else', 'status']
    readonly_fields = ('username', 'what_i_did', 'what_i_expected_to_happen', 'what_actually_happened',
                    'anything_else', 'reference_number',)
    actions = ["export_as_csv"]
    date_hierarchy = 'created_at'
    search_fields = (
        'username', 'what_i_did', 'what_i_expected_to_happen', 'what_actually_happened', 'anything_else', 'admin_notes')


admin.site.register(Help, HelpAdmin)
