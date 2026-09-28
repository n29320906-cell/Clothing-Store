from django.urls import path
from . import views


urlpatterns = [

    # =========================
    # HOME
    # =========================

    path(
        "",
        views.home,
        name="home"
    ),

    # =========================
    # AUTH
    # =========================

    path(
        "register/",
        views.register_view,
        name="register"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    # =========================
    # FAVORITES
    # =========================

    path(
        "favorites/",
        views.favorites,
        name="favorites"
    ),

    # =========================
    # PRODUCTS
    # =========================

    path(
        "product/<int:pk>/",
        views.product_detail,
        name="product_detail"
    ),

    path(
        "category/<int:pk>/",
        views.category_products,
        name="category_products"
    ),

    # =========================
    # CART
    # =========================

    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    path(
        "cart/add/<int:pk>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    path(
        "cart/increase/<int:pk>/",
        views.increase_cart,
        name="increase_cart"
    ),

    path(
        "cart/decrease/<int:pk>/",
        views.decrease_cart,
        name="decrease_cart"
    ),

    path(
        "cart/remove/<int:pk>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),

    # =========================
    # CHECKOUT
    # =========================

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    path(
        "order-success/<int:pk>/",
        views.order_success,
        name="order_success"
    ),

    # =========================
    # PRODUCT RATING
    # =========================

    path(
        "product/<int:pk>/rate/",
        views.rate_product,
        name="rate_product"
    ),
]