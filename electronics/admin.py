from tinymce.widgets import TinyMCE
from django.contrib import admin

from .models import (
    Product,
    Image,
    Category,
    SubCategory,
    Tag,
    Review,
    Contact,
    NewsLetter,
)
from django import forms

class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Product
        fields = '__all__'

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

admin.site.register(Product, ProductAdmin)

admin.site.register([Image, Category, SubCategory, Tag, Review, Contact, NewsLetter, ])
