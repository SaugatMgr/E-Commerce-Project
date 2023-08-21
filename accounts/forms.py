from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import (
    CustomUser,
    Order,
)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name",
                  "password1", "password2", )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", )


class CheckOutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

class CustomerForm(forms.ModelForm):
    class Meta:
        widgets = {
            "phone_number": PhoneNumberPrefixWidget(),
        }
