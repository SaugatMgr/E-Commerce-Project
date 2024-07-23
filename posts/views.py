from typing import Any
from django.db.models.query import QuerySet
from django.views import View
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.db.models import Q

from posts.helpers import PostContextMixin

from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "blog/blog list/blog.html"
    context_object_name = "posts"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/blog detail/blog_detail.html"
    context_object_name = "blg_post_detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_post = self.get_object()
        context["related_posts"] = (
            super()
            .get_queryset()
            .filter(
                Q(category=current_post.category) | Q(tag__in=current_post.tag.all())
            )
            .exclude(id=current_post.id)
            .distinct()
            # .select_related("category")
            # .prefetch_related("tag")
        )
        return context


class PostByCategoryView(PostContextMixin, ListView):
    model = Post
    template_name = "blog/blog list/blog.html"
    context_object_name = "posts"

    def get_queryset(self) -> QuerySet[Any]:
        return (
            super().get_queryset().filter(category__name=self.kwargs["category_name"])
        )


class PostByTagView(PostContextMixin, ListView):
    model = Post
    template_name = "blog/blog list/blog.html"
    context_object_name = "posts"

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(tag__name=self.kwargs["tag_name"])


class PostSearchView(View):
    template_name = "blog/blog list/blog.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get("post_search_query")
        if query:
            posts = Post.objects.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(tag__name__icontains=query)
                | Q(category__name__icontains=query)
                | Q(author__first_name__icontains=query)
                | Q(author__last_name__icontains=query)
            ).distinct()
        return render(request, self.template_name, {"posts": posts})
