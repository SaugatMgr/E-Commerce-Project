from posts.models import Post, PostCategory, PostTag

def posts_context(request):
    context = {}

    context["recent_posts"] = Post.objects.all()[:5]
    context["post_categories"] = PostCategory.objects.all()[:5]
    context["post_tags"] = PostTag.objects.all()[:21]
    
    return context
