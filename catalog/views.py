from decimal import Decimal

from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)

from django.http import JsonResponse

from .models import (
    Product,
    Category,
    Order,
    OrderItem,
)


# =========================
# HOME
# =========================

def home(request):

    search = request.GET.get(
        "q",
        ""
    ).strip()

    # =========================
    # AUTOMATIC CATEGORIES
    # =========================

    category_names = [
        "Футболки",
        "Джинсы",
        "Куртки",
        "Обувь",
    ]

    for name in category_names:

        Category.objects.get_or_create(
            name=name
        )

    # =========================
    # PRODUCTS
    # =========================

    products = Product.objects.filter(
        available=True
    ).select_related(
        "category"
    )

    if search:

        products = products.filter(
            name__icontains=search
        )

    # =========================
    # CATEGORIES
    # =========================

    categories = Category.objects.all()

    return render(
        request,
        "catalog/home.html",
        {
            "products": products,
            "categories": categories,
            "search": search,
        }
    )


# =========================
# FAVORITES
# =========================

def favorites(request):

    products = Product.objects.filter(
        available=True
    ).select_related(
        "category"
    )

    return render(
        request,
        "catalog/favorites.html",
        {
            "products": products,
        }
    )


# =========================
# PRODUCT DETAIL
# =========================

def product_detail(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    return render(
        request,
        "catalog/product_detail.html",
        {
            "product": product,
        }
    )


# =========================
# CATEGORY PRODUCTS
# =========================

def category_products(request, pk):

    category = get_object_or_404(
        Category,
        pk=pk
    )

    products = Product.objects.filter(
        category=category,
        available=True
    ).select_related(
        "category"
    )

    return render(
        request,
        "catalog/category.html",
        {
            "category": category,
            "products": products,
        }
    )


# =========================
# ADD TO CART
# =========================

def add_to_cart(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk,
        available=True
    )

    cart = request.session.get(
        "cart",
        {}
    )

    product_id = str(
        product.id
    )

    if product_id in cart:

        cart[product_id] += 1

    else:

        cart[product_id] = 1

    request.session["cart"] = cart

    request.session.modified = True

    # =========================
    # AJAX
    # =========================

    if request.headers.get(
        "X-Requested-With"
    ) == "XMLHttpRequest":

        cart_count = sum(
            cart.values()
        )

        return JsonResponse(
            {
                "success": True,
                "message": "Товар добавлен в корзину",
                "cart_count": cart_count,
            }
        )

    return redirect("home")


# =========================
# INCREASE CART
# =========================

def increase_cart(request, pk):

    cart_data = request.session.get(
        "cart",
        {}
    )

    product_id = str(pk)

    if product_id in cart_data:

        cart_data[product_id] += 1

    request.session["cart"] = cart_data

    request.session.modified = True

    return redirect("cart")


# =========================
# DECREASE CART
# =========================

def decrease_cart(request, pk):

    cart_data = request.session.get(
        "cart",
        {}
    )

    product_id = str(pk)

    if product_id in cart_data:

        cart_data[product_id] -= 1

        if cart_data[product_id] <= 0:

            del cart_data[product_id]

    request.session["cart"] = cart_data

    request.session.modified = True

    return redirect("cart")


# =========================
# CART
# =========================

def cart(request):

    cart_data = request.session.get(
        "cart",
        {}
    )

    products = []

    total = Decimal("0.00")

    # =========================
    # CALCULATE TOTAL
    # =========================

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        subtotal = (
            product.price * quantity
        )

        total += subtotal

        products.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    # =========================
    # PROMOCODE
    # =========================

    promo_code = request.session.get(
        "promo_code",
        ""
    )

    promo_error = ""

    discount = Decimal("0.00")

    # =========================
    # APPLY PROMOCODE
    # =========================

    if request.method == "POST":

        entered_code = request.POST.get(
            "promo_code",
            ""
        ).strip().upper()

        if entered_code == "CLOTHE10":

            promo_code = "CLOTHE10"

            request.session["promo_code"] = (
                "CLOTHE10"
            )

        else:

            promo_code = ""

            request.session.pop(
                "promo_code",
                None
            )

            promo_error = (
                "Неверный промокод."
            )

    # =========================
    # DISCOUNT
    # =========================

    if promo_code == "CLOTHE10":

        discount = (
            total * Decimal("10")
            / Decimal("100")
        )

    # =========================
    # FINAL TOTAL
    # =========================

    final_total = (
        total - discount
    )

    request.session.modified = True

    return render(
        request,
        "catalog/cart.html",
        {
            "products": products,
            "total": total,
            "discount": discount,
            "final_total": final_total,
            "promo_code": promo_code,
            "promo_error": promo_error,
        }
    )


# =========================
# REMOVE FROM CART
# =========================

def remove_from_cart(request, pk):

    cart_data = request.session.get(
        "cart",
        {}
    )

    product_id = str(pk)

    if product_id in cart_data:

        del cart_data[product_id]

    request.session["cart"] = cart_data

    # =========================
    # REMOVE PROMOCODE
    # =========================

    if not cart_data:

        request.session.pop(
            "promo_code",
            None
        )

    request.session.modified = True

    return redirect("cart")


# =========================
# CHECKOUT
# =========================

def checkout(request):

    cart_data = request.session.get(
        "cart",
        {}
    )

    # =========================
    # EMPTY CART
    # =========================

    if not cart_data:

        return redirect("cart")

    # =========================
    # PRODUCTS
    # =========================

    products = Product.objects.filter(
        id__in=cart_data.keys(),
        available=True
    )

    items = []

    total = Decimal("0.00")

    # =========================
    # CALCULATE TOTAL
    # =========================

    for product in products:

        quantity = cart_data.get(
            str(product.id),
            0
        )

        subtotal = (
            product.price * quantity
        )

        total += subtotal

        items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    # =========================
    # PROMOCODE
    # =========================

    promo_code = request.session.get(
        "promo_code",
        ""
    )

    discount = Decimal("0.00")

    if promo_code == "CLOTHE10":

        discount = (
            total * Decimal("10")
            / Decimal("100")
        )

    # =========================
    # FINAL TOTAL
    # =========================

    final_total = (
        total - discount
    )

    # =========================
    # CREATE ORDER
    # =========================

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        address = request.POST.get(
            "address",
            ""
        ).strip()

        order = Order.objects.create(
            name=name,
            phone=phone,
            address=address,
            total=final_total,
        )

        # =========================
        # ORDER ITEMS
        # =========================

        for item in items:

            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["product"].price,
            )

        # =========================
        # CLEAR CART
        # =========================

        request.session["cart"] = {}

        request.session.pop(
            "promo_code",
            None
        )

        request.session.modified = True

        # =========================
        # SUCCESS
        # =========================

        return redirect(
            "order_success",
            pk=order.pk
        )

    return render(
        request,
        "catalog/checkout.html",
        {
            "items": items,
            "total": total,
            "discount": discount,
            "final_total": final_total,
            "promo_code": promo_code,
        }
    )


# =========================
# ORDER SUCCESS
# =========================

def order_success(request, pk):

    order = get_object_or_404(
        Order,
        pk=pk
    )

    return render(
        request,
        "catalog/order_success.html",
        {
            "order": order,
        }
    )


# =========================
# PRODUCT RATING
# =========================

def rate_product(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    if request.method == "POST":

        try:

            rating = int(
                request.POST.get(
                    "rating",
                    0
                )
            )

        except (ValueError, TypeError):

            rating = 0

        if 1 <= rating <= 5:

            total_rating = (
                product.rating *
                product.rating_count
            )

            product.rating_count += 1

            product.rating = (
                total_rating + rating
            ) / product.rating_count

            product.save()

    return redirect(
        "product_detail",
        pk=product.pk
    )