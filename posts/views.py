from typing import Any
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.query import QuerySet
from django.views import View
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.db.models import Q

from helpers.pagination import PaginationMixin

from .models import Post


class PostListView(PaginationMixin, ListView):
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


class PostByCategoryView(PaginationMixin, ListView):
    model = Post
    template_name = "blog/blog list/blog.html"
    context_object_name = "posts"

    def get_queryset(self) -> QuerySet[Any]:
        return (
            super().get_queryset().filter(category__name=self.kwargs["category_name"])
        )


class PostByTagView(PaginationMixin, ListView):
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
        else:
            posts = Post.objects.all()

        page_obj = Paginator(posts, 10)
        page = request.GET.get("page", 1)

        try:
            page_obj = page_obj.page(page)
        except PageNotAnInteger:
            page_obj = page_obj.page(1)
        except EmptyPage:
            page_obj = page_obj.page(page_obj.num_pages)

        return render(
            request,
            self.template_name,
            {
                "posts": posts,
                "page_obj": page_obj,
                "query": query,
                "is_paginated": page_obj.has_other_pages(),
            },
        )
