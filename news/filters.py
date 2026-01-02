from django_filters import FilterSet, ModelChoiceFilter
import django_filters
from .models import Post, User


class PostFilter(FilterSet):
    author_username = ModelChoiceFilter(
        field_name='author__user',
        queryset=User.objects.filter(is_active=True).exclude(is_superuser=True).order_by('username'),
        to_field_name='username',
        lookup_expr='exact',
        label='Поиск по имени автора',
        empty_label='Все авторы'
    )

    title_post = django_filters.CharFilter (
        field_name='title',
        lookup_expr='icontains',
        label='Поиск по названию'
    )

    time_in_post = django_filters.DateFromToRangeFilter(
        field_name='time_in',
        label='Период публикации',
        widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = {
        }