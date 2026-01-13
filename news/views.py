from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView, TemplateView)
from .models import Post
from .filters import PostFilter
from .forms import NewsForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')

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

class NewsCreate(PermissionRequiredMixin, CreateView): #создавать новости
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post_type = 'NE'
        self.object.save()
        return super().form_valid(form)

class ArticlesCreate(PermissionRequiredMixin, CreateView): #создавать статьи
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'articles_create.html'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post_type = 'AR'
        self.object.save()
        return super().form_valid(form)

class NewsEdit(PermissionRequiredMixin, UpdateView): #редактирование новостей
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.post_type != 'NE':
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class ArticlesEdit(PermissionRequiredMixin, UpdateView): #редактирование статей
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'articles_create.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.post_type != 'AR':
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news:post_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.post_type != 'NE':
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('news:post_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.post_type != 'AR':
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)