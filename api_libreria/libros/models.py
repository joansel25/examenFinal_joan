# libros/models.py

from django.db import models
from django.core.validators import MinValueValidator


class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=150)
    isbn = models.CharField(max_length=13, unique=True, db_index=True)
    paginas = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Cantidad de ejemplares disponibles"
    )
    publicado_en = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros" 
        ordering = ['-id']

    def __str__(self):
        return f"{self.titulo} - {self.autor}"