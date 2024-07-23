# helper classes/functions for posts app

from posts.models import Post, PostCategory, PostTag


class PostContextMixin:
    def get_shared_context_data(self, **kwargs):
        context = kwargs
        all_posts = Post.objects.all()

        context["posts"] = all_posts
        context["recent_posts"] = all_posts[:5]
        context["post_categories"] = PostCategory.objects.all()[:5]
        context["post_tags"] = PostTag.objects.all()[:21]
        
        return context