from accounts.models import (
    Customer,
    Cart,
    CartItems,
)


def electronics_context(request):
    context = {}
    user = request.user

    if user.is_authenticated:
        current_customer = Customer.objects.filter(user=user).first()
        if current_customer:
            cart = Cart.objects.filter(customer=current_customer).first()
            if cart:
                cart_items = CartItems.objects.filter(cart=cart)
                if cart_items:
                    context["cart_items"] = cart_items
                    context["cart_items_count"] = cart_items.count()
                    context["sub_total"] = sum(
                        [item.quantity * item.product.price for item in cart_items]
                    )
    return context
