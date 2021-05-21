import django_filters
from django_filters import DateFilter, CharFilter

from .models import *


class ProjectFilter(django_filters.FilterSet):
    char = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Projects
        fields = '__all__'
