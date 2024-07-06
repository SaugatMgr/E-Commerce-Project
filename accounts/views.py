from multi_form_view import MultiModelFormView

from django.db import transaction
from django.views.generic import View, TemplateView, CreateView
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from electronics.models import Product

from .forms import (
    CheckOutForm,
    CustomerForm,
)
from .models import (
    Cart,
    CartItems,
    Customer,
    Order,
    WishList,
)


class UserAccountView(MultiModelFormView):
    form_classes = {"customer_form": CustomerForm, "checkout_form": CheckOutForm}

    template_name = "users/my_account/my_account.html"

    def forms_valid(self, forms):
        user = self.request.user
        customer_order = Order.objects.get(
            customer=Customer.objects.get(user=user)
        ).customer

        print(customer_order)

        forms["customer_form"].instance.user = user
        forms["checkout_form"].instance.customer = customer_order

        forms["customer_form"].save()
        forms["checkout_form"].save()

        return super(UserAccountView, self).forms_valid(forms)


class CheckOutView(CreateView):
    template_name = "users/checkout.html"
    form_class = CheckOutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        customer = Customer.objects.get(user=user)
        cart = Cart.objects.get(customer=customer)
        cart_items = CartItems.objects.filter(cart=cart)

        sub_total = 0
        for item in cart_items:
            sub_total += float(item.total_price)

        context["sub_total"] = "{:.3f}".format(sub_total)
        context["ordered_items"] = cart_items

        return context


class WishListView(TemplateView):
    model = WishList
    template_name = "users/wishlist.html"

    def get_context_data(self, **kwargs):
        customer, created = Customer.objects.get_or_create(user=self.request.user)

        context = super().get_context_data(**kwargs)
        context["wish_list"] = WishList.objects.filter(customer=customer).first()
        return context


class AddToWishListView(View):
    template_name = "users/wishlist.html"
    model = WishList

    def post(self, request):
        ajax_format = request.headers.get("x-requested-with")
        user = self.request.user

        with transaction.atomic():
            if ajax_format == "XMLHttpRequest":
                if not user.is_authenticated:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "Please login to continue...",
                        },
                        status=401,
                    )
                product_slug = request.POST.get("prod_slug")
                product = Product.objects.get(slug=product_slug)

                customer, created = Customer.objects.get_or_create(user=user)
                wish_list, created = WishList.objects.get_or_create(customer=customer)

                if WishList.objects.filter(customer=customer, product=product).exists():
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "Product already exists in your wishlist.",
                        },
                        status=409,
                    )
                else:
                    wish_list.product.add(product)
                    wish_list.save()
                    return JsonResponse(
                        {
                            "success": True,
                            "message": f"{product.name} added to your wishlist.",
                        },
                        status=200,
                    )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Cannot process.Must be and AJAX XMLHttpRequest.",
                    },
                    status=400,
                )


@require_POST
def remove_wishlist_item(request):
    ajax_format = request.headers.get("x-requested-with")

    with transaction.atomic():
        if ajax_format == "XMLHttpRequest":
            product_slug = request.POST.get("prod_slug")
            if product_slug:
                product = Product.objects.get(slug=product_slug)
                customer = Customer.objects.get(user=request.user)

                wish_list = WishList.objects.get(customer=customer)
                wish_list.product.remove(product)
                wish_list.save()

                return JsonResponse(
                    {
                        "success": True,
                        "message": f"{product.name} removed from your wishlist.",
                    },
                    status=200,
                )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Cannot process.Must be and AJAX XMLHttpRequest.",
                },
                status=400,
            )
