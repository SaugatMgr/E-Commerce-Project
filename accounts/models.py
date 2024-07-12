import uuid
import decimal

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.core.validators import MinValueValidator

from accounts.constants import (
    ORDER_STATUS_CHOICES,
    PAYMENT_METHOD_CHOICES,
    PAYMENT_STATUS_CHOICES,
)

from .managers import CustomUserManager

from electronics.models import Product


class TimeStamp(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Customer(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="user"
    )
    phone_number = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state_or_province = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        abstract = True


class BillingAddress(Address):
    class Meta:
        verbose_name = "Billing Address"
        verbose_name_plural = "Billing Addresses"

    def __str__(self):
        return f"{self.customer.user.first_name} {self.customer.user.last_name}'s Billing Address"


class ShippingAddress(Address):
    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"

    def __str__(self):
        return f"{self.customer.user.first_name} {self.customer.user.last_name}'s Shipping Address"


class Cart(TimeStamp):
    customer = models.OneToOneField(
        Customer,
        on_delete=models.SET_NULL,
        related_name="customer",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Cart #{self.id} of {self.customer.user.first_name} {self.customer.user.last_name}"


class CartItems(TimeStamp):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="products",
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)

    class Meta:
        unique_together = ("cart", "product")
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    VAT = 13

    @property
    def total_price(self):
        vat_added_price = self.quantity * (
            self.product.price * decimal.Decimal((1 + self.VAT / 100))
        )
        discount = self.product.discount

        if discount:
            discount_added_price = self.product.price * decimal.Decimal(
                (1 - (discount / 100))
            )
            final_price = "{:.3f}".format(vat_added_price - discount_added_price)
        else:
            final_price = "{:.3f}".format(vat_added_price)

        return final_price

    def __str__(self):
        return self.product.name


class Order(TimeStamp):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="customer_order",
    )

    order_notes = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS_CHOICES, default="Pending"
    )
    shipping_address = models.ForeignKey(
        ShippingAddress,
        related_name="shipping_orders",
        on_delete=models.SET_NULL,
        null=True,
    )
    billing_address = models.ForeignKey(
        BillingAddress,
        related_name="billing_orders",
        on_delete=models.SET_NULL,
        null=True,
    )
    order_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default="UNPAID"
    )
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    tracking_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.user.first_name} {self.customer.user.last_name}"


class WishList(TimeStamp):
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, related_name="customer_wishlist"
    )
    product = models.ManyToManyField(Product, related_name="wishlisted")

    class Meta:
        verbose_name = "WishList"
        verbose_name_plural = "WishList"

    def __str__(self):
        return (
            f"{self.customer.user.first_name} {self.customer.user.last_name} WishList"
        )
