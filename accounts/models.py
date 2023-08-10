from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator
import uuid

from .managers import CustomUserManager

from electronics.models import Product


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

class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name="customer"
    )
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}"

class CartItems(models.Model):
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

    @property
    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return self.product.name