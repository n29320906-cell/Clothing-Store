from django.urls import path
from rest_framework.routers import DefaultRouter

from .api_views import (
    ProductViewSet,
    CategoryViewSet,
    RegisterAPIView,
)


# =========================
# ROUTER
# =========================

router = DefaultRouter()

router.register(
    "products",
    ProductViewSet,
    basename="product"
)

router.register(
    "categories",
    CategoryViewSet,
    basename="category"
)


# =========================
# API URLS
# =========================

urlpatterns = [

    path(
        "register/",
        RegisterAPIView.as_view(),
        name="api_register"
    ),

]


# =========================
# ROUTER URLS
# =========================

urlpatterns += router.urls