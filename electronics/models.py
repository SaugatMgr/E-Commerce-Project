from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class TimeStamp(models.Model):
    added_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class NameMsgEmail(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=150)
    msg = models.TextField()

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(
        Category,
        default="",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Product(TimeStamp):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    price = models.IntegerField()
    description = models.TextField()
    product_img_thumbnail = models.ImageField(upload_to="product/", blank=True)
    views_count = models.PositiveBigIntegerField()
    is_featured = models.BooleanField(default=False)
    
    category = models.ForeignKey(
        Category,
        default="",
        on_delete=models.CASCADE
    )

    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})


class Review(NameMsgEmail, TimeStamp):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user}: {self.msg[:30]}"


class Contact(NameMsgEmail, TimeStamp):
    subject = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}: {self.msg[:30]}"


class Image(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    images = models.ImageField(upload_to="product/product_images/")

    def __str__(self):
        return self.product.name


class NewsLetter(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email
