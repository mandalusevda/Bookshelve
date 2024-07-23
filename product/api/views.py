
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, status,serializers
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser


from .paginations import DefaultPagination

from product.product_service import ProductService
from product.models import Product,Rating,Category,Genre

from .seriailizers import ProductSerializer,RatingSerializer,CategorySerializer,GenreSerializer

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

@extend_schema_view(
    create=extend_schema(tags=["Product"], summary="Create a new product"),
    retrieve=extend_schema(tags=["Product"], summary="Retrieve a single product."),
    list=extend_schema(tags=["Product"], summary="Retrieve a list of products"),
    update=extend_schema(tags=["Product"], summary="Update a product"),
    partial_update=extend_schema(tags=["Product"], summary="Partial update a product"),
    destroy=extend_schema(tags=["Product"], summary="Deletes a product"),
)

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    lookup_field='sku'
    lookup_url_kwarg = 'sku'

    # Filter options
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    filterset_fields = [
        'is_special'
    ]
    search_fields = [
        'sku', 
        'title', 
        "description",
    ]
    ordering_fields = [
        'title'
    ]
    permission_classes = [IsAdminUser]
    pagination_class = DefaultPagination

    ACTION_PERMISSIONS = {
        "list": [AllowAny()],
        "retrieve": [AllowAny()],
        "list_variants": [AllowAny()],
    }

    def get_queryset(self):
        return ProductService.get_product_queryset(self.request)

    def create(self, request, *args, **kwargs):
        # Validate
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        # Create product
        product = ProductService.create_product(**payload)

        # Return the serialized response
        return Response(
            serializer.to_representation(product), status=status.HTTP_201_CREATED
        )


@extend_schema_view(
    create=extend_schema(tags=["Rating"], summary="Create a new rating"),
    retrieve=extend_schema(tags=["Rating"], summary="Retrieve a single rating"),
    list=extend_schema(tags=["Rating"], summary="Retrieve a list of ratings"),
    update=extend_schema(tags=["Rating"], summary="Update an rating"),
    destroy=extend_schema(tags=["Rating"], summary="Deletes an rating"),
)
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    http_method_names = ["post", "get", "put", "delete"]
    # TODO add test for pagination
    ordering_fields = [
        "rating",
    ]
    pagination_class = DefaultPagination
    ACTION_PERMISSIONS = {
        "list": [AllowAny()],
        "retrieve": [AllowAny()],
    }

    def get_permissions(self):
        return self.ACTION_PERMISSIONS.get(self.action, super().get_permissions())

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @api_view(["POST"])
    def accept_rating(request, rating_id):
        try:
            rating = Rating.objects.get(pk=rating_id)
            rating.status = "accepted"
            rating.save()
            return Response({"status": "Rating accepted"})
        except Rating.DoesNotExist:
            return Response({"error": "Rating not found"}, status=404)

    @api_view(["POST"])
    def reject_rating(request, rating_id):
        try:
            rating = Rating.objects.get(pk=rating_id)
            rating.delete()
            return Response({"status": "Rating rejected"})
        except Rating.DoesNotExist:
            return Response({"error": "Rating not found"}, status=404)

@extend_schema_view(
    create=extend_schema(tags=["Category"], summary="Create a new category"),
    retrieve=extend_schema(tags=["Category"], summary="Retrieve a category"),
    list=extend_schema(tags=["Category"], summary="Retrieve a list of categories"),
    update=extend_schema(tags=["Category"], summary="Update a category"),
    destroy=extend_schema(tags=["Category"], summary="Deletes a category"),
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()  #.order_by("-created_at") descending order
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = DefaultPagination
    http_method_names = ["post", "get", "put", "delete"]

    ACTION_PERMISSIONS = {
        "list": [AllowAny()],
        "retrieve": [AllowAny()],
    }

    def get_permissions(self):
        return self.ACTION_PERMISSIONS.get(self.action, super().get_permissions())

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Check if the category is its own parent only during update
        if "parent" in serializer.validated_data:
            if serializer.validated_data["parent"] == instance:
                raise serializers.ValidationError(
                    {"parent": "A category cannot be a parent of itself."}
                )

        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


@extend_schema_view(
    create=extend_schema(tags=["Genre"], summary="Create a new genre"),
    retrieve=extend_schema(tags=["Genre"], summary="Retrieve a single genre"),
    list=extend_schema(tags=["Genre"], summary="Retrieve a list of genres"),
    update=extend_schema(tags=["Genre"], summary="Update an genre"),
    destroy=extend_schema(tags=["Genre"], summary="Deletes an genre"),
)
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    http_method_names = ["post", "get", "put", "delete"]
    # TODO add test for pagination
    ordering_fields = [
        "rating",
    ]
    pagination_class = DefaultPagination
    ACTION_PERMISSIONS = {
        "list": [AllowAny()],
        "retrieve": [AllowAny()],
    }

    def get_permissions(self):
        return self.ACTION_PERMISSIONS.get(self.action, super().get_permissions())

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

