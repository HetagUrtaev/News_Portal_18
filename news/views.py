from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'news'

class PostDetail(DetailView):
    model = Post
    template_name = 'news1.html'
    context_object_name = 'news1'