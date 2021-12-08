from django import template
from posts.models import Likes

register = template.Library()


@register.simple_tag
def like(user, post):
    like = Likes.objects.filter(user=user, post=post)
    if like:
        return True
    else:
        return False


@register.simple_tag
def get_companion(user, chat):
    for u in chat.members.all():
        if u != user:
            return u
    return None
