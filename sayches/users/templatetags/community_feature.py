from django import template

register = template.Library()


@register.filter
def community_feature(developer_name):
    text = "This feature is developed by and within the community. By {}.".format(developer_name)
    return text
