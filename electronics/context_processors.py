from .models import (
    Product,
    Category,
    SubCategory,
)
from accounts.models import (
    Customer,
    Cart,
    CartItems,
)

def electronics_context(request):
    context = {}
    user = request.user
    all_categories = Category.objects.all()
    all_products = Product.objects.all()

    filter_product_by_views = Product.objects.filter(views_count__gte=0)
    filter_product_by_higher_views = filter_product_by_views.order_by(
        "-views_count"
    )
    products_by_date = filter_product_by_views.order_by("-added_date")

    context["categories"] = all_categories
    context["product_category"] = all_categories[:9]
    context["product_category_rem"] = all_categories[9:12]
    context["product_sub_category"] = SubCategory.objects.all()

    context["today_deals_categories_first"] = all_categories.first()
    context["today_deals_categories"] = all_categories[1:8]
    context["today_deals_products"] = products_by_date

    context["best_sellers"] = filter_product_by_higher_views
    context["all_products"] = all_products

    context["new_products_left_sidebar"] = products_by_date[:2]
    context["new_products_center"] = products_by_date[2]
    context["new_products_right_sidebar"] = products_by_date[3:5]

    context["featured_products"] = all_products.filter(is_featured=True)
    context["default_active_tab_category"] = Category.objects.first()
    context["remaining_categories"] = all_categories[1:8]

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