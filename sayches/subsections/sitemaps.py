from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class HomeStaticViewSitemap(Sitemap):
    changefreq = "always"
    priority = 0.9

    def items(self):
        return ['subsections:home', 'subsections:docs', 'subsections:news',
                'subsections:help', 'subsections:index', 'subsections:ads']

    def location(self, items):
        return reverse(items)
