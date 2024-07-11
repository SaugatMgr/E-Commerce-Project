from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    CustomerForm,
)
from .models import (
    BillingAddress,
    CustomUser,
    Customer,
    Cart,
    CartItems,
    Order,
    ShippingAddress,
    WishList,
)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": ("is_staff", "is_active", "groups", "user_permissions"),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Customer)
admin.site.register(
    [Cart, CartItems, Order, WishList, BillingAddress, ShippingAddress]
)
