from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)
from django import forms
from .models import (
    Address,
    CustomUser,
    Order,
    Customer,
)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
        )


# This is the form that will be used to create a new user or display the user's information in checkout form.
class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
        )


class CheckOutForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = (
            "cart",
            "status",
            "customer",
        )


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ("user",)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            "address_line_1",
            "address_line_2",
            "city",
            "state_or_province",
            "postal_code",
        )
