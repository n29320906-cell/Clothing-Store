from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Category
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    RegisterSerializer,
)


class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer


class CategoryViewSet(ModelViewSet):

    queryset = Category.objects.all()

    serializer_class = CategorySerializer


class RegisterAPIView(APIView):

    permission_classes = []

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.save()

            return Response(
                {
                    "message": "Регистрация успешна",
                    "username": user.username,
                    "email": user.email,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    from rest_framework import generics
    from rest_framework.permissions import AllowAny

    from .serializers import RegisterSerializer

    class RegisterView(generics.CreateAPIView):
        serializer_class = RegisterSerializer
        permission_classes = [AllowAny]