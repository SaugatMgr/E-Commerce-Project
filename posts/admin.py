from django.contrib import admin

from .models import (
    Post,
    Comment,
    PostCategory,
    PostTag,
    Reply,
    PostLikes,
    PostDislikes,
    CommentLikes,
    CommentDislikes,
    ReplyLikes,
    ReplyDislikes,
)
from .forms import PostAdminForm


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


admin.site.register(Post, PostAdmin)
admin.site.register(
    [
        Comment,
        PostCategory,
        PostTag,
        Reply,
        PostLikes,
        PostDislikes,
        CommentLikes,
        CommentDislikes,
        ReplyLikes,
        ReplyDislikes,
    ]
)
