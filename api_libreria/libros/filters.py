import django_filters
from django_filters import rest_framework as filters
from .models import Libro

class LibroFilter(filters.FilterSet):
    autor = filters.CharFilter(field_name='autor', lookup_expr='icontains')

    class Meta:
        model = Libro
        fields = ['autor']