from rest_framework import serializers

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        field = [
            'title', 'content', 'price', 'sale_price'
        ]
        fields = '__all__'