from django.urls import path

from .views import PostListView, PostDetailView

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("<uuid:post_id>/", PostDetailView.as_view(), name="post_detail"),
]
