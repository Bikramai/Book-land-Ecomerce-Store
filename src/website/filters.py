import django_filters
from django.db.models import Q
from django.forms import TextInput

from src.administration.admins.models import Product, Post


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Search'
                                      , widget=TextInput(attrs={'placeholder': 'Search By Comic , Novel ,Artist or '
                                                                               'Author Name',
                                                                'class': 'form-control '}),
                                      method='product_filter')

    class Meta:
        model = Product
        fields = ['title', 'book_type', ]

    def product_filter(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value) | Q(artist__icontains=value)
                               | Q(author__icontains=value))


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label=''
                                      , widget=TextInput(attrs={'placeholder': 'Search Posts here',
                                                                'class': 'form-control rounded-pill'}),
                                      method='post_filter')

    class Meta:
        model = Post
        fields = ['title', 'author']

    def post_filter(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(content__icontains=value))
