from django.contrib import admin

from .models import (
    Product,
    Image,
    Category,
    SubCategory,
    Tag,
)

admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Tag)
