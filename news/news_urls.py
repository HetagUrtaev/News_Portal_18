from django.urls import path
from .views import PostList, PostDetail, NewsCreate,  NewsEdit, NewsDelete
from news.views import upgrade_me

app_name = 'news'

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/',  NewsEdit.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('upgrade/', upgrade_me, name = 'upgrade')
]