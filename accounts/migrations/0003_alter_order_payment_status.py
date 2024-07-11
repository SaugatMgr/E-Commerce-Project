# Generated by Django 4.2.3 on 2024-07-10 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(blank=True, choices=[('UNPAID', 'Unpaid'), ('PAID', 'Paid'), ('REFUNDED', 'Refunded')], default='UNPAID', max_length=20),
        ),
    ]
