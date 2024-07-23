from django.urls import path, include
from rest_framework import routers
from django.urls import re_path
from rest_framework_simplejwt import views


from .views import (
    ProductViewSet,
    CategoryViewSet,
    RatingViewSet,
    GenreViewSet
)

router = routers.DefaultRouter()
router.register("products", ProductViewSet, basename="product")
router.register("categories", CategoryViewSet, basename="category")
router.register("ratings", RatingViewSet, basename="rating")
router.register("genres", GenreViewSet, basename="genres")

urlpatterns = (
    path('', include(router.urls)),
    re_path(r"^create/?", views.TokenObtainPairView.as_view(), name="jwt-create"),
    re_path(r"^refresh/?", views.TokenRefreshView.as_view(), name="jwt-refresh"),
    re_path(r"^verify/?", views.TokenVerifyView.as_view(), name="jwt-verify"),
)