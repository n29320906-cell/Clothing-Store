from .models import Product, Category
from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    password2 = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {
                    "password": "Пароли не совпадают."
                }
            )

        if User.objects.filter(
            username=attrs["username"]
        ).exists():
            raise serializers.ValidationError(
                {
                    "username": "Такой пользователь уже существует."
                }
            )

        if User.objects.filter(
            email=attrs["email"]
        ).exists():
            raise serializers.ValidationError(
                {
                    "email": "Этот email уже используется."
                }
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        return user


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )

        return user


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

        from django.contrib.auth.models import User
        from rest_framework import serializers

        class RegisterSerializer(serializers.ModelSerializer):

            password = serializers.CharField(
                write_only=True,
                min_length=8
            )

            password2 = serializers.CharField(
                write_only=True
            )

            class Meta:
                model = User
                fields = [
                    "username",
                    "email",
                    "password",
                    "password2",
                ]

            def validate(self, attrs):

                if attrs["password"] != attrs["password2"]:
                    raise serializers.ValidationError({
                        "password": "Пароли не совпадают."
                    })

                if User.objects.filter(
                        username=attrs["username"]
                ).exists():
                    raise serializers.ValidationError({
                        "username": "Такой пользователь уже существует."
                    })

                if User.objects.filter(
                        email=attrs["email"]
                ).exists():
                    raise serializers.ValidationError({
                        "email": "Этот email уже используется."
                    })

                return attrs

            def create(self, validated_data):

                validated_data.pop("password2")

                user = User.objects.create_user(
                    username=validated_data["username"],
                    email=validated_data["email"],
                    password=validated_data["password"],
                )

                return user