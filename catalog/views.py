from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)

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

    # Search
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
    )


    # Search by product name
    if search:

        products = products.filter(
            name__icontains=search
        )


    # All categories
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
        pk=pk
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

    return redirect("cart")


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

    total = 0

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

    return render(
        request,
        "catalog/cart.html",
        {
            "products": products,
            "total": total,
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

    # If cart is empty
    if not cart_data:

        return redirect("cart")


    # Get available products
    products = Product.objects.filter(
        id__in=cart_data.keys(),
        available=True
    )


    items = []

    total = 0


    # Calculate total
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


    # Create order
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
            total=total,
        )


        # Create order items
        for item in items:

            OrderItem.objects.create(
                order=order,

                product=item["product"],

                quantity=item["quantity"],

                price=item["product"].price,
            )


        # Clear cart
        request.session["cart"] = {}

        request.session.modified = True


        # Success page
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