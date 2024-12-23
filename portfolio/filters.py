import django_filters
from .models import Website

class WebsiteFilter(django_filters.FilterSet):
    skill = django_filters.CharFilter(field_name='skill__skill', lookup_expr='icontains')

    class Meta:
        model = Website
        fields = ["skill"]  # Leave the fields list empty since you're defining the filter manually
