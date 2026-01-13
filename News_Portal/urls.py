from django.contrib import admin
from django.urls import path, include
from news.views import Profile
from news.views import upgrade_me

urlpatterns = [
   path('accounts/', include('allauth.urls')),
   #path('oauth/', include('social_django.urls', namespace='social')), #метка
   path("", Profile.as_view(), name = 'profile'),
   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),
   path('', include('news.urls')),
]