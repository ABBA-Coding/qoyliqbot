# Generated by Django 4.2.9 on 2024-04-28 01:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0007_selectedproduct"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="address",
        ),
        migrations.RemoveField(
            model_name="order",
            name="cash_type",
        ),
        migrations.RemoveField(
            model_name="order",
            name="charge_id",
        ),
        migrations.RemoveField(
            model_name="order",
            name="comment",
        ),
        migrations.RemoveField(
            model_name="order",
            name="cost",
        ),
        migrations.RemoveField(
            model_name="order",
            name="delivery",
        ),
        migrations.RemoveField(
            model_name="order",
            name="delivery_cost",
        ),
        migrations.RemoveField(
            model_name="order",
            name="distance",
        ),
        migrations.RemoveField(
            model_name="order",
            name="filial",
        ),
    ]
