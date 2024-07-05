# Generated by Django 4.2.3 on 2024-07-04 17:46

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('electronics', '0001_initial'),
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_wishlist', to='accounts.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlisted', to='electronics.product')),
            ],
            options={
                'verbose_name': 'WishList',
                'verbose_name_plural': 'WishList',
                'unique_together': {('customer', 'product')},
            },
        ),
    ]
