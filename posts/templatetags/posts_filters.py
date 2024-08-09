from django import template

register = template.Library()


@register.simple_tag
def has_liked_post(post, user):
    return post.user_has_liked(user=user)


@register.simple_tag
def has_disliked_post(post, user):
    return post.user_has_disliked(user=user)


@register.simple_tag
def has_liked_comment(comment, user):
    return comment.user_has_liked(user=user)


@register.simple_tag
def has_disliked_comment(comment, user):
    return comment.user_has_disliked(user=user)


@register.simple_tag
def has_liked_reply(reply, user):
    return reply.user_has_liked(user=user)


@register.simple_tag
def has_disliked_reply(reply, user):
    return reply.user_has_disliked(user=user)
