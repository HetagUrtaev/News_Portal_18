from django.urls import path
from .views import ArticlesEdit, ArticlesDelete, ArticlesCreate

app_name = 'articles'

urlpatterns = [
    path('create/', ArticlesCreate.as_view(), name='articles_create'),
    path('<int:pk>/edit/',  ArticlesEdit.as_view(), name='news_edit'),
    path('<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete')
]