from django import template


register = template.Library()


@register.filter
def top_level_replies(replies):
    return replies.filter(parent=None)
