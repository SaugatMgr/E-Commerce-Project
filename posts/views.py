from typing import Any
from datetime import datetime
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.query import QuerySet
from django.views import View
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string

from helpers.pagination import PaginationMixin

from .models import (
    CommentDislikes,
    CommentLikes,
    Post,
    Comment,
    PostDislikes,
    PostLikes,
    Reply,
    ReplyDislikes,
    ReplyLikes,
)


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


class MonthlyArchiveView(PaginationMixin, ListView):
    model = Post
    template_name = "blog/blog list/blog.html"
    context_object_name = "posts"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                published_on__year=self.kwargs["year"],
                published_on__month=datetime.strptime(self.kwargs["month"], "%B").month,
            )
        )


class PostCommentView(View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        comment = data.get("comment")
        post_id = data.get("blg_post_detail_id")

        with transaction.atomic():
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                if comment:
                    current_post = Post.objects.get(id=post_id)
                    comment = Comment.objects.create(
                        post=current_post,
                        comment_writer=request.user,
                        comment=comment,
                    )
                    html_content = render_to_string(
                        "blog/blog detail/comment_area.html",
                        {
                            "blg_post_detail": current_post,
                        },
                        request,
                    )
                    return JsonResponse(
                        {
                            "success": True,
                            "message": "Reply added.",
                            "html_content": html_content,
                        },
                        status=201,
                    )
                else:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "Comment cannot be empty.",
                        },
                        status=400,
                    )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Cannot process.Must be and AJAX XMLHttpRequest.",
                    },
                    status=400,
                )


class ReplyView(View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        reply = data.get("reply")
        blg_post_detail_id = data.get("blg_post_detail_id")
        comment_id = data.get("comment_id")
        parent_reply_id = data.get("parent_reply_id")

        with transaction.atomic():
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                blg_post_detail = Post.objects.get(id=blg_post_detail_id)
                if reply and not parent_reply_id:
                    current_comment = Comment.objects.get(id=comment_id)
                    reply = Reply.objects.create(
                        comment=current_comment,
                        reply_writer=request.user,
                        reply_content=reply,
                    )
                    html_content = render_to_string(
                        "blog/blog detail/comment_area.html",
                        {
                            "blg_post_detail": blg_post_detail,
                        },
                        request,
                    )
                    return JsonResponse(
                        {
                            "success": True,
                            "message": "Reply added.",
                            "html_content": html_content,
                        },
                        status=201,
                    )
                elif reply and parent_reply_id:
                    parent = Reply.objects.get(id=parent_reply_id)
                    reply = Reply.objects.create(
                        reply_writer=request.user,
                        reply_content=reply,
                        parent=parent,
                    )
                    html_content = render_to_string(
                        "blog/blog detail/comment_area.html",
                        {
                            "blg_post_detail": blg_post_detail,
                        },
                        request,
                    )
                    return JsonResponse(
                        {
                            "success": True,
                            "message": "Reply added.",
                            "html_content": html_content,
                        },
                        status=201,
                    )
                else:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "Reply cannot be empty.",
                        },
                        status=400,
                    )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Cannot process.Must be and AJAX XMLHttpRequest.",
                    },
                    status=400,
                )


class LikeDislikeView(View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        user = request.user

        obj_id = data.get("obj_id")
        model = data.get("model")
        action = data.get("action")

        with transaction.atomic():
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                if model == "post":
                    obj = Post.objects.get(id=obj_id)
                    like_model = PostLikes
                    dislike_model = PostDislikes
                elif model == "comment":
                    obj = Comment.objects.get(id=obj_id)
                    like_model = CommentLikes
                    dislike_model = CommentDislikes
                elif model == "reply":
                    obj = Reply.objects.get(id=obj_id)
                    like_model = ReplyLikes
                    dislike_model = ReplyDislikes
                else:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "Missing model.",
                        },
                        status=400,
                    )
                if action == "like":
                    like_model_obj = like_model.objects.filter(
                        user=user, **{f"{model}": obj}
                    )
                    if like_model_obj.exists():
                        like_model_obj.delete()
                        return JsonResponse(
                            {
                                "success": True,
                                "like_count": obj.like_count,
                                "dislike_count": obj.dislike_count,
                            },
                            status=200,
                        )
                    else:
                        like_model.objects.create(user=user, **{f"{model}": obj})
                        dislike_model.objects.filter(
                            user=user, **{f"{model}": obj}
                        ).delete()
                        return JsonResponse(
                            {
                                "success": True,
                                "like_count": obj.like_count,
                                "dislike_count": obj.dislike_count,
                            },
                            status=201,
                        )
                elif action == "dislike":
                    dislike_model_obj = dislike_model.objects.filter(
                        user=user, **{f"{model}": obj}
                    )
                    if dislike_model_obj.exists():
                        dislike_model_obj.delete()
                        return JsonResponse(
                            {
                                "success": True,
                                "like_count": obj.like_count,
                                "dislike_count": obj.dislike_count,
                            },
                            status=200,
                        )
                    else:
                        dislike_model.objects.create(user=user, **{f"{model}": obj})
                        like_model.objects.filter(
                            user=user, **{f"{model}": obj}
                        ).delete()
                        return JsonResponse(
                            {
                                "success": True,
                                "like_count": obj.like_count,
                                "dislike_count": obj.dislike_count,
                            },
                            status=201,
                        )
                else:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "Unknown action.",
                        },
                        status=400,
                    )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Cannot process.Must be and AJAX XMLHttpRequest.",
                    },
                    status=400,
                )
