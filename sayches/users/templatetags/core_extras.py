import re

from django import template
from django.utils.safestring import mark_safe
from posts.utils import convert_to_anchor_tag

register = template.Library()


@register.filter(name='linkify')
def linkify(value):
    anchor_tags = re.findall(r'@[\w\.-]+', value)
    hashtags = re.findall(r'#[\w\.-]+', value)
    for mention in anchor_tags:
        user_url = "/u/" + str(mention).replace('@', '%40', 1)
        value = convert_to_anchor_tag(value, user_url, mention)
    for hash in hashtags:
        hash_url = "/h/" + str(hash).replace('#', '%23', 1)
        value = convert_to_anchor_tag(value, hash_url, hash)
    return value


class CaptureasNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = mark_safe(self.nodelist.render(context).strip())
        context[self.varname] = output
        return ''
