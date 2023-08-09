from django import forms

from .models import (
    Product,
    Review,
    Contact,
    NewsLetter,
)


class AddProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["images"].widget.attrs.update({
            "multiple": True,
        })

    images = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
            }
        )
    )

    class Meta:
        model = Product
        exclude = ("slug", "views_count",)

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the name of the product..."
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the price of the product..."
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the description of the product..."
                }
            ),
            "product_img_thumbnail": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "is_featured": forms.CheckboxInput(
                attrs={
                    "class": "form-control",
                    "class": "form-check-input mt-2",
                }
            ),
            "discount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "tag": forms.SelectMultiple(
                attrs={
                    "class": "form-select",
                }
            ),
        }


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


class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = "__all__"
