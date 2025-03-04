import django_filters
from .models import *
class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Post
        fields = ['cls', 'title']

class BlogFilter(django_filters.FilterSet):
    class Meta:
        model = Blog
        fields = ['type',]