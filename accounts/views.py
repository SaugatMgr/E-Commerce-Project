import decimal
import requests
import json
import uuid
import base64

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import transaction
from django.views.generic import View, TemplateView
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from accounts.helpers import (
    build_abs_uri,
    calc_tracking_number,
    generate_hmac_signature,
)
from accounts.tasks import generate_and_send_order_pdf
from electronics.models import Product

from .forms import (
    BillingAddressForm,
    CheckOutForm,
    CustomUserForm,
    CustomerForm,
    MyAccountBillingAddressForm,
    MyAccountDetailsForm,
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


class UserAccountView(LoginRequiredMixin, View):
    template_name = "users/my_account/my_account.html"
    form_classes = {
        "user_form": MyAccountDetailsForm(),
        "billing_address_form": MyAccountBillingAddressForm(),
    }

    def get(self, request, *args, **kwargs):
        context = {}
        user = self.request.user
        customer = Customer.objects.filter(user=user).first()
        if customer:
            # For Order tab
            orders = Order.objects.filter(customer=customer)
            if orders:
                context["orders_by_customer"] = orders

            # For Account Details and Billing Address tab
            billing_address_instance = BillingAddress.objects.filter(
                customer=customer
            ).first()

            self.form_classes = {
                "user_form": MyAccountDetailsForm(instance=user),
                "billing_address_form": MyAccountBillingAddressForm(
                    instance=billing_address_instance
                ),
            }

        context.update(
            {
                form_name: form_class
                for form_name, form_class in self.form_classes.items()
            }
        )
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        data = request.POST
        current_user = request.user
        customer, _ = Customer.objects.get_or_create(user=current_user)
        ajax_format = request.headers.get("x-requested-with")

        with transaction.atomic():
            if ajax_format == "XMLHttpRequest":
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
                if data.get("from_account_details_page"):
                    user_form = MyAccountDetailsForm(user_data, instance=current_user)
                    if user_form.is_valid():
                        user_form.save()
                        return JsonResponse(
                            {
                                "success": True,
                                "message": "Account details updated successfully.",
                            },
                            status=200,
                        )
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "An error occurred while updating your account details.",
                        },
                        status=400,
                    )
                if data.get("from_billing_address_page"):
                    existing_billing_address = BillingAddress.objects.filter(
                        customer=customer
                    ).first()
                    if existing_billing_address:
                        billing_address_form = MyAccountBillingAddressForm(
                            billing_address_data,
                            instance=existing_billing_address,
                            customer=customer,
                        )
                    else:
                        billing_address_form = MyAccountBillingAddressForm(
                            billing_address_data, customer=customer
                        )

                    if billing_address_form.is_valid():
                        billing_address_form.save()
                        return JsonResponse(
                            {
                                "success": True,
                                "message": "Billing address updated successfully.",
                            },
                            status=200,
                        )
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "An error occurred while updating your billing address.",
                        },
                        status=400,
                    )
            return JsonResponse(
                {
                    "success": False,
                    "message": "Cannot process.Must be and AJAX XMLHttpRequest.",
                },
                status=400,
            )


class CheckOutView(LoginRequiredMixin, View):
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
        payment_method = data.get("payment_method")
        current_user = request.user
        customer = Customer.objects.get(user=current_user)
        existing_order = Order.objects.filter(
            customer=customer, status="Pending", payment_status="UNPAID"
        ).first()
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
            "payment_method": payment_method,
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
                if existing_order:
                    order_form = CheckOutForm(order_data, instance=existing_order)
                else:
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
                        current_user.set_password(
                            user_form.cleaned_data.get("password")
                        )
                        current_user.save()
                    user_form.save()
                    customer_form.save()
                    billing_address = billing_address_form.save()
                    shipping_address = shipping_address_form.save()

                    order = order_form.save(commit=False)
                    order.billing_address = billing_address
                    order.shipping_address = shipping_address
                    order.save()

                    if payment_method == "Khalti":
                        return redirect(reverse("khalti_payment", args=[order.id]))
                    if payment_method == "Esewa":
                        return redirect(reverse("esewa_payment", args=[order.id]))
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


class KhaltiPaymentView(LoginRequiredMixin, View):
    template_name = "payment/Khalti/khalti.html"

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get("order_id")
        order = Order.objects.get(id=order_id)
        cart = Cart.objects.get(customer=order.customer)
        cart_items = CartItems.objects.filter(cart=cart)
        context = {
            "order": order,
            "cart_items": cart_items,
            "khalti_public_key": settings.KHALTI_PUBLIC_KEY,
        }
        return render(request, self.template_name, context)


class KhaltiPaymentVerifyView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = request.body
            data = json.loads(data)

            order_id = data.get("order_id")
            amount = data.get("amount")
            token = data.get("token")

            if not order_id or not amount or not token:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Missing required parameters.",
                    }
                )

            url = "https://khalti.com/api/v2/payment/verify/"
            payload = {
                "token": token,
                "amount": 1000,
            }
            headers = {
                "Authorization": f"key {settings.KHALTI_SECRET_KEY}",
            }

            with transaction.atomic():
                response = requests.post(url, headers=headers, data=payload)
                response_data = response.json()
                if response_data.get("idx"):
                    order = Order.objects.get(id=order_id)
                    order.payment_status = "PAID"
                    order.status = "Completed"
                    order.save()

                    cart = Cart.objects.get(customer=order.customer)
                    cart_items = CartItems.objects.filter(cart=cart)
                    # cart_items_ids = list(cart_items.values_list("id", flat=True))

                    generate_and_send_order_pdf(
                        {
                            "request": request,
                            "order": order,
                            "cart_items": cart_items,
                        },
                        order_id=order.id,
                        user_email=order.customer.user.email,
                        customer_first_name=order.customer.user.first_name,
                        customer_last_name=order.customer.user.last_name,
                    )

                    # base_url = request.build_absolute_uri("/")
                    # css_url = f"{base_url}static/pallas/css/style.css"
                    # plugins_css_url = f"{base_url}static/pallas/css/plugins.css"
                    # logo_url = f"{base_url}static/pallas/img/logo/logo.png"

                    # generate_and_send_order_pdf.delay(
                    #     {
                    #         "order_id": order.id,
                    #         "cart_items_ids": cart_items_ids,
                    #         "css_url": css_url,
                    #         "plugins_css_url": plugins_css_url,
                    #         "logo_url": logo_url,
                    #     },
                    #     user_email=order.customer.user.email,
                    #     customer_first_name=order.customer.user.first_name,
                    #     customer_last_name=order.customer.user.last_name,
                    # )

                    # result = chain(
                    #     generate_order_pdf.s(
                    #         {
                    #             "order_id": order.id,
                    #             "cart_items_ids": cart_items_ids,
                    #             "css_url": css_url,
                    #             "plugins_css_url": plugins_css_url,
                    #             "logo_url": logo_url,
                    #         }
                    #     )
                    #     | send_order_pdf_email.s(
                    #         order_id=order.id,
                    #         user_email=order.customer.user.email,
                    #         customer_first_name=order.customer.user.first_name,
                    #         customer_last_name=order.customer.user.last_name,
                    #     )
                    # ).apply_async()
                    cart_items.delete()
                    return JsonResponse(
                        {
                            "success": True,
                            "message": "Payment successful.",
                        },
                        status=200,
                    )
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Invalid JSON data.",
                },
                status=400,
            )
        except requests.RequestException:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Payment verification request failed.",
                },
                status=500,
            )
        except Order.DoesNotExist:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Order does not exist.",
                },
                status=404,
            )
        except Exception as e:
            print(str(e))
            return JsonResponse(
                {
                    "success": False,
                    "message": "An unexpected error occurred.",
                },
                status=500,
            )


