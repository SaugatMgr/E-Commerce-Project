# Generated by Django 4.2.3 on 2024-07-24 04:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('electronics', '0002_alter_product_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-added_date',)},
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='electronics.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(related_name='products', to='electronics.tag'),
        ),
    ]
