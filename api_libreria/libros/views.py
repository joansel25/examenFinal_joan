from rest_framework import viewsets
from .models import Libro
from .serializers import LibroSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import LibroFilter

class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LibroFilter
    
