from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Product

class ProductAPITests(APITestCase):
    def setUp(self):
        # 1. Crear un usuario y forzar autenticación para permitir POST, PATCH y DELETE
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)

        # 2. Crear un producto de prueba con un vector dummy (384 dimensiones)
        self.product = Product.objects.create(
            asin="TEST01",
            title="Mechanical Keyboard",
            description="A clicky mechanical keyboard for typing.",
            category="Electronics",
            price=99.99,
            embedding=[0.1] * 384,
        )

        # 3. Definir URLs de los endpoints
        self.list_url = reverse("products:product_list")
        self.detail_url = reverse(
            "products:product_detail", kwargs={"pk": self.product.pk}
        )
        self.recommend_url = reverse(
            "products:product_recommendations", kwargs={"pk": self.product.pk}
        )
        self.search_url = reverse("products:product_semantic_search")

    def test_list_products(self):
        """Test que el listado de productos funciona y está paginado."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verificamos dentro de 'results' debido a la paginación configurada
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]["asin"], "TEST01")

    def test_create_product(self):
        """Test para crear un nuevo producto (requiere autenticación)."""
        data = {
            "asin": "TEST02",
            "title": "Gaming Mouse",
            "description": "High DPI mouse.",
            "category": "Electronics",
            "price": 49.99,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_retrieve_product(self):
        """Test para obtener el detalle de un solo producto."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Mechanical Keyboard")

    def test_update_product(self):
        """Test para actualizar un producto (requiere autenticación)."""
        data = {"price": 89.99}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, 89.99)

    def test_delete_product(self):
        """Test para eliminar un producto (requiere autenticación)."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_embedding_exclusion(self):
        """Verifica que el campo sensible 'embedding' no se envíe en la API."""
        response = self.client.get(self.detail_url)
        self.assertNotIn("embedding", response.data)

        response = self.client.get(self.list_url)
        self.assertNotIn("embedding", response.data['results'][0])

    def test_semantic_search(self):
        """Test de estructura de respuesta en búsqueda semántica."""
        response = self.client.get(self.search_url, {"q": "keyboard"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("has_exact_matches", response.data)
        self.assertIn("results", response.data)

    def test_search_no_results(self):
        """Test de búsqueda vacía."""
        response = self.client.get(self.search_url, {"q": ""}, follow=True)
        # El endpoint devuelve 400 si falta el parámetro 'q'
        if response.status_code == 400:
            self.assertIn("q", response.data)
        else:
            self.assertEqual(len(response.data["results"]), 0)

    def test_product_recommendations(self):
        """Test que las recomendaciones devuelven productos similares paginados."""
        Product.objects.create(
            asin="TEST03",
            title="Another Keyboard",
            category="Electronics",
            price=120.00,
            embedding=[0.1] * 384,
        )
        response = self.client.get(self.recommend_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Corregido: Accedemos a 'results' por la paginación
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)

    def test_invalid_id(self):
        """Test de error 404 para IDs inexistentes."""
        url = reverse("products:product_detail", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)