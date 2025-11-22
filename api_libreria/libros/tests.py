from .models import Libro
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class LibroAPITestCase(APITestCase):
    def setUp(self):
        self.libro_data = {
            "titulo": "Cien años de soledad",
            "autor": "Gabriel García Márquez",
            "isbn": "1234567890123",
            "paginas": 471,
            "stock": 5,
            "publicado_en": 1967
        }

    def test_crear_libro_valido(self):
        url = reverse('libro-list')
        response = self.client.post(url, self.libro_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Libro.objects.count(), 1)

    def test_isbn_duplicado(self):
        Libro.objects.create(**self.libro_data)
        response = self.client.post(reverse('libro-list'), self.libro_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_stock_negativo(self):
        data = self.libro_data.copy()
        data['stock'] = -1
        response = self.client.post(reverse('libro-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_paginacion(self):
        for i in range(15):
            Libro.objects.create(
                titulo=f"Libro {i}",
                autor=f"Autor Prueba {i}",
                isbn=f"1234567890{i:03d}",
                paginas=150,
                stock=4,
                publicado_en=2012
            )
        response = self.client.get(reverse('libro-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 10)

    def test_actualizar_y_parcial(self):
        libro = Libro.objects.create(**self.libro_data)
        url = reverse('libro-detail', kwargs={'pk': libro.pk})

        data = self.libro_data.copy()
        data['stock'] = 12
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Libro.objects.get(pk=libro.pk).stock, 12)

        response = self.client.patch(url, {'stock': 8}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Libro.objects.get(pk=libro.pk).stock, 8)

    def test_eliminar_libro(self):
        libro = Libro.objects.create(**self.libro_data)
        url = reverse('libro-detail', kwargs={'pk': libro.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Libro.objects.filter(pk=libro.pk).exists())