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

admin.site.register([Product, Image, Category, SubCategory, Tag, Review, Contact, NewsLetter, ])
