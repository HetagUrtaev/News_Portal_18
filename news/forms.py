from django import forms
from .models import Post


class NewsForm(forms.ModelForm):

   class Meta:
       model = Post
       fields = ['author',
                 #'post_type',
                 'categories',
                 'title',
                 'text',
                 ]

       labels = {
           'author': 'Автор',
           #'post_type': 'Тип поста',
           'categories': 'Категории',
           'title': 'Заголовок',
           'text': 'Текст поста',
       }

       error_messages = {
           'title': {
                'unique': 'Пост с таким заголовком уже существует!',
                'max_length' : 'Максимальная длина не может быть больше 250 символов '
            },
        }

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user