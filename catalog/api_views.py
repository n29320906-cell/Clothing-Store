from rest_framework.viewsets import ModelViewSet

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer


class CategoryViewSet(ModelViewSet):

    queryset = Category.objects.all()

    serializer_class = CategorySerializer