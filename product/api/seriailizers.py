from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
    HyperlinkedIdentityField,
    HyperlinkedRelatedField
)
from product.models import (
    Product,
    Category,
    Rating,
    Genre
)

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'sku',
            'title',
            'subtitle',
            'description',
            'summary',
            'is_special',
            'rating',
            'stock',
        ]

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = [
            "id", 
            "user", 
            "rating", 
            "message", 
            "status", 
            "product"
        ]
        read_only_fields = [
            "status", 
            "user"
        ]

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"