from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator
import uuid

from .managers import CustomUserManager

from electronics.models import Product


class TimeStamp(models.Model):
    created_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
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
        CustomUser,
        on_delete=models.CASCADE,
        related_name="user"
    )
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Cart(TimeStamp):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    customer = models.OneToOneField(
        Customer,
        on_delete=models.SET_NULL,
        related_name="customer",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.id}"


class CartItems(TimeStamp):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_product_in_cart"
            )
        ]
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="cart"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="products",
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    VAT = 13

    @property
    def total_price(self):
        return self.quantity * (self.product.price * (1 + self.VAT/100))

    def __str__(self):
        return self.product.name


class Order(TimeStamp):
    ORDER_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("On the Way", "On the Way"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]
    cart = models.OneToOneField(
        Cart,
        on_delete=models.CASCADE,
    )
    street_no = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    order_notes = models.TextField()
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS_CHOICES, default="Pending")

    def __st__(self):
        return f"By {self.cart.customer.user.first_name}"
    