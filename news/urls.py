from django.urls import include, path

urlpatterns = [

    path('news/', include(('news.news_urls', 'news'), namespace='news')), #namespace='news' возможно лишнее
    path('articles/', include(('news.articles_urls', 'articles'), namespace='articles')),
]