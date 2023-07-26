from django.db import models


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


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    description = models.TextField()
    product_img_thumbnail = models.ImageField(upload_to="product/", blank=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    category = models.ForeignKey(
        Category,
        default="",
        on_delete=models.CASCADE
    )

    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="product_images/")

    def __str__(self):
        return self.product.name
