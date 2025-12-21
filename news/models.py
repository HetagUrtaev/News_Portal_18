from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        posts_rating = (
            Post.objects.filter(author=self)
            .aggregate(sum_rating=Coalesce(Sum('rating'), 0))['sum_rating']
        )

        comments_rating = (
            Comment.objects.filter(user=self.user)
            .aggregate(sum_rating=Coalesce(Sum('rating'), 0))['sum_rating']
        )

        post_comments_rating = (
            Comment.objects.filter(post__author=self)
            .aggregate(sum_rating=Coalesce(Sum('rating'), 0))['sum_rating']
        )

        self.rating = posts_rating * 3 + comments_rating + post_comments_rating
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    article = 'AR'
    news = 'NE'

    POST = [
        (article, 'Статья'),
        (news, 'Новость'),

    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2,
                                 choices=POST,
                                 default=article)
    time_in = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory', related_name='posts')
    title = models.CharField(max_length=250)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def preview(self):
        if len(self.text) < 124:
            return self.text
        return f"{self.text[:124]}..."

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()