from accounts.models import (
    Customer,
    Cart,
    CartItems,
)
from electronics.models import Category, Product, Tag


def electronics_context(request):
    context = {}
    user = request.user
    context["footer_categories"] = Category.objects.filter()[:5]
    context["categories"] = Category.objects.all()
    context["product_tags"] = Tag.objects.all()
    context["top_rated_products"] = Product.objects.all().order_by("-views_count")[:3]

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
