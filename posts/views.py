from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.db.models import Q

from posts.helpers import PostContextMixin

from .models import Post


class PostListView(PostContextMixin, ListView):
    model = Post
    template_name = "blog/blog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_shared_context_data(**context)

        return context


class PostDetailView(PostContextMixin, DetailView):
    model = Post
    template_name = "blog/blog_detail.html"

    def get(self, request, *args, **kwargs):
        context = self.get_shared_context_data(**kwargs)
        current_post = Post.objects.get(id=self.kwargs["post_id"])
        context["blg_post_detail"] = current_post
        context["related_posts"] = (
            context.get("posts")
            .filter(
                Q(category=current_post.category) | Q(tag__in=current_post.tag.all())
            )
            .exclude(id=current_post.id)
            .distinct()
            # .select_related("category")
            # .prefetch_related("tag")
        )

        return render(request, self.template_name, context)
