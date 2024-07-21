from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)
from django import forms

from accounts.constants import ORDER_STATUS_CHOICES, PAYMENT_STATUS_CHOICES
from .models import (
    BillingAddress,
    CustomUser,
    Order,
    Customer,
    ShippingAddress,
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
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
        )

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if "password" not in self.data:
            del self.fields["password"]


class MyAccountDetailsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class CheckOutForm(forms.ModelForm):
    status = forms.TypedChoiceField(
        coerce=str,
        choices=ORDER_STATUS_CHOICES,
        required=False,
    )
    payment_status = forms.TypedChoiceField(
        coerce=str,
        choices=PAYMENT_STATUS_CHOICES,
        required=False,
    )
    shipping_address = forms.ModelChoiceField(
        queryset=ShippingAddress.objects.all(), required=False
    )
    billing_address = forms.ModelChoiceField(
        queryset=BillingAddress.objects.all(), required=False
    )

    class Meta:
        model = Order
        exclude = ("cart",)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("phone_number",)


class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = (
            "customer",
            "address_line_1",
            "address_line_2",
            "city",
            "state_or_province",
            "postal_code",
        )


class MyAccountBillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = (
            "address_line_1",
            "address_line_2",
            "city",
            "state_or_province",
            "postal_code",
        )
    
    def __init__(self, *args, **kwargs):
        self.customer = kwargs.pop('customer', None)
        super(MyAccountBillingAddressForm, self).__init__(*args, **kwargs)
    
    def save(self):
        billing_address = super(MyAccountBillingAddressForm, self).save(commit=False)
        billing_address.customer = self.customer
        billing_address.save()
        return billing_address


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = (
            "customer",
            "address_line_1",
            "address_line_2",
            "city",
            "state_or_province",
            "postal_code",
        )
