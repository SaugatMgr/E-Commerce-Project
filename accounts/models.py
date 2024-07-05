from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator
import uuid

from .managers import CustomUserManager

from electronics.models import Product


class TimeStamp(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
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
    phone_number = PhoneNumberField(null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Cart(TimeStamp):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    customer = models.OneToOneField(
        Customer,
        on_delete=models.SET_NULL,
        related_name="customer",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.id}"


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
        vat_added_price = self.quantity * (self.product.price * (1 + self.VAT / 100))
        discount = self.product.discount

        if discount:
            discount_added_price = self.product.price * (1 - (discount / 100))
            final_price = "{:.3f}".format(vat_added_price - discount_added_price)
        else:
            final_price = "{:.3f}".format(vat_added_price)

        return final_price

    def __str__(self):
        return self.product.name


class Order(TimeStamp):
    customer = models.OneToOneField(
        Customer,
        on_delete=models.SET_NULL,
        related_name="customer_order",
        null=True,
        blank=True,
    )
    ORDER_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("On the Way", "On the Way"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]
    state_or_country = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    order_notes = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS_CHOICES, default="Pending"
    )

    def __str__(self):
        return f"By {self.customer.user.first_name} {self.customer.user.last_name}"


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
