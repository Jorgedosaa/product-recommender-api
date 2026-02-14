from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Product


class ProductAPITests(APITestCase):
    def setUp(self):
        # Create a test product with a dummy vector (384 dimensions)
        self.product = Product.objects.create(
            asin="TEST01",
            title="Mechanical Keyboard",
            description="A clicky mechanical keyboard for typing.",
            category="Electronics",
            price=99.99,
            embedding=[0.1] * 384,  # Simulate an embedding
        )
        self.list_url = reverse("products:product_list")
        self.detail_url = reverse(
            "products:product_detail", kwargs={"pk": self.product.pk}
        )
        self.recommend_url = reverse(
            "products:product_recommendations", kwargs={"pk": self.product.pk}
        )
        self.search_url = reverse("products:product_semantic_search")

    def test_list_products(self):
        """Test that product listing works correctly."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["asin"], "TEST01")

    def test_create_product(self):
        """Test creating a new product."""
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
        """Test retrieving a single product detail."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Mechanical Keyboard")

    def test_update_product(self):
        """Test updating a product."""
        data = {"price": 89.99}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, 89.99)

    def test_delete_product(self):
        """Test deleting a product."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_embedding_exclusion(self):
        """Verify that the sensitive 'embedding' field is excluded from API responses."""
        response = self.client.get(self.detail_url)
        self.assertNotIn("embedding", response.data)

        response = self.client.get(self.list_url)
        self.assertNotIn("embedding", response.data[0])

    def test_semantic_search(self):
        """Test that semantic search returns the expected structure."""
        response = self.client.get(self.search_url, {"q": "keyboard"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify it includes our confidence metadata
        self.assertIn("has_exact_matches", response.data)
        self.assertIn("results", response.data)

    def test_search_no_results(self):
        """Test search with empty query returns empty results."""
        response = self.client.get(self.search_url, {"q": ""})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_product_recommendations(self):
        """Test that the recommendation endpoint returns similar products."""
        # Create a second product to be recommended
        Product.objects.create(
            asin="TEST03",
            title="Another Keyboard",
            category="Electronics",
            price=120.00,
            embedding=[0.1] * 384,
        )
        response = self.client.get(self.recommend_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        # Should find the other product
        self.assertEqual(len(response.data), 1)

    def test_invalid_id(self):
        """Test accessing a non-existent product ID."""
        url = reverse("products:product_detail", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
