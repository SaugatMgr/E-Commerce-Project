from django.urls import path

from .views import (
    MonthlyArchiveView,
    PostByCategoryView,
    PostByTagView,
    PostCommentView,
    PostListView,
    PostDetailView,
    PostSearchView,
    ReplyView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("<uuid:pk>/", PostDetailView.as_view(), name="post_detail"),
    path(
        "post-by-category/<str:category_name>/",
        PostByCategoryView.as_view(),
        name="post_by_category_list",
    ),
    path(
        "post-by-tag/<str:tag_name>/", PostByTagView.as_view(), name="post_by_tag_list"
    ),
    path("post-search/", PostSearchView.as_view(), name="post_search"),
    path(
        "monthly-archive/<str:month>/<int:year>/",
        MonthlyArchiveView.as_view(),
        name="monthly_archive",
    ),
    path(
        "post-comment/",
        PostCommentView.as_view(),
        name="post_comment",
    ),
    path(
        "reply/",
        ReplyView.as_view(),
        name="reply",
    ),
]
