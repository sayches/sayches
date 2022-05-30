from django.contrib import admin
from django.utils.safestring import mark_safe

from sayches.utils.export_csv import ExportCsvMixin
from .models import Post, Hashtag, ReportPost, Likes, LinkValidation, \
    PostsTimestamp, BlacklistWords


@admin.register(BlacklistWords)
class BlacklistWordsAdmin(admin.ModelAdmin):
    list_display = ['word', 'is_emoji', 'created_at']
    list_filter = ['is_emoji', 'created_at']
    date_hierarchy = 'created_at'
    search_fields = ('word',)

@admin.register(PostsTimestamp)
class PostsTimestampAdmin(admin.ModelAdmin):
    list_display = ['user', 'post_id', 'post_timestamp']
    readonly_fields = ['user', 'post_id', 'post_timestamp']
    date_hierarchy = 'created_at'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin, ExportCsvMixin):
    filter_horizontal = ['post_followers']
    date_hierarchy = 'created_at'
    list_display = (
        'id',
        'user',
        'flair',
        'post_option',
        'image_thumbnail',
        'created_at',
        'pinned_post',
        'post_followers_count',
        'post_likes',
        'post_have_followers',
        'post_have_likes',
        'media',
        'restrict',
    )

    fieldsets = (
        ("Post", {"fields": (
            "user", "text", "flair", "post_followers", "post_option", "pinned_post", "media",
            "image_thumbnail", "restrict")}),
    )
    readonly_fields = [
        'id',
        'user',
        'text',
        'flair',
        'post_option',
        'image_thumbnail',
        'created_at',
        'pinned_post',
        'post_followers',
        'post_followers_count',
        'post_likes',
        'post_have_followers',
        'post_have_likes',
        'media',
    ]
    list_filter = ['created_at']
    actions = ["export_as_csv", "restrict_post"]
    search_fields = ('text',)

    def restrict_post(self, request, queryset):
        queryset.update(restrict=True)

    def post_followers_count(self, obj):
        return obj.post_followers.all().count()

    def post_have_followers(self, obj):
        return obj.post_followers.all().count() > 0

    def post_likes(self, obj):
        return Likes.objects.filter(post=obj).count()

    def post_have_likes(self, obj):
        return Likes.objects.filter(post=obj).count() > 0

    def image_thumbnail(self, obj):
        if obj.media:
            return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.media.url,
                width=110,
                height=110,
            )
            )
        else:
            return None

    post_have_likes.boolean = True
    post_have_followers.boolean = True

    post_followers_count.admin_order_field = 'post_followers'
    post_have_followers.admin_order_field = 'post_followers'
    post_likes.admin_order_field = 'post_likes'
    post_have_likes.admin_order_field = 'post_likes'


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin, ExportCsvMixin):
    filter_horizontal = ['posts']
    date_hierarchy = 'created_at'
    list_display = ('explicit_name', 'author', 'hashtag_counter')

    fieldsets = (
        ("Hashtag", {"fields": ("posts", "explicit_name", "implicit_name", "hashtag_counter", "status")}),
    )
    list_filter = ['created_at']
    readonly_fields = ['created_at']
    actions = ["export_as_csv"]
    search_fields = ('implicit_name',)


@admin.register(LinkValidation)
class LinkValidationAdmin(admin.ModelAdmin):
    list_display = ('url', 'type')
    date_hierarchy = 'created_at'

class ReportPostAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_per_page = 15
    list_display = (
        'id', 'post_reporter', 'post_user', 'post_id', 'complaint_date', 'removal_date', 'flagging_reason',
        'flagger_type',
        'outcome', 'appeal', 'notes')
    list_filter = ['removal_date', 'complaint_date']
    readonly_fields = ["post_id", "post_text", "post_user", "post_reporter", "post_url", "complaint_date",
                       "flagging_reason"]
    actions = ["export_as_csv"]
    date_hierarchy = 'created_at'
    search_fields = ('post_reporter', 'post_user', 'post_text')


admin.site.register(ReportPost, ReportPostAdmin)