class EsewaPaymentView(LoginRequiredMixin, View):
    template_name = "payment/Esewa/esewa.html"

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get("order_id")
        order = Order.objects.get(id=order_id)
        cart = Cart.objects.get(customer=order.customer)
        cart_items = CartItems.objects.filter(cart=cart)

        transaction_uuid = uuid.uuid4()
        product_code = settings.ESEWA_MERCHANT_ID
        message = f"total_amount=110,transaction_uuid={transaction_uuid},product_code={product_code}"

        context = {
            "order": order,
            "shipping_cost": order.shipping_cost,
            "cart_items": cart_items,
            "success_url": build_abs_uri(request, "esewa_payment_verify", order_id),
            "failure_url": build_abs_uri(request, "esewa_payment", order_id),
            "transaction_uuid": transaction_uuid,
            "hmac_signature": generate_hmac_signature(settings.ESEWA_SECRET, message),
            "esewa_merchant_id": product_code,
        }
        return render(request, self.template_name, context)


class EsewaPaymentVerifyView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            order_id = kwargs.get("order_id")
            get_response_encoded_data = request.GET.get("data")
            get_response_decoded_data = base64.b64decode(
                get_response_encoded_data
            ).decode("utf-8")
            get_response_decoded_data = json.loads(get_response_decoded_data)

            get_url = (
                f"https://uat.esewa.com.np/api/epay/transaction/status/"
                f"?product_code=EPAYTEST"
                f"&total_amount={get_response_decoded_data.get('total_amount')}"
                f"&transaction_uuid={get_response_decoded_data.get('transaction_uuid')}"
            )

            with transaction.atomic():
                response = requests.get(get_url)
                response = response.json()

                if response.get("status") == "COMPLETE" and response.get("ref_id"):
                    order = Order.objects.get(id=order_id)
                    order.payment_status = "PAID"
                    order.status = "Completed"
                    order.save()

                    cart = Cart.objects.get(customer=order.customer)
                    cart_items = CartItems.objects.filter(cart=cart)

                    generate_and_send_order_pdf(
                        {
                            "request": request,
                            "order": order,
                            "cart_items": cart_items,
                        },
                        order_id=order_id,
                        user_email=order.customer.user.email,
                        customer_first_name=order.customer.user.first_name,
                        customer_last_name=order.customer.user.last_name,
                    )
                    cart_items.delete()

                    messages.success(
                        request,
                        "Payment successful.",
                    )
                    return redirect(reverse("home"))
                else:
                    messages.error(
                        request, "Payment verification failed. Please try again."
                    )
                    return redirect(reverse("esewa_payment", args=[order_id]))

        except requests.RequestException as e:
            messages.error(request, f"Request error: {e}")
            return redirect(reverse("esewa_payment", args=[order_id]))

        except base64.binascii.Error as e:
            messages.error(request, f"Base64 decoding error: {e}")
            return redirect(reverse("esewa_payment", args=[order_id]))

        except json.JSONDecodeError as e:
            messages.error(request, f"JSON decoding error: {e}")
            return redirect(reverse("esewa_payment", args=[order_id]))

        except Order.DoesNotExist:
            messages.error(request, "Order does not exist.")
            return redirect(reverse("esewa_payment", args=[order_id]))

        except Exception as e:
            messages.error(request, f"Unexpected error: {e}")
            return redirect(reverse("esewa_payment", args=[order_id]))


class WishListView(LoginRequiredMixin, TemplateView):
    model = WishList
    template_name = "users/wishlist.html"

    def get_context_data(self, **kwargs):
        customer, created = Customer.objects.get_or_create(user=self.request.user)
        wish_list = WishList.objects.filter(customer=customer).first()

        context = super().get_context_data(**kwargs)
        context["wish_list"] = wish_list
        context["product_count"] = 0 if not wish_list else wish_list.product.count()
        return context


class AddToWishListView(LoginRequiredMixin, View):
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
