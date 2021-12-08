from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy, reverse
from subsections.models import News


class NewsroomFeed(Feed):
    title = 'Sayches / Newsroom'
    link = reverse_lazy('subsections:news')

    def items(self):
        return News.objects.all().order_by('-created_at')[:5]

    def item_title(self, item):
        return item.article_title

    def item_link(self, item):
        return reverse('subsections:article', args=[item.slug])
