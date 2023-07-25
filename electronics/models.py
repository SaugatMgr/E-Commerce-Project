from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    product_img_thumbnail = models.ImageField(upload_to="product/", blank=True)

    def __str__(self):
        return self.name
    