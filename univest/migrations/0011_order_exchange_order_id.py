# Generated by Django 4.2.5 on 2023-09-07 18:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("univest", "0010_remove_ideastatus_exchanges_order_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="exchange_order_id",
            field=models.CharField(
                default="", max_length=255, verbose_name="Exchange Order ID"
            ),
            preserve_default=False,
        ),
    ]
