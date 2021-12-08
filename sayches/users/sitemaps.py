from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class UserProfileStaticViewSitemap(Sitemap):
    changefreq = "always"
    priority = 0.9

    def items(self):
        return ['users:profile_update']

    def location(self, items):
        return reverse(items)
