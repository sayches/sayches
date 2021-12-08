from django import template

register = template.Library()


@register.simple_tag(name="make_confirm_url", takes_context=True)
def make_confirm_url(context):
    activate_url = context.get('activate_url')
    slice_idx = activate_url.find('account')
    return ''.join(['http://', context.get('current_site').domain, '/', activate_url[slice_idx:]])
