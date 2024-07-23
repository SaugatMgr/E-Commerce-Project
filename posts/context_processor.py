from datetime import datetime
from django.db.models import Count
from posts.models import Post, PostCategory, PostTag


def posts_context(request):
    context = {}
    current_year = datetime.now().year
    all_posts = Post.objects.all()
    monthly_posts_count = (
        all_posts.filter(published_on__year=current_year, status="published")
        .values("published_on__month")
        .annotate(count=Count("id"))
    )

    context["recent_posts"] = all_posts[:5]
    context["post_categories"] = PostCategory.objects.all()[:5]
    context["post_tags"] = PostTag.objects.all()[:21]
    context["blog_archives"] = [
        {
            "year": current_year,
            "month": item["published_on__month"],
            "count": item["count"],
        }
        for item in monthly_posts_count
    ]
    for archive in context["blog_archives"]:
        archive["month"] = datetime.strptime(str(archive["month"]), "%m").strftime("%B")

    return context
