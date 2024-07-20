from django.views.generic import ListView, DetailView
from django.shortcuts import render

from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "blog/blog_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/blog_detail.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context["post"] = Post.objects.get(id=self.kwargs["post_id"])

        return render(request, self.template_name, context)
