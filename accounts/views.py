import decimal

from multi_form_view import MultiModelFormView

from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import transaction
from django.views.generic import View, TemplateView
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from accounts.helpers import calc_tracking_number
from electronics.models import Product

from .forms import (
    BillingAddressForm,
    CheckOutForm,
    CustomUserForm,
    CustomerForm,
    ShippingAddressForm,
)
from .models import (
    BillingAddress,
    Cart,
    CartItems,
    Customer,
    Order,
    ShippingAddress,
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


class CheckOutView(View):
    template_name = "users/checkout.html"
    form_classes = {
        "user_form": CustomUserForm(),
        "customer_form": CustomerForm(),
        "checkout_form": CheckOutForm(),
        "address_form": BillingAddressForm(),
        "shipping_address_form": ShippingAddressForm(),
    }

    def get(self, request, *args, **kwargs):
        user = self.request.user
        customer = Customer.objects.get(user=user)
        cart = Cart.objects.get(customer=customer)
        cart_items = CartItems.objects.filter(cart=cart)
        billing_address_instance = BillingAddress.objects.filter(
            customer=customer
        ).first()

        if user:
            self.form_classes = {
                "user_form": CustomUserForm(instance=user),
                "customer_form": CustomerForm(instance=customer),
                "checkout_form": CheckOutForm(),
                "address_form": BillingAddressForm(instance=billing_address_instance),
                "shipping_address_form": ShippingAddressForm(),
            }

        sub_total = 0
        for item in cart_items:
            sub_total += decimal.Decimal(item.total_price)

        context = {
            form_name: form_class for form_name, form_class in self.form_classes.items()
        }
        context["sub_total"] = "{:.3f}".format(sub_total)
        context["ordered_items"] = cart_items

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        data = request.POST
        current_user = request.user
        customer = Customer.objects.get(user=current_user)
        # User Form input data
        user_data = {
            "email": data.get("email"),
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
        }

        # Billing Address Form input data
        billing_address_data = {
            "customer": customer,
            "address_line_1": data.get("address_line_1"),
            "address_line_2": data.get("address_line_2"),
            "city": data.get("city"),
            "state_or_province": data.get("state_or_province"),
            "postal_code": data.get("postal_code"),
        }

        # Shipping Address Form input data
        # sh_first_name = data.get("sh_first_name")
        # sh_last_name = data.get("sh_last_name")
        # sh_email = data.get("sh_email")
        # sh_phone_number = data.get("sh_phone")
        # sh_address_line_1 = data.get("sh_address_line_1")
        # shipping_address_data = {
        #     address_line_1: address_line_1,
        #     address_line_2: address_line_2,
        #     city: city,
        #     state_or_province: state_or_province,
        #     postal_code: postal_code,
        # }

        # User Form input data
        customer_data = {
            "phone_number": data.get("phone_number"),
        }

        # Customer Form input data
        order_data = {
            "customer": customer,
            "order_notes": data.get("order_notes"),
            "payment_method": data.get("payment_method"),
            "subtotal": float(data.get("sub_total")),
            "shipping_cost": data.get("shipping_cost"),
            "total": float(data.get("total")),
            "tracking_number": calc_tracking_number(),
        }

        create_acc = data.get("create_account")
        password = data.get("password")
        ship_to_diff_address = data.get("ship_to_different_address")

        with transaction.atomic():
            if ship_to_diff_address == "false":
                user_form = CustomUserForm(user_data, instance=current_user)
                customer_form = CustomerForm(customer_data, instance=customer)
                order_form = CheckOutForm(order_data)

                existing_billing_address = BillingAddress.objects.filter(
                    customer=customer
                ).first()
                if existing_billing_address:
                    billing_address_form = BillingAddressForm(
                        billing_address_data, instance=existing_billing_address
                    )
                else:
                    billing_address_form = BillingAddressForm(billing_address_data)

                existing_shipping_address = ShippingAddress.objects.filter(
                    customer=customer
                ).first()
                if existing_shipping_address:
                    shipping_address_form = ShippingAddressForm(
                        billing_address_data, instance=existing_shipping_address
                    )
                else:
                    shipping_address_form = ShippingAddressForm(billing_address_data)

                is_form_valid = [
                    form.is_valid()
                    for form in [
                        user_form,
                        customer_form,
                        billing_address_form,
                        shipping_address_form,
                        order_form,
                    ]
                ]
                if all(is_form_valid):
                    if create_acc and password:
                        current_user.set_password(user_form.cleaned_data.get("password"))
                        current_user.save()
                    user_form.save()
                    customer_form.save()
                    billing_address = billing_address_form.save()
                    shipping_address = shipping_address_form.save()

                    order_data["billing_address"] = billing_address
                    order_data["shipping_address"] = shipping_address
                    order_form = CheckOutForm(order_data)
                    order = order_form.save()

                    return redirect(
                        reverse("khalti_payment") + "?order_id=" + str(order.id)
                    )
                else:
                    context = {
                        "user_form": user_form,
                        "customer_form": customer_form,
                        "address_form": billing_address_form,
                        "shipping_address_form": shipping_address_form,
                        "checkout_form": order_form,
                    }
                    return render(request, self.template_name, context)

            if ship_to_diff_address == "true":
                pass


class KhaltiPaymentView(View):
    template_name = "main/payment/khalti.html"

    def get(self, request, *args, **kwargs):
        order_id = request.GET.get("order_id")
        order = Order.objects.get(id=order_id)
        context = {
            "order": order,
        }
        return render(request, self.template_name, context)


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
