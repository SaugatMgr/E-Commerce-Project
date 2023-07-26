from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    description = models.TextField()
    product_img_thumbnail = models.ImageField(upload_to="product/", blank=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="product_images/")

    def __str__(self):
        return self.product.name
