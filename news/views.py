from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)
from .models import Post
from .filters import PostFilter
from .forms import NewsForm
from django.urls import reverse_lazy


class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news1.html'
    context_object_name = 'news1'

class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post_type = 'NE'
        self.object.save()
        return super().form_valid(form)

class ArticlesCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'articles_create.html'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post_type = 'AR'
        self.object.save()
        return super().form_valid(form)

class NewsEdit(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.post_type != 'NE':
            return self.handle_no_permission()  # Можно вернуть 403 или redirect
        return super().dispatch(request, *args, **kwargs)

class ArticlesEdit(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'articles_create.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.post_type != 'AR':
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news:post_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.post_type != 'NE':
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('news:post_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.post_type != 'AR':
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)