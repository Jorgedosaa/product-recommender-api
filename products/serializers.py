from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    The 'embedding' field is excluded by default to keep API responses 
    clean and readable, as it contains high-dimensional vector data.
    """
    class Meta:
        model = Product
        # We explicitly list or exclude fields to avoid sending raw 
        # vector data (384+ floats) to the client.
        exclude = ["embedding"]

    def to_representation(self, instance):
        """
        Optional: Ensure price is formatted as a float/decimal 
        and handle potential null values.
        """
        representation = super().to_representation(instance)
        if representation.get('price'):
            representation['price'] = float(representation['price'])
        return representation