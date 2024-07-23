from itertools import product as options_combination

from django.db.models import Prefetch

from product.models.product import Product



class ProductService:
    product = None
    price: int | float
    stock: int
    category: list = []

    @classmethod
    def create_product(cls, **data):
        """
        Create a new product with options and return the product object.

        Note:
            This method creates a new product instance, generates options, and optimizes queries
            for retrieving the product with related options and variants.

        """

        # Extract relevant data
        cls.stock = data.pop("stock")
        # Add categories to product
        # Create product
        cls.product = Product.objects.create(**data)
     
        # Return product object
        return cls.product
    
    @classmethod
    def get_product_queryset(cls, request):
        queryset = Product.objects.all()
        return queryset.order_by("id")

   