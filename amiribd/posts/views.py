from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView, DetailView
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "pages/posts.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post.html"
    context_object_name = "post"

    def get_object(self):
        post = get_object_or_404(
            Post,
            slug=self.kwargs.get("slug"),
            date_posted__year=self.kwargs.get("year"),
            date_posted__month=self.kwargs.get("month"),
            date_posted__day=self.kwargs.get("day"),
        )
        return post
