from django.contrib import admin

from .models import Post, Comment
from .forms import PostAdminForm


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


admin.site.register(Post, PostAdmin)
admin.site.register(
    [
        Comment,
    ]
)
