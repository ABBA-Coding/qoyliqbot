# Generated by Django 4.2.9 on 2024-04-28 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0008_remove_order_address_remove_order_cash_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="all_cost",
            field=models.CharField(max_length=255),
        ),
    ]
