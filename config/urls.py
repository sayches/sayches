from django.conf import settings
from django.urls import include, path
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.views.generic.base import RedirectView, TemplateView
from django_otp.admin import OTPAdminSite
from users.models import User
from django.contrib.sitemaps.views import sitemap
from sayches.subsections.sitemaps import HomeStaticViewSitemap
from sayches.users.sitemaps import UserProfileStaticViewSitemap
from django.views.static import serve
import os
from rest_framework.authtoken.views import obtain_auth_token
from sayches.subsections.rss import NewsroomFeed

class OTPAdmin(OTPAdminSite):
    pass

from django_otp.admin import OTPAdminSite
from django_otp.plugins.otp_totp.models import TOTPDevice

admin_site = OTPAdmin(name='OTPAdmin')
admin_site.register(User)
admin_site.register(TOTPDevice)

urlpatterns = []

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")}, name="404"
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns


sitemaps = {
            "home_static": HomeStaticViewSitemap,
            "users_static":UserProfileStaticViewSitemap,
            }

ADMIN_URL = os.environ.get('ADMIN_PATH')

urlpatterns += [
                   path("", include("subsections.urls", namespace="subsections")),
                   path("", RedirectView.as_view(pattern_name='subsections:home', permanent=False)),
                   path(ADMIN_URL, admin.site.urls),
                   path("", include("sign.urls")),
                   path("", include("users.urls", namespace="profile")),
                   path("", include("posts.urls", namespace="posts")),
                   path("", include("ads.urls", namespace="ads")),
                   path("messages/", include("message.urls", namespace="message")),
                   path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
                   path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),),
                   path("api/", include("api.urls")),
                   path('auth/', obtain_auth_token),
                   path('newsroom/rss/', NewsroomFeed()),
]

DEBUG = os.environ.get('DEBUG')

if eval(DEBUG) == False:
    admin.site.__class__ = OTPAdminSite
admin.site.site_header = "Administration Area"
admin.site.site_title = "Sayches Admin Portal"
handler404 = 'sayches.custom_views.handler404'
