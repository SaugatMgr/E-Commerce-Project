from django import forms

from .models import (
    Product,
    Image,
    Review,
    Contact,
)

class AddProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = "__all__"


class AddImagesForm(forms.ModelForm):
    images = forms.ImageField(required=False,
        widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}))

    class Meta:
        model = Image
        fields = ("images", )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "msg",
            "name",
            "email",
        ]

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            "name",
            "email",
            "subject",
            "msg",
        ]
