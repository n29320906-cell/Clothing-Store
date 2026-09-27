from django.urls import path
from rest_framework.routers import DefaultRouter
from .api_views import RegisterView

from .api_views import (
    ProductViewSet,
    CategoryViewSet,
    RegisterAPIView,
)


router = DefaultRouter()

router.register(
    "products",
    ProductViewSet,
    basename="product"
)
path(
    "register/",
    RegisterView.as_view(),
    name="register"
),

router.register(
    "categories",
    CategoryViewSet,
    basename="category"
)


urlpatterns = [
    path(
        "register/",
        RegisterAPIView.as_view(),
        name="register"
    ),
]

urlpatterns += router.urls